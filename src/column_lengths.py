import pandas as pd

from generics.file_locations import raw_data_folder


df = pd.read_csv(raw_data_folder() / 'sales_train_validation.csv')

for column_name in ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']:
    print(f"column {column_name} has max length {max(df[column_name].str.len())}")

#%%