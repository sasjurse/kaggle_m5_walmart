import pandas as pd

from generics.file_locations import raw_data_folder
from generics.postgres import dataframe_to_table_bulk, execute_sql, execute_sql_from_file

import time


def upload_day_of_sales(label: str, sales: pd.DataFrame, posting_date):
    core_columns = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']

    df_sales_one_day = sales[core_columns + [label]]

    df_sales_one_day['posting_date'] = posting_date

    df_sales_one_day.rename({label: 'quantity'}, inplace=True, axis='columns')

    dataframe_to_table_bulk(df_sales_one_day, 'sales_ext')


def upload_sales():
    start = time.time()

    df = pd.read_csv(raw_data_folder() / 'sales_train_validation.csv')
    calendar = pd.read_csv(raw_data_folder() / 'calendar.csv')

    execute_sql('drop table if exists sales_ext')
    execute_sql_from_file('sales_ext_table')

    for index, row in calendar.sample(10).iterrows():
        label = row['d']
        date = row['date']

        upload_day_of_sales(label=label, sales=df, posting_date=date)
        print(label)


    end = time.time()
    print(f'dataframe_to_table took {round(end-start)} seconds')

#%%

import cProfile
import re
cProfile.run(upload_sales())

#%%

upload_sales()
#%%

for index, row in calendar.iterrows():
    print(row['d'])
    print(row['date'])


#%%
df.sample(5).to_csv('yolo.csv', sep=',', date_format='%Y-%m-%d', index=False)

#%%
dateff = dates.query('d==@label').iloc[0, 0]


df1['posting_date'] = dateff

df1.rename({label: 'amount'}, inplace=True, axis='columns')

#%%

from generics.postgres import dataframe_to_table

dataframe_to_table(df1, 'sales')

#%%

from generics.postgres import dataframe_from_sql

df2 = dataframe_from_sql('select * from sales')

#%%

import pandas as pd

from generics.file_locations import raw_data_folder
from generics.postgres import dataframe_to_table_bulk, execute_sql, execute_sql_from_file

import time


df = pd.read_csv(raw_data_folder() / 'sales_train_validation.csv')


#%%

column_name = 'id'

max(df[column_name].str.len())

#%%

df2 = pd.melt(df, id_vars=['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id'])


#%%
execute_sql('drop table if exists sales_ext')
execute_sql_from_file('sales_ext_table')

dataframe_to_table_bulk(df2, 'sales_ext')

#%%

execute_sql('drop table if exists sales_ext')