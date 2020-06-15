from generics.postgres import execute_sql, execute_sql_from_file

execute_sql_from_file('validation_table')
sql = "DELETE FROM validation where model_name = 'quantity_last_7'"
execute_sql(sql)

#%%

from datetime import timedelta

from generics.postgres import execute_sql
from model_utilities import VALIDATION_START_DATE, VALIDATION_LENGTH


validation_end_date = VALIDATION_START_DATE + timedelta(days=VALIDATION_LENGTH-1)

sql = f"""
insert into validation 
select
'quantity_last_7' as model_name
,train.date
,train.id
,train.quantity_last_7 / 7 as predicted
from
    train
where date between '{VALIDATION_START_DATE:%Y-%m-%d}' and '{validation_end_date:%Y-%m-%d}'
"""
execute_sql(sql)

#%%

from datetime import timedelta

from generics.postgres import execute_sql
from model_utilities import VALIDATION_START_DATE, VALIDATION_LENGTH


validation_end_date = VALIDATION_START_DATE + timedelta(days=VALIDATION_LENGTH-1)

sql = f"""
insert into validation 
select
'weighted_quantity' as model_name
,train.date
,train.id
,train.quantity_last_7 / 21 + train.quantity_last_3 / 9 + train.quantity_last_21 / 63 as predicted
from
    train
where date between '{VALIDATION_START_DATE:%Y-%m-%d}' and '{validation_end_date:%Y-%m-%d}'
"""
execute_sql(sql)
