from src.generics.postgres import dataframe_from_sql
from catboost import CatBoostRegressor
from datetime import datetime

dt = datetime(year=2014, month=7, day=1)

df = dataframe_from_sql(f"select * from train where date < '{dt:%Y-%m-%d}' order by random() limit 400000")

df_val = dataframe_from_sql(f"select * from train where date between '2014-07-02' and '2014-07-25' order by random() limit 100000")
df_val_y = df_val['target']
df_val_x = df_val.drop(['id', 'target', 'date'], axis='columns')

model = CatBoostRegressor(verbose=True,
                          cat_features=['weekday', 'dept_id', 'state_id', 'store_id'],
                          loss_function='RMSE',
                          learning_rate=0.005,
                          iterations=1200,
                          random_strength=2,
                          min_data_in_leaf=10
                          )

target = df['target']
train_set = df.drop(['id', 'target', 'date'], axis='columns')
# train the model
model.fit(train_set, target, eval_set=(df_val_x, df_val_y))

print(train_set.columns)

yolo = model.get_feature_importance(prettified=True)

#%%

from datetime import datetime, timedelta
import pandas as pd
from src.generics.postgres import dataframe_to_table, execute_sql

execute_sql('drop table if exists validation')

start_date = datetime(year=2014, month=10, day=10)
for dt in [start_date+timedelta(days=x) for x in range(0, 7)]:
    df = dataframe_from_sql(f"select * from train where date < '{dt:%Y-%m-%d}' order by random() limit 25000")
    val_set = df.drop(['id', 'target', 'date'], axis='columns')
    pred_values = model.predict(val_set)
    predictions = pd.DataFrame(data={'id': df['id'], 'predicted': pred_values})
    predictions['date'] = dt

    dataframe_to_table(df=predictions, table='validation')


#%%

from src.generics.postgres import dataframe_from_sql

sql = """
select 
train.date
,SQRT(AVG(POWER((train.target - validation.predicted),2))) as RMSE
from
train
inner join validation on train.date = validation.date and validation.id = train.id
group by 1
order by 1 desc
"""

df_rmse = dataframe_from_sql(sql)

#%%

from src.generics.postgres import dataframe_from_sql

sql = """
select 
train.date
,SQRT(AVG(POWER((train.target - train.quantity_last_7/7),2))) as RMSE
from
train
inner join validation on train.date = validation.date and validation.id = train.id
group by 1
order by 1 desc
"""

df_rmse2 = dataframe_from_sql(sql)

#%%


sql = """
select 
train.*
,validation.predicted
from
train
inner join validation on train.date = validation.date and validation.id = train.id
order by train.date, train.id desc limit 2500
"""


df_test = dataframe_from_sql(sql)