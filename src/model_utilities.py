from datetime import datetime, timedelta
import logging
import pandas as pd
from generics.postgres import dataframe_to_table_bulk, dataframe_to_table, execute_sql, dataframe_from_sql, execute_sql_from_file
from generics.utilities import get_git_commit
import numpy as np

START_TRAIN = datetime(year=2013, month=1, day=15)
END_TRAIN = datetime(year=2013, month=6, day=1)
START_TEST = datetime(year=2013, month=6, day=2)
END_TEST = datetime(year=2013, month=6, day=10)

START_VALIDATION = datetime(year=2013, month=10, day=12)
VALIDATION_LENGTH = 60
VALIDATION_SIZE = 600000


def write_validation_results_to_db(model,
                                   model_name: str,
                                   params: str,
                                   train_size=np.nan,
                                   validation_size=VALIDATION_SIZE,
                                   numeric_only=False):

    execute_sql_from_file('validation')
    sql = f"DELETE FROM validation where model_name = '{model_name}'"
    execute_sql(sql)

    [val_x, val_y, ids] = collect_features(data_set='validation', size=validation_size, numeric_only=numeric_only)
    pred_values = model.predict(val_x)
    predictions = pd.DataFrame(data={'numeric_id': ids['numeric_id'],
                                     'predicted': pred_values,
                                     'date': ids['date'],
                                     'target': val_y})
    predictions['model_name'] = model_name

    dataframe_to_table_bulk(df=predictions[['model_name', 'date', 'numeric_id', 'predicted', 'target']],
                            table='validation')

    execute_sql_from_file('model_info')
    model_info = pd.DataFrame(data={'model_name': [model_name],
                                    'rmse': [get_rmse(model_name)],
                                    'created_at': [f"{datetime.now():%Y-%m-%d %H:%M}"],
                                    'params': [str(params)],
                                    'train_size': [train_size],
                                    'features': [", ".join(list(val_x))],
                                    'git_commit': [get_git_commit()]
                                    }
                              )
    dataframe_to_table(model_info, table='model_info')


def get_rmse(model_name: str):
    sql = f"""
with val_errors as (
select
validation.date
,validation.numeric_id
,POWER((validation.target - validation.predicted), 2) as pred_error
,ce.cum_mse
from 
    validation
inner join cum_errors as ce on validation.date=ce.date and validation.numeric_id=ce.numeric_id
where
validation.model_name = '{model_name}'

)
select
SQRT(AVG(pred_error/cum_mse)) as RMSE
from
val_errors
    """
    validation_error = dataframe_from_sql(sql).iloc[0, 0]
    logging.info(f'Validation error for {model_name} is {validation_error}')
    return validation_error


def get_daily_rmse(model_name: str):
    sql = f"""
    select
    train.date
    ,SQRT(AVG(POWER((train.target - validation.predicted),2))) as RMSE
    from
    train
    inner join validation on train.date = validation.date and validation.id = train.id
    where validation.model_name = '{model_name}'
    group by 1
    order by 1 desc
    """

    return dataframe_from_sql(sql)


def collect_features(data_set: str, size=10000, numeric_only=False):
    assert data_set in ['train', 'test', 'validation']
    if data_set == 'train':
        data = collect_from_train(size=size, numeric_only=numeric_only, start_date=START_TRAIN, end_date=END_TRAIN)
    elif data_set == 'test':
        data = collect_from_train(size=size, numeric_only=numeric_only, start_date=START_TEST, end_date=END_TEST)
    elif data_set == 'validation':
        end_date = START_VALIDATION + timedelta(days=VALIDATION_LENGTH)
        data = collect_from_train(size=size, numeric_only=numeric_only, start_date=START_VALIDATION, end_date=end_date)
    else:
        raise Exception('unknown data set')
    mem_usage = data[0].memory_usage().sum() / (1024 * 1024)
    logging.info(f"data set with features is {mem_usage} MB")
    return data


def collect_from_train(size=10000, numeric_only=False, start_date=START_TRAIN, end_date=END_TRAIN):
    sql = f"""
    select
    *
    from train
    where date between '{start_date:%Y-%m-%d}' and '{end_date:%Y-%m-%d}'
    order by random()
    limit {size}
    """
    df = dataframe_from_sql(sql)
    logging.info(f'Collected {len(df)} rows from train')

    y = df['target']
    if numeric_only:
        x = df[[col for col in df.select_dtypes('number').columns if col not in ['target', 'numeric_id', 'wday']]]
    else:
        x = df.drop(['numeric_id', 'target', 'date'], axis='columns')
        for c in get_categorical_columns(x):
            x[c] = x[c].astype('category')  # makes it easier for lightgbm
    return x, y, df[['numeric_id', 'date']]


def get_categorical_columns(df: pd.DataFrame):
    by_type = [col for col in df.columns if col not in df.select_dtypes(['number', 'datetime']).columns]
    return by_type + ['wday']


def eval_model(model, model_name, params, train_size=800000, numeric_only=False, fit_params=None):
    assert isinstance(model_name, str), 'model_name should be a string'
    assert isinstance(params, dict), 'params should be a dict'

    [x, y, ids] = collect_features(data_set='train', size=train_size, numeric_only=numeric_only)
    del ids
    [test_x, test_y, ids] = collect_features(data_set='test', size=100000, numeric_only=numeric_only)
    del ids

    if fit_params:
        model.fit(x, y, eval_set=(test_x, test_y), **fit_params)
    else:
        model.fit(x, y, eval_set=(test_x, test_y))

    write_validation_results_to_db(model=model, model_name=model_name, params=str(params), numeric_only=numeric_only)

    score = get_rmse(model_name=model_name)

    return score
