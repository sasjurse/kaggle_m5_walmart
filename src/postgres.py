import os
import psycopg2
import pandas as pd


def import_secrets_from_local():
    from credentials import set_secrets
    set_secrets.set_postgres_secrets()


def get_connection():
    if not os.getenv('POSTGRES_SERVICE_HOST'):
        import_secrets_from_local()
    conn = psycopg2.connect(user='postgres',
                            host=os.environ['POSTGRES_SERVICE_HOST'],
                            password=os.environ['POSTGRES_PASSWORD'])
    conn.autocommit = True
    return conn


def get_cursor():
    return get_connection().cursor()


def dataframe_from_sql(sql: str):
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    return df


def execute_sql(sql: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except psycopg2.Error as e:
        print('SQL was: \n', sql)
        raise e
    cursor.close()
    conn.close()


def insert_dict_to_db(data: dict, table: str):
    for key, value in data.items():
        assert ',' not in key, 'No escape characters in data please'
        assert ',' not in value, 'No escape characters in values please'
    sql = f"""
    INSERT INTO {table} ({", ".join(data.keys())})
    VALUES ({", ".join(data.values())})"""

    execute_sql(sql)
