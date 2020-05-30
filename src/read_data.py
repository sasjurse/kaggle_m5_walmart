import pandas as pd

from generics.file_locations import raw_data_folder
from generics.postgres import dataframe_to_table, execute_sql_from_file, execute_sql, get_connection


def import_calendar():
    df = pd.read_csv(raw_data_folder() / 'calendar.csv', parse_dates=['date'])
    print(df.dtypes)
    dataframe_to_table(df=df, table='calendar', if_exists='replace')


def import_sales_prices():
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
    print(f'import_sales took {round(end - start)} seconds')



#%%

import_calendar()
print('calendar imported')
import_sales_prices()
print('prices imported')

#%%

import time
start = time.time()
import_sales_prices()
end = time.time()
print(f'insert took {round(end-start)} seconds')
#%%

from generics.postgres import execute_sql_from_file, execute_sql

execute_sql('drop table if exists  sales')
execute_sql_from_file('sales_table')

#%%

from generics.postgres import execute_sql_from_file, execute_sql

execute_sql('drop table if exists item_info')
execute_sql_from_file('item_info_table')

#%%
execute_sql('drop table sell_prices')

#%%

from generics.postgres import get_connection
from generics.postgres import dataframe_to_table, execute_sql_from_file, execute_sql
import time
start = time.time()

execute_sql('drop table if exists prices')
execute_sql_from_file('prices_table')

conn = get_connection()
cur = conn.cursor()
from generics.file_locations import raw_data_folder

with open(raw_data_folder() / 'sell_prices.csv', 'r') as f:
    f.readline()
    cur.copy_from(file=f, table='prices', sep=',')

end = time.time()
print(f'insert took {round(end-start)} seconds')

#%%

from generics.postgres import dataframe_from_sql

df = dataframe_from_sql('select * from calendar limit 100')