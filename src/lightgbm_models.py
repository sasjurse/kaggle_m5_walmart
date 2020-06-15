from src.generics.postgres import dataframe_from_sql
from lightgbm import LGBMRegressor
from datetime import datetime
from src.model_utilities import retrieve_train_set, write_validation_results_to_db


sql = f"select * from train where date between '2014-07-02' and '2014-07-25' order by random() limit 5000"
df_val = dataframe_from_sql(sql)
df_val_y = df_val['target']
df_val_x = df_val[[col for col in df_val.select_dtypes('number').columns if col != 'target']]

model = LGBMRegressor(verbose=1)

[x, y] = retrieve_train_set(size=10000, numeric_only=True)

model.fit(x, y, eval_set=(df_val_x, df_val_y))

write_validation_results_to_db(model=model, model_name='LGBM')

#%%

