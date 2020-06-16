from model_utilities import collect_features, write_validation_results_to_db, get_rmse

import optuna


def eval_model(model, model_name, params, numeric_only=False):
    assert isinstance(model_name, str), 'model_name should be a string'
    assert isinstance(params, dict), 'params should be a dict'

    [x, y, ids] = collect_features(data_set='train', size=8000, numeric_only=numeric_only)
    [test_x, test_y, ids] = collect_features(data_set='test', size=8000, numeric_only=numeric_only)

    model.fit(x, y, eval_set=(test_x, test_y))

    write_validation_results_to_db(model=model, model_name=model_name, params=str(params), numeric_only=numeric_only)

    score = get_rmse(model_name=model_name)

    return score

#%%

from generics.postgres import create_sa_string
from catboost import CatBoostRegressor


def objective(trial):
    params = dict(cat_features=['weekday', 'dept_id', 'state_id', 'store_id'],
                  loss_function='RMSE',
                  learning_rate=trial.suggest_uniform('learning_rate', 0.001, 0.01),
                  iterations=5000,
                  random_strength=trial.suggest_uniform('random_strength', 1, 3),
                  min_data_in_leaf=trial.suggest_int('min_child_samples', 5, 100))

    model = CatBoostRegressor(verbose=True, **params)

    score = eval_model(model=model, model_name='CatBoost', params=params)
    return score


study = optuna.create_study(direction='minimize',
                            study_name='CatBoost',
                            storage=create_sa_string(database='optuna'),
                            load_if_exists=True)

study.optimize(objective, n_trials=5)
