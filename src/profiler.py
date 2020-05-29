import pandas as pd
from pandas_profiling import ProfileReport

from generics import file_locations


def profile_csv(input_file: str):
    df = pd.read_csv(file_locations.raw_data_folder() / f'{input_file}.csv')
    profile = ProfileReport(df, title=f"{input_file}")
    profile.to_file(file_locations.plots_folder() / f'{input_file}.html')


if __name__ == '__main__':
    profile_csv('calendar')
    profile_csv('sales_train_validation')
    profile_csv('sample_submission')
    profile_csv('sell_prices')
