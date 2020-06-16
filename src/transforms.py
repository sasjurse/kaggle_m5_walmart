from src.generics.postgres import execute_sql, dataframe_from_sql, execute_sql_from_file


def sales_ext():
    execute_sql('drop view if exists sales_ext')
    execute_sql_from_file('sales_ext_view')


def sales_by_day():
    execute_sql('drop table if exists sales_by_day')
    execute_sql_from_file('sales_by_day')


def snap_info():
    execute_sql('drop table if exists snap_info')
    execute_sql_from_file('snap_info_table')


def weekday_averages():
    execute_sql('drop table if exists weekday_average')
    execute_sql_from_file('weekday_average_table')


def snap_influence():
    execute_sql('drop table if exists snap_influence')
    execute_sql_from_file('snap_influence_table')


def model_info():
    execute_sql('drop table if exists model_info')
    execute_sql_from_file('model_info')


def price_changes():
    execute_sql('drop table if exists price_changes')
    execute_sql_from_file('price_changes_table')


def lags():
    execute_sql('drop table if exists lags')
    execute_sql_from_file('lags')


def train():
    execute_sql('drop table if exists train')
    execute_sql_from_file('train_table')


if __name__ == '__main__':
    sales_ext()
    sales_by_day()
    snap_info()
    weekday_averages()
    snap_influence()
    price_changes()
    lags()
    train()
    model_info()
