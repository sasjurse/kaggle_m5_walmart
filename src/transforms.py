from src.generics.postgres import execute_sql, dataframe_from_sql, execute_sql_from_file
import time
import psycopg2


def recreate(name: str):
    try:
        execute_sql(f'drop table if exists {name}')
    except psycopg2.errors.WrongObjectType:
        execute_sql(f'drop view if exists {name}')
    execute_sql_from_file(name)


if __name__ == '__main__':
    tables_or_views = ['sales_ext',
                       'sales_by_day',
                       'snap_info',
                       'weekday_average',
                       'snap_influence',
                       'price_changes',
                       'lags',
                       'train',
                       'model_info',
                       ]

    for t in tables_or_views:
        print(f'recreating {t}')
        start = time.time()
        recreate(t)
        end = time.time()
        print(f'creating {t} took {round(end - start)} seconds')
