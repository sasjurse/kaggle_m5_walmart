from datetime import datetime
import os
import requests
import twitter
from sqlalchemy.exc import IntegrityError
import time

from src.twitter_collector import clean_text, search_api
from src.generics.postgres import execute_sql, dataframe_from_sql
from src.generics.postgres_sqlalchemy import SearchTerm, Example
from generics.postgres import create_sa_session


def get_prediction_url():
    env_var = os.environ.get('SENTIMENT_SERVICE_HOST')
    if not env_var:
        return 'localhost'
    else:
        return env_var


def evaluate_sentiment_in_tweet(text: str):
    url = f'http://{get_prediction_url()}:5000/model/predict'

    text_fixed = clean_text(text)

    payload = {'text': [text_fixed]}
    response = requests.post(url,
                             json=payload,
                             headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        print(f'status code {response.status_code}')
        print(text)
        print(text_fixed)
        raise Exception('Problem with sentiment api')
    return response.json()['predictions'][0]['positive']


def information_we_care_about_in_tweet(tweet: twitter.models.Status):
    assert isinstance(tweet, twitter.models.Status), 'Unexpected input'
    sentiment = evaluate_sentiment_in_tweet(tweet.text)
    created_at = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S +0000 %Y')
    sentiment = round(sentiment, 3)

    print(sentiment, tweet.text)

    return Example(id=str(tweet.id), text=tweet.text, created_at=created_at, sentiment=sentiment)


def evaluate_and_upload(tweet: twitter.models.Status):
    create_table_examples()
    assert isinstance(tweet, twitter.models.Status), 'Unexpected input'

    example = information_we_care_about_in_tweet(tweet)

    sess = create_sa_session()
    try:
        sess.add(example)
        sess.commit()
    except IntegrityError:  # Triggers if we are trying to add duplicates to table
        print('uniqueness error')
    sess.close()


def evaluate_search_term(search_term: str, location='Manhattan'):
    results_api = search_api(search_term, location=location)
    for r in results_api:
        evaluate_and_upload(r)


# FIXME: SQLAlchemy is insanely slow here
def update_search_term(search: str, location: str):
    start = time.time()
    sess = create_sa_session()
    query_result = sess.query(SearchTerm)
    if query_result.count() != 1:
        print('length not 1')
        execute_sql('DELETE FROM search_term')
        row = SearchTerm(search_term=search, location=location)
        sess.add(row)
        sess.commit()
    else:
        row = query_result.first()
        row.search_term = search
        row.location = location
        sess.commit()
    end = time.time()
    print(f'Update took {end-start} time')
    sess.close()


def get_search_term():
    df = dataframe_from_sql('select * from search_term')
    return {'search_term': df['search_term'][0], 'location': df['location'][0]}


def create_table_examples():
    sql = """
    CREATE TABLE IF NOT EXISTS examples (
        id BIGINT UNIQUE,
        text VARCHAR(280),
        created_at TIMESTAMP,
        sentiment FLOAT
        )"""

    execute_sql(sql)


def create_table_search_term():
    sql = """
    CREATE TABLE IF NOT EXISTS search_term (
        search_term VARCHAR(140),
        location VARCHAR(140)
        )"""

    execute_sql(sql)
