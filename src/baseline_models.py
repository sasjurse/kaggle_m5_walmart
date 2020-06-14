from src.generics.postgres import execute_sql

sql = "DELETE FROM validation where model_name = 'quantity_last_7'"
execute_sql(sql)

#%%

from datetime import timedelta

from src.generics.postgres import execute_sql
from src.model_utilities import VALIDATION_START_DATE, VALIDATION_LENGTH


validation_end_date = VALIDATION_START_DATE + timedelta(days=VALIDATION_LENGTH-1)

sql = f"""
insert into validation 
select
'quantity_last_7' as model_name
,train.date
,train.id
,train.quantity_last_7 as predicted
from
    train
where date between '{VALIDATION_START_DATE:%Y-%m-%d}' and '{validation_end_date:%Y-%m-%d}'
"""
execute_sql(sql)