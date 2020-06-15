from src.generics.postgres import dataframe_from_sql
from catboost import CatBoostRegressor
from datetime import datetime
from src.model_utilities import START_TRAIN, END_TRAIN, write_validation_results_to_db

start_train = START_TRAIN
end_train = END_TRAIN

sql = f"""
select 
* 
from train 
where date between '{start_train:%Y-%m-%d}' and '{end_train:%Y-%m-%d}'
order by random() 
limit 600000
"""

df = dataframe_from_sql(sql)

df_val = dataframe_from_sql(f"select * from train where date between '2014-07-02' and '2014-07-25' order by random() limit 100000")
df_val_y = df_val['target']
df_val_x = df_val.drop(['id', 'target', 'date'], axis='columns')

model = CatBoostRegressor(verbose=True,
                          cat_features=['weekday', 'dept_id', 'state_id', 'store_id'],
                          loss_function='RMSE',
                          learning_rate=0.002,
                          iterations=5000,
                          random_strength=2,
                          min_data_in_leaf=20
                          )

target = df['target']
train_set = df.drop(['id', 'target', 'date'], axis='columns')
# train the model
model.fit(train_set, target, eval_set=(df_val_x, df_val_y))

print(train_set.columns)

yolo = model.get_feature_importance(prettified=True)

write_validation_results_to_db(model=model, model_name='CatBoost_5')


#%%

from src.generics.postgres import execute_sql
execute_sql('drop table validation')

#%%

from model_utilities import get_daily_rmse

df_cb = get_daily_rmse('CatBoost')

#%%
