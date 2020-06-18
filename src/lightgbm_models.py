from generics.postgres import execute_sql, execute_sql_from_file
from lightgbm import LGBMRegressor
from model_utilities import collect_features, write_validation_results_to_db
import pandas as pd

model_name = 'LGBM_1200'


params = {'feature_fraction': 0.58,
          'bagging_fraction': 0.47,
          'n_estimators': 4000,
          'learning_rate': 0.0285,
          'objective': 'tweedie',
          'early_stopping_rounds': 100,
          'min_child_samples': 5
          }


model = LGBMRegressor(verbose=1, **params)

[x, y, ids] = collect_features(data_set='train', size=12000000, numeric_only=True)
print('number of rows', len(x))
[test_x, test_y, ids] = collect_features(data_set='test', size=100000, numeric_only=True)


model.fit(x, y, eval_set=(test_x, test_y))

write_validation_results_to_db(model=model, model_name=model_name, params=str(params), numeric_only=True)

#%%
import pandas as pd
print(model_name)
importance = pd.DataFrame(data={'feature': x.columns, 'importance': model.feature_importances_})
importance.sort_values(by='importance', inplace=True)
print(importance)

#%%

from generics.postgres import dataframe_from_sql, execute_sql, execute_sql_from_file
from lightgbm import LGBMRegressor
from model_utilities import collect_features, write_validation_results_to_db


model_name = 'LGBM_100'

params = {'feature_fraction': 0.58,
          'bagging_fraction': 0.47,
          'n_estimators': 4000,
          'learning_rate': 0.0285,
          'objective': 'tweedie',
          'early_stopping_rounds': 100,
          'min_child_samples': 5
          }


model = LGBMRegressor(verbose=1, **params)

[x, y, ids] = collect_features(data_set='train', size=100000, numeric_only=True)
[test_x, test_y, ids] = collect_features(data_set='test', size=100000, numeric_only=True)

model.fit(x, y, eval_set=(test_x, test_y))
print('helli')
print(str(params))

write_validation_results_to_db(model=model, model_name=model_name, params=str(params),  numeric_only=True)

#%%

from generics.postgres import dataframe_from_sql, execute_sql, execute_sql_from_file
from lightgbm import LGBMRegressor
from model_utilities import collect_features, write_validation_results_to_db, get_categorical_columns
from sklearn.preprocessing import OrdinalEncoder

model_name = 'LGBM_cat'

params = {'feature_fraction': 0.58,
          'bagging_fraction': 0.47,
          'n_estimators': 4000,
          'learning_rate': 0.0285,
          'objective': 'tweedie',
          'early_stopping_rounds': 100,
          'min_child_samples': 5
          }

model = LGBMRegressor(verbose=1, **params)

[x, y, ids] = collect_features(data_set='train', size=400000, numeric_only=False)
[test_x, test_y, ids] = collect_features(data_set='test', size=100000, numeric_only=False)


model.fit(x, y, eval_set=(test_x, test_y), categorical_feature=get_categorical_columns(x))
print(str(params))

write_validation_results_to_db(model=model, model_name=model_name, params=str(params),  numeric_only=False)

#%%

from generics.postgres import dataframe_from_sql, execute_sql, execute_sql_from_file
from lightgbm import LGBMRegressor
from model_utilities import collect_features, write_validation_results_to_db


model_name = 'LGBM_diff'


params = {'sub_feature': 0.9,
          'n_estimators': 4000,
          'learning_rate': 0.01,
          'objective': 'tweedie',
          'early_stopping_rounds': 100,
          'max_depth': 5,
          'subsample': 0.7
          }


model = LGBMRegressor(verbose=1, **params)


[x, y, ids] = collect_features(data_set='train', size=900000, numeric_only=True)
[test_x, test_y, ids] = collect_features(data_set='test', size=100000, numeric_only=True)

model.fit(x, y, eval_set=(test_x, test_y))

write_validation_results_to_db(model=model, model_name=model_name,  params=str(params), numeric_only=True)

#%%
