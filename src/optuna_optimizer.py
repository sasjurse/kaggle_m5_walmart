from model_utilities import collect_features, write_validation_results_to_db, get_rmse

import optuna


def eval_model(model, model_name, params):
    [x, y, ids] = collect_features(data_set='train', size=8000, numeric_only=True)
    [test_x, test_y, ids] = collect_features(data_set='test', size=8000, numeric_only=True)

    model.fit(x, y, eval_set=(test_x, test_y))

    write_validation_results_to_db(model=model, model_name=model_name, params=str(params), numeric_only=True)

    score = get_rmse(model_name=model_name)

    return score

#%%


from generics.postgres import create_sa_string


study = optuna.create_study(direction='minimize',
                            study_name='CatBoost',
                            storage=create_sa_string(database='optuna'),
                            load_if_exists=True)

#%%
study.optimize(objective, n_trials=5)