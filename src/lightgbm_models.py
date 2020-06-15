from generics.postgres import execute_sql, execute_sql_from_file
from lightgbm import LGBMRegressor
from model_utilities import collect_features, write_validation_results_to_db

model_name = 'LGBM_600'

execute_sql_from_file('validation_table')
sql = f"DELETE FROM validation where model_name = '{model_name}'"
execute_sql(sql)


params = {'sub_feature': 0.9,
          'n_estimators': 4000,
          'learning_rate': 0.02,
          'objective': 'tweedie',
          'early_stopping_rounds': 100
          }


model = LGBMRegressor(verbose=1, **params)

[x, y, ids] = collect_features(data_set='train', size=600000, numeric_only=True)
[test_x, test_y, ids] = collect_features(data_set='test', size=100000, numeric_only=True)


model.fit(x, y, eval_set=(test_x, test_y))

write_validation_results_to_db(model=model, model_name=model_name, numeric_only=True, size=300000)

#%%

from src.generics.postgres import dataframe_from_sql, execute_sql, execute_sql_from_file
from lightgbm import LGBMRegressor
from datetime import datetime
from src.model_utilities import collect_features, write_validation_results_to_db


model_name = 'LGBM_100'

execute_sql_from_file('validation_table')
sql = f"DELETE FROM validation where model_name = '{model_name}'"
execute_sql(sql)



params = {'sub_feature': 0.9,
          'n_estimators': 4000,
          'learning_rate': 0.02,
          'objective': 'tweedie',
          'early_stopping_rounds': 100
          }


model = LGBMRegressor(verbose=1, **params)

[x, y, ids] = collect_features(data_set='train', size=100000, numeric_only=True)
[test_x, test_y, ids] = collect_features(data_set='test', size=100000, numeric_only=True)

model.fit(x, y, eval_set=(test_x, test_y))

write_validation_results_to_db(model=model, model_name=model_name, numeric_only=True, size=300000)

#%%

from src.generics.postgres import dataframe_from_sql, execute_sql, execute_sql_from_file
from lightgbm import LGBMRegressor
from datetime import datetime
from src.model_utilities import collect_features, write_validation_results_to_db


model_name = 'LGBM_diff'

execute_sql_from_file('validation_table')
sql = f"DELETE FROM validation where model_name = '{model_name}'"
execute_sql(sql)



params = {'sub_feature': 0.9,
          'n_estimators': 4000,
          'learning_rate': 0.01,
          'objective': 'tweedie',
          'early_stopping_rounds': 100,
          'max_depth': 5,
          'subsample': 0.7
          }


model = LGBMRegressor(verbose=1, **params)


[x, y, ids] = collect_features(data_set='train', size=400000, numeric_only=True)
[test_x, test_y, ids] = collect_features(data_set='test', size=400000, numeric_only=True)

model.fit(x, y, eval_set=(test_x, test_y))

write_validation_results_to_db(model=model, model_name=model_name, numeric_only=True, size=300000)
