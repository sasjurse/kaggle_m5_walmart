from generics.postgres import dataframe_from_sql, execute_sql, execute_sql_from_file
from catboost import CatBoostRegressor
from datetime import datetime
from model_utilities import collect_features, write_validation_results_to_db


execute_sql_from_file('validation_table')
sql = "DELETE FROM validation where model_name = 'CatBoost'"
execute_sql(sql)

[test_x, test_y, ids] = collect_features(data_set='test', size=400000, numeric_only=False)
[x, y, ids] = collect_features(data_set='train', size=40000, numeric_only=False)

model = CatBoostRegressor(verbose=True,
                          cat_features=['weekday', 'dept_id', 'state_id', 'store_id'],
                          loss_function='RMSE',
                          learning_rate=0.002,
                          iterations=5000,
                          random_strength=2,
                          min_data_in_leaf=20
                          )

# train the model
model.fit(x, y, eval_set=(test_x, test_y))

yolo = model.get_feature_importance(prettified=True)

write_validation_results_to_db(model=model, model_name='CatBoost', numeric_only=False)


#%%

from model_utilities import get_daily_rmse

df_cb = get_daily_rmse('CatBoost')
print(df_cb)

#%%
