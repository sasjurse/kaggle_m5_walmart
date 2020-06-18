import optuna
from lightgbm import LGBMRegressor
from model_utilities import eval_model, get_categorical_columns
import pandas as pd
from generics.postgres import dataframe_from_sql, execute_sql, execute_sql_from_file, create_sa_string


def objective(trial):

    params = {'feature_fraction': trial.suggest_uniform('feature_fraction', 0.5, 0.7),
              'bagging_fraction': trial.suggest_uniform('bagging_fraction', 0.4, 0.7),
              'n_estimators': 3500,
              'learning_rate': trial.suggest_uniform('learning_rate', 0.01, 0.3),
              'objective': trial.suggest_categorical('objetive', ['tweedie', 'poisson']),
              'early_stopping_rounds': 100,
              'lambda_l1': trial.suggest_int('lambda_l1', 0, 1),
              'min_child_samples': trial.suggest_int('min_child_samples', 5, 100)
              }

    train_sample = dataframe_from_sql('select * from train limit 1')

    train_size = trial.suggest_int('train_size', 400000, 600000)
    params['train_size'] = train_size

    model = LGBMRegressor(verbose=1, **params)

    score = eval_model(model, 'LGBM optuna', params=params, train_size=train_size)

    return score


study = optuna.create_study(direction='minimize',
                            study_name='LGBM_optuna_2',
                            storage=create_sa_string(database='optuna'),
                            load_if_exists=True)

study.optimize(objective, n_trials=100)

#%%