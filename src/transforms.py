from src.generics.postgres import execute_sql, dataframe_from_sql, execute_sql_from_file


def sales_ext():
    execute_sql('drop view if exists sales_ext')
    execute_sql_from_file('sales_ext_view')


def sales_by_day():
    execute_sql('drop table if exists sales_by_day')
    execute_sql_from_file('sales_by_day')


if __name__ == '__main__':
    sales_ext()
    sales_by_day()
