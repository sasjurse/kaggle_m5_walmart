from src.generics.postgres import dataframe_from_sql
from catboost import CatBoostRegressor
from datetime import datetime

dt = datetime(year=2014, month=6, day=1)

df = dataframe_from_sql(f"select * from train where date < '{dt:%Y-%m-%d}' order by random() limit 100000")

model = CatBoostRegressor(verbose=True,
                          cat_features=['weekday', 'dept_id', 'state_id', 'store_id'],
                          loss_function='RMSE')

target = df['target']
train_set = df.drop(['id', 'target', 'date'], axis='columns')
# train the model
model.fit(train_set, target)

print(train_set.columns)

yolo = model.get_feature_importance(prettified=True)

#%%

for dt in


test =

#%%

from datetime import datetime, timedelta
import pandas as pd

start_date = datetime(year=2014, month=6, day=1)
for dt in [start_date+timedelta(days=x) for x in range(0,3)]:
    df = dataframe_from_sql(f"select * from train where date < '{dt:%Y-%m-%d}' order by random() limit 10000")
    val_set = df.drop(['id', 'target', 'date'], axis='columns')
    pred_values = model.predict(val_set)
    predictions = pd.DataFrame(data={'id': df['id'], 'predicted': pred_values})