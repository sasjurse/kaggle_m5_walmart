from datetime import datetime, timedelta
import pandas as pd
from generics.postgres import dataframe_to_table_bulk, execute_sql, dataframe_from_sql, execute_sql_from_file


START_TRAIN = datetime(year=2014, month=3, day=1)
END_TRAIN = datetime(year=2014, month=7, day=1)
VALIDATION_START_DATE = datetime(year=2014, month=8, day=1)
VALIDATION_LENGTH = 60


def write_validation_results_to_db(model,
                                   model_name,
                                   validation_start_date=VALIDATION_START_DATE,
                                   validation_length=VALIDATION_LENGTH,
                                   daily_test_size=10000):
    execute_sql_from_file('validation_table')
    for dt in [validation_start_date + timedelta(days=x) for x in range(0, validation_length)]:
        sql = f"""
        select * from train 
        where date = '{dt:%Y-%m-%d}' 
        order by random() limit {daily_test_size}"""

        df = dataframe_from_sql(sql)
        val_x = df.drop(['id', 'target', 'date'], axis='columns')
        pred_values = model.predict(val_x)
        predictions = pd.DataFrame(data={'id': df['id'], 'predicted': pred_values, 'date': df['date']})
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


def retrieve_train_set(size=10000, numeric_only=False, start_train = START_TRAIN, end_train = END_TRAIN):
    sql = f"""
    select 
    * 
    from train 
    where date between '{start_train:%Y-%m-%d}' and '{end_train:%Y-%m-%d}'
    order by random() 
    limit {size}
    """
    df = dataframe_from_sql(sql)
    y = df['target']
    if numeric_only:
        x = df[[col for col in df.select_dtypes('number').columns if col != 'target']]
    else:
        x = df.drop(['id', 'target', 'date'], axis='columns')
    return x, y
