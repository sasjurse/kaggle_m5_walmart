from generics.postgres import execute_sql, execute_sql_from_file
from lightgbm import LGBMRegressor
from model_utilities import collect_features, write_validation_results_to_db
import pandas as pd

model_name = 'LGBM_900'


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

train_size = 100000


#%%

model_name = 'LGBM_cat'

params = {'feature_fraction': 0.58,
          'bagging_fraction': 0.47,
          'n_estimators': 4000,
          'learning_rate': 0.0145,
          'objective': 'tweedie',
          'early_stopping_rounds': 100,
          'min_child_samples': 5
          }

train_size = 2000000

#%%

model_name = 'LGBM_diff'

params = {'feature_fraction': 0.4827903694720314,
          'bagging_fraction': 0.572260424947954,
          'n_estimators': 9000,
          'learning_rate': 0.12602389742331246,
          'objective': 'tweedie',
          'early_stopping_rounds': 100,
          'lambda_l1': 1
          }

train_size = 2000000
#%%

from generics.postgres import dataframe_from_sql, execute_sql, execute_sql_from_file
from lightgbm import LGBMRegressor
from model_utilities import collect_features, write_validation_results_to_db, get_categorical_columns

model = LGBMRegressor(verbose=-1, **params)

[x, y, ids] = collect_features(data_set='train', size=train_size, numeric_only=False)
[test_x, test_y, ids] = collect_features(data_set='test', size=100000, numeric_only=False)


model.fit(x, y, eval_set=(test_x, test_y),
          categorical_feature=get_categorical_columns(x),
          verbose=False,
          early_stopping_rounds=100)

print(f'Best iteration was {model.best_iteration_}')

write_validation_results_to_db(model=model,
                               model_name=model_name,
                               train_size=train_size,
                               params=str(params),
                               numeric_only=False)

#%%
import pandas as pd
print(model_name)
importance = pd.DataFrame(data={'feature': x.columns, 'importance': model.feature_importances_})
importance.sort_values(by='importance', inplace=True)
print(importance)

