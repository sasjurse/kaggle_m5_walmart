from src.generics.postgres import dataframe_from_sql, execute_sql, execute_sql_from_file
from lightgbm import LGBMRegressor
from datetime import datetime
from src.model_utilities import collect_features, write_validation_results_to_db


execute_sql_from_file('validation_table')
sql = "DELETE FROM validation where model_name = 'LGBM'"
execute_sql(sql)


params = {'sub_feature': 0.9,
          'n_estimators': 4000,
          'learning_rate': 0.02,
          'objective': 'tweedie',
          'early_stopping_rounds': 100
          }

[test_x, test_y, ids] = collect_features(data_set='test', size=400000, numeric_only=True)
model = LGBMRegressor(verbose=1, **params)

[x, y, ids] = collect_features(data_set='train', size=20000, numeric_only=True)

model.fit(x, y, eval_set=(test_x, test_y))

write_validation_results_to_db(model=model, model_name='LGBM', numeric_only=True, size=100000)

#%%

hmm = model.best_iteration_