import pandas as pd
import time

from generics.file_locations import raw_data_folder
from generics.postgres import dataframe_to_table, execute_sql_from_file, execute_sql, \
    get_connection, dataframe_to_table_bulk


def import_calendar():
    df = pd.read_csv(raw_data_folder() / 'calendar.csv', parse_dates=['date'])
    execute_sql('drop table if exists calendar')
    execute_sql_from_file('calendar_table')
    dataframe_to_table_bulk(df, 'calendar')


def import_sell_prices():
    start = time.time()

    execute_sql('drop table if exists prices')
    execute_sql_from_file('prices_table')

    conn = get_connection()
    cur = conn.cursor()

    with open(raw_data_folder() / 'sell_prices.csv', 'r') as f:
        f.readline()  # don't read the column names as a row in copy_from
        cur.copy_from(file=f, table='prices', sep=',')

    cur.close()
    conn.close()

    end = time.time()
    print(f'import_sell_prices took {round(end - start)} seconds')


def import_sales():
    start = time.time()

    df = pd.read_csv(raw_data_folder() / 'sales_train_validation.csv')
    df.drop(['item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'], inplace=True, axis='columns')
    df2 = pd.melt(df, id_vars=['id'])

    execute_sql('drop table if exists sales_raw')
    execute_sql_from_file('sales_raw_table')
    dataframe_to_table_bulk(df2, 'sales_raw')

    end = time.time()
    print(f'import_sales took {round(end - start)} seconds')


def import_item_info():
    start = time.time()

    df = pd.read_csv(raw_data_folder() / 'sales_train_validation.csv')
    df = df[['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']]
    df.drop_duplicates(inplace=True)

    execute_sql('drop table if exists item_info')
    execute_sql_from_file('item_info_table')
    dataframe_to_table_bulk(df, 'item_info')

    end = time.time()
    print(f'import_sales took {round(end - start)} seconds')


if __name__ == '__main__':
    import_calendar()
    print('calendar imported')
    import_sell_prices()
    print('prices imported')
    import_sales()
    print('sales imported')
    import_item_info()
    print('item info imported')