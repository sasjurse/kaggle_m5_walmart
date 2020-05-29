import pandas as pd
import os
from pathlib import Path

import generics.postgres
#%%


def raw_data_folder():
    return Path('./raw_data')


df = pd.read_csv(raw_data_folder() / 'calendar.csv', parse_dates=['date'])
print(df.dtypes)

#%%

from generics.postgres import create_sa_engine

engine = create_sa_engine()

#%%

from generics.postgres import dataframe_to_table

dataframe_to_table(df=df, table='calendar')

#%%

if __name__ == '__main__':
    print(os.environ['POSTGRES_SERVICE_HOST'])
