import optuna
from catboost import CatBoostRegressor

from generics.postgres import dataframe_from_sql, execute_sql, execute_sql_from_file, create_sa_string

7
from datetime import datetime
from model_utilities import collect_features, write_validation_results_to_db, eval_model

execute_sql_from_file('validation')
sql = "DELETE FROM validation where model_name = 'CatBoost'"
execute_sql(sql)

train_size = 800000

[test_x, test_y, ids] = collect_features(data_set='test', size=100000, numeric_only=False)
[x, y, ids] = collect_features(data_set='train', size=train_size, numeric_only=False)

params = dict(cat_features=['wday', 'dept_id', 'state_id', 'store_id', 'snap_status'],
              loss_function='RMSE',
              learning_rate=0.002,
              iterations=5000,
              random_strength=2,
              min_data_in_leaf=20)

model = CatBoostRegressor(verbose=True, **params)

# train the model
model.fit(x, y, eval_set=(test_x, test_y))

yolo = model.get_feature_importance(prettified=True)

write_validation_results_to_db(model=model, model_name='CatBoost', params=str(params), train_size=train_size,
                               numeric_only=False)


#%%

from model_utilities import get_daily_rmse

df_cb = get_daily_rmse('CatBoost')
print(df_cb)

#%%
def cat_boost_objective(trial):
    params = dict(cat_features=['weekday', 'dept_id', 'state_id', 'store_id'],
                  loss_function='RMSE',
                  learning_rate=trial.suggest_uniform('learning_rate', 0.01, 0.2),
                  iterations=3000,
                  depth=trial.suggest_int('depth', 6, 12),
                  random_strength=trial.suggest_uniform('random_strength', 1, 3),
                  min_data_in_leaf=trial.suggest_int('min_child_samples', 5, 100))

    model = CatBoostRegressor(verbose=True, **params)

    score = eval_model(model=model, model_name='CatBoost_3', params=params)
    return score


study = optuna.create_study(direction='minimize',
                            study_name='CatBoost_3',
                            storage=create_sa_string(database='optuna'),
                            load_if_exists=True)