from generics.postgres import dataframe_from_sql

#%%
from generics.postgres import dataframe_from_sql

sql = """
select 
validation.model_name
,SQRT(AVG(POWER((train.target - validation.predicted),2))) as rmse
,avg(train.target - validation.predicted) as Error
from
train
inner join validation on train.date = validation.date and validation.id = train.id
group by 1
order by 2 desc"""


df_totals = dataframe_from_sql(sql)

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
where validation.model_name = 'CatBoost_5'
group by 1,2,3,4,5
order by 4,2 desc"""


df_long = dataframe_from_sql(sql)

#%%

calendar = dataframe_from_sql('select * from calendar order by date')


#%%
from generics.postgres import dataframe_from_sql

sql = """
select 
validation.model_name
,weekday
,SQRT(AVG(POWER((train.target - validation.predicted),2))) as rmse
,avg(train.target - validation.predicted) as Error
from
train
inner join validation on train.date = validation.date and validation.id = train.id
group by 1,2
order by 1 desc"""


df_weekday = dataframe_from_sql(sql)