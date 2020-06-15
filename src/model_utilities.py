from datetime import datetime, timedelta
import pandas as pd
from generics.postgres import dataframe_to_table_bulk, execute_sql, dataframe_from_sql, execute_sql_from_file


START_TRAIN = datetime(year=2014, month=3, day=1)
END_TRAIN = datetime(year=2014, month=7, day=1)
START_TEST = datetime(year=2014, month=7, day=2)
END_TEST = datetime(year=2014, month=7, day=10)

START_VALIDATION = datetime(year=2014, month=8, day=1)
VALIDATION_LENGTH = 60


def write_validation_results_to_db(model,
                                   model_name,
                                   size=10000,
                                   numeric_only=False):
    execute_sql_from_file('validation_table')
    [val_x, val_y, ids] = collect_features(data_set='validation', size=size, numeric_only=numeric_only)
    pred_values = model.predict(val_x)
    predictions = pd.DataFrame(data={'id': ids['id'], 'predicted': pred_values, 'date': ids['date']})
    predictions['model_name'] = model_name

    dataframe_to_table_bulk(df=predictions[['model_name', 'date', 'id', 'predicted']], table='validation')


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
        return collect_from_train(size=size, numeric_only=numeric_only, start_date=START_TRAIN, end_date=END_TRAIN)
    if data_set == 'test':
        return collect_from_train(size=size, numeric_only=numeric_only, start_date=START_TEST, end_date=END_TEST)
    if data_set == 'validation':
        end_date = START_VALIDATION + timedelta(days=VALIDATION_LENGTH)
        return collect_from_train(size=size, numeric_only=numeric_only, start_date=START_VALIDATION, end_date=end_date)


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
    y = df['target']
    if numeric_only:
        x = df[[col for col in df.select_dtypes('number').columns if col != 'target']]
    else:
        x = df.drop(['id', 'target', 'date'], axis='columns')
    return x, y, df[['id', 'date']]