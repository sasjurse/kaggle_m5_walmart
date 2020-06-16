from generics.postgres import dataframe_from_sql, execute_sql, execute_sql_from_file
from lightgbm import LGBMRegressor
from model_utilities import collect_features, write_validation_results_to_db, get_rmse

import optuna


# 1. Define an objective function to be maximized.
def objective(trial):
    model_name = 'optuna'

    params = {'n_estimators': 2000,
              'learning_rate':  trial.suggest_uniform('feature_fraction', 0.005, 0.04),
              'objective': 'tweedie',
              'early_stopping_rounds': 100,
              'feature_fraction': trial.suggest_uniform('feature_fraction', 0.4, 1.0),
              'bagging_fraction': trial.suggest_uniform('bagging_fraction', 0.4, 1.0),
              'min_child_samples': trial.suggest_int('min_child_samples', 5, 100)
              }

    model = LGBMRegressor(verbose=1, **params)

    [x, y, ids] = collect_features(data_set='train', size=400000, numeric_only=True)
    [test_x, test_y, ids] = collect_features(data_set='test', size=100000, numeric_only=True)

    model.fit(x, y, eval_set=(test_x, test_y))

    write_validation_results_to_db(model=model, model_name=model_name, params=str(params), numeric_only=True)

    score = get_rmse(model_name=model_name)

    return score


# 3. Create a study object and optimize the objective function.
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=20)

#%%

print(study.best_params)