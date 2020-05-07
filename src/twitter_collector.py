import os
import twitter


def clean_text(text: str):
    assert isinstance(text, str), 'Expected input to be a string'
    return "".join(e for e in text if e.isalpha() or e == ' ')  # remove all characters that are not letters


def get_api_connection():
    if not os.getenv('TWITTER_CONSUMER_KEY'):
        from credentials import set_secrets
        set_secrets.set_twitter_secrets()
    return twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                       consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                       access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
                       access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


def search_api(query: str, location='Manhattan', count=100):
    clean_query = clean_text(query)
    api_conn = get_api_connection()
    q = f"q={clean_query}&location={location}&result_type=recent&count={count}&lang=en&exclude=retweets"
    return api_conn.GetSearch(raw_query=q)
