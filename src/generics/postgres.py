import logging
import os
import psycopg2
import pandas as pd
import sqlalchemy as sa
import tempfile
import time
from generics.file_locations import sql_folder


def set_secrets_from_local():
    if not os.getenv('POSTGRES_SERVICE_HOST'):
        from credentials.set_secrets import set_postgres_secrets
        set_postgres_secrets()


def get_connection():
    set_secrets_from_local()
    conn = psycopg2.connect(user='postgres',
                            host=os.environ['POSTGRES_SERVICE_HOST'],
                            password=os.environ['POSTGRES_PASSWORD'])
    conn.autocommit = True
    return conn


def get_cursor():
    return get_connection().cursor()


def dataframe_from_sql(sql: str):
    start = time.time()
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    end = time.time()
    logging.info(f'dataframe_from_sql took {round(end-start)} seconds')
    return df


def execute_sql(sql: str):
    start = time.time()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except psycopg2.Error as e:
        print('SQL was: \n', sql)
        raise e
    cursor.close()
    conn.close()
    end = time.time()
    logging.info(f'execute_sql took {round(end-start)} seconds')


def create_sa_string(database='postgres'):
    set_secrets_from_local()
    return f"postgresql+psycopg2://postgres:{os.environ['POSTGRES_PASSWORD']}@" \
           f"{os.environ['POSTGRES_SERVICE_HOST']}:5432/{database}"


def create_sa_engine():
    db_string = create_sa_string()
    return sa.create_engine(db_string)


def create_sa_session():
    return sa.orm.Session(create_sa_engine())


def dataframe_to_table(df: pd.DataFrame, table: str, if_exists='append'):
    """SLOW because sqlalchemy
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html"""
    assert isinstance(df, pd.DataFrame), 'expected dataframe'
    start = time.time()
    df.to_sql(name=table, con=create_sa_engine(), if_exists=if_exists, index=False)
    end = time.time()
    logging.info(f'dataframe_to_table took {round(end-start)} seconds')


def execute_sql_from_file(filename: str):
    with open(sql_folder()/f'{filename}.sql', 'r') as f:
        txt = f.read()
        execute_sql(txt)


def dataframe_to_table_bulk(df: pd.DataFrame, table: str):
    """Faster, but less checks on column names and escape characters"""
    start = time.time()
    cur = get_cursor()

    with tempfile.NamedTemporaryFile() as temp:
        df.to_csv(temp.name, sep=';', date_format='%Y-%m-%d', index=False)
        temp.seek(0)
        temp.readline()  # don't read the column names as a row in copy_from
        cur.copy_from(file=temp, table=table, sep=';')

    cur.close()
    end = time.time()

    logging.info(f'dataframe_to_table_bulk took {round(end-start)} seconds')
