import pandas as pd

from generics.file_locations import raw_data_folder
from generics.postgres import dataframe_to_table, execute_sql_from_file, execute_sql

#%%


def import_calendar():
    df = pd.read_csv(raw_data_folder() / 'calendar.csv', parse_dates=['date'])
    print(df.dtypes)
    dataframe_to_table(df=df, table='calendar', if_exists='replace')


def import_sales_prices():
    execute_sql('drop table if exists prices')
    execute_sql_from_file('prices_table')
    df = pd.read_csv(raw_data_folder() / 'sell_prices.csv')
    print(df.dtypes)
    dataframe_to_table(df=df, table='prices', if_exists='append')



#%%

import_calendar()
import_sales_prices()

#%%

from generics.postgres import execute_sql
from generics.file_locations import sql_folder

with open(sql_folder()/'sales_table.sql', 'r') as f:
    rrr = f.read()

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