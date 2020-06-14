import pandas as pd
from pandas_profiling import ProfileReport

from generics import file_locations, postgres

#%%


def profile_csv(input_file: str, minimal=False):
    df = pd.read_csv(file_locations.raw_data_folder() / f'{input_file}.csv')
    profile = ProfileReport(df, title=f"{input_file}", minimal=minimal)
    profile.to_file(file_locations.plots_folder() / f'{input_file}.html')

profile_csv('calendar')
profile_csv('sales_train_validation', minimal=True)
profile_csv('sample_submission')
profile_csv('sell_prices', minimal=True)

#%%


def profile_train():
    input_file = 'train_heavy'
    df = postgres.dataframe_from_sql('select * from train order by random() limit 50000')
    profile = ProfileReport(df, title=f"{input_file}")
    profile.to_file(file_locations.plots_folder() / f'{input_file}.html')

profile_train()
#%%

if __name__ == '__main__':
    profile_csv('calendar')
    profile_csv('sales_train_validation', minimal=True)
    profile_csv('sample_submission')
    profile_csv('sell_prices', minimal=True)
