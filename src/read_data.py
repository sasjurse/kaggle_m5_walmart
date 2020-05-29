import pandas as pd

from generics.file_locations import raw_data_folder
from generics.postgres import dataframe_to_table

#%%


def import_calendar():
    df = pd.read_csv(raw_data_folder() / 'calendar.csv', parse_dates=['date'])
    print(df.dtypes)
    dataframe_to_table(df=df, table='calendar', if_exists='replace')


def import_sales_train_validation():
    df = pd.read_csv(raw_data_folder() / 'sales_train_validation.csv', parse_dates=['date'])
    print(df.dtypes)
    dataframe_to_table(df=df, table='sales', if_exists='replace')


#%%

import_calendar()
import_sales_train_validation()
