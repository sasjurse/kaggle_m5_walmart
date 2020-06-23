from generics.postgres import dataframe_from_sql

#%%
from generics.postgres import dataframe_from_sql

from generics.postgres import dataframe_from_sql

sql = """
select 
validation.model_name
,calendar.date
,calendar.event_name_1
,SQRT(AVG(POWER((target - validation.predicted),2))) as rmse
,avg(target - predicted) as Error
from
validation
inner join calendar on validation.date = calendar.date
group by 1,2,3
order by 1,2 desc"""


df_long = dataframe_from_sql(sql)

#%%

sql = """
select 
validation.model_name
,train.date
,train.snap_status
,train.store_id
,train.weekday
,SQRT(AVG(POWER((train.target - validation.predicted),2))) as rmse
,avg(train.target - validation.predicted) as Error
from
train
inner join validation on train.date = validation.date and validation.id = train.id
where validation.model_name = 'LGBM_1200'
group by 1,2,3,4,5
order by 4,2 desc"""


df_long = dataframe_from_sql(sql)

#%%

from generics.postgres import execute_sql
calendar = execute_sql('delete from model_info')


#%%
from generics.postgres import dataframe_from_sql

sql = """
select 
validation.model_name
,calendar.weekday
,SQRT(AVG(POWER((target - validation.predicted),2))) as rmse
,avg(target - predicted) as Error
from
validation
inner join calendar on validation.date = calendar.date
group by 1,2
order by 1 desc"""


df_weekday = dataframe_from_sql(sql)

#%%
from generics.postgres import dataframe_from_sql
df_mi = dataframe_from_sql('select model_name, rmse, created_at from model_info order by 2 desc')

#%%

from generics.postgres import dataframe_from_sql
df_mi = dataframe_from_sql('select * from model_info order by rmse desc')

#%%


from generics.postgres import sql_to_csv, dataframe_from_sql
from generics.file_locations import logs_folder
from datetime import datetime

fn = logs_folder() / f"{datetime.now():%Y-%m-%d_%H_%M}_train_results.csv"
sql_to_csv('select * from model_info', fn)
