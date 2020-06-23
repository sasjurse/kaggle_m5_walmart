import optuna
from lightgbm import LGBMRegressor
from model_utilities import eval_lgbm_model, get_categorical_columns
import pandas as pd
from generics.postgres import dataframe_from_sql, execute_sql, execute_sql_from_file, create_sa_string


def objective(trial):

    params = {'feature_fraction': trial.suggest_uniform('feature_fraction', 0.3, 0.8),
              'bagging_fraction': trial.suggest_uniform('bagging_fraction', 0.4, 0.7),
              'n_estimators':  trial.suggest_categorical('n_trees', [1000, 3000, 6000, 9000]),
              'learning_rate': trial.suggest_uniform('learning_rate', 0.001, 0.05),
              'objective': trial.suggest_categorical('objective', ['tweedie', 'poisson']),
              'early_stopping_rounds': 100,
              'lambda_l1': trial.suggest_int('lambda_l1', 0, 1),
              }

    train_size = 3000000

    model = LGBMRegressor(verbose=1, **params)

    score = eval_lgbm_model(model, 'LGBM optuna 8', params=params, train_size=train_size,
                            fit_params={'verbose': False, 'early_stopping_rounds': 100})

    return score


study = optuna.create_study(direction='minimize',
                            study_name='LGBM_optuna_8',
                            storage=create_sa_string(database='optuna'),
                            load_if_exists=True)

study.optimize(objective, n_trials=100)

#%%