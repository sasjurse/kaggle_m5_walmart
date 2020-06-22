from generics.postgres import execute_sql, dataframe_from_sql

execute_sql('drop table if exists train')

sql = """
CREATE UNLOGGED TABLE train (
    numeric_id int
    ,date date
    ,wday smallint
    ,store_id text
    ,dept_id text
    ,state_id text
    ,snap_status boolean
    ,days_since_snap real
    ,avg_last_1 real
    ,avg_last_3 real
    ,avg_last_7 real
    ,avg_last_21 real
    ,max_last_21 real
    ,min_last_21 smallint 
    ,std_last_21 smallint
    ,max_last_42 real
    ,min_last_42 smallint
    ,avg_last_42 smallint
    ,relative_median real
    ,wa_adjusted_quantity_last_7 real
    ,sinf_relative_median real
    ,sinf_adjusted_quantity_last_7 real
    ,price_change_w1 numeric
    ,price_change_w3 numeric
    ,target smallint
    ,cum_mse real
) PARTITION BY RANGE (date);
"""

execute_sql(sql)



#%%

from generics.postgres import execute_sql, dataframe_from_sql

year = 2013
print('starting tmp_train')

execute_sql(f'drop table if exists tmp_train_{year}')

sql = f"""
create unlogged table tmp_train_{year} as
select
se.numeric_id
, se.date
, se.wday
, se.store_id
, se.dept_id
, se.state_id
, si.snap_status
, si.days_since_snap
, wa.relative_median
, pc.price_change_w1
, pc.price_change_w3
from sales_ext as se
inner join price_changes as pc on se.store_id = pc.store_id and se.item_id = pc.item_id and se.wm_yr_wk = pc.wm_yr_wk
inner join snap_info as si on se.state_id = si.state_id and si.date = se.date
inner join weekday_average as wa
    on se.wday = wa.wday and wa.dept_id = se.dept_id and wa.store_id = se.store_id
inner join snap_influence as sinf
    on se.dept_id = sinf.dept_id and se.store_id = sinf.store_id
        and sinf.snap_status = si.snap_status
where se.date between '{year}-01-01' and '{year}-12-31'
"""

execute_sql(sql)

#%%

from generics.postgres import execute_sql, dataframe_from_sql

year = 2013
execute_sql(f'drop table if exists train_{year}')


execute_sql(f"""
create unlogged table train_{year} partition of train
for values from ('{year}-01-01') to ('{year+1}-01-01') 
""")


#%%

sql = f"""
insert into train_{year} 
select
    tmp_train.numeric_id
    ,tmp_train.date
    ,tmp_train.wday
    ,tmp_train.store_id
    ,tmp_train.dept_id
    ,tmp_train.state_id
    ,tmp_train.snap_status
    ,tmp_train.days_since_snap
    ,lags.avg_last_1
    ,lags.avg_last_3
    ,lags.avg_last_7
    ,lags.avg_last_21
    ,lags.max_last_21
    ,lags.min_last_21
    ,lags.std_last_21
    ,lags.max_last_42
    ,lags.min_last_42
    ,lags.avg_last_42
    ,tmp_train.relative_median
    ,avg_last_7 * tmp_train.relative_median as wa_adjusted_quantity_last_7
    ,tmp_train.relative_median as sinf_relative_median
    ,avg_last_7 * tmp_train.relative_median as sinf_adjusted_quantity_last_7
    ,tmp_train.price_change_w1
    ,tmp_train.price_change_w3
    ,lags.target
    ,cum_errors.cum_mse
from tmp_train_{year} as tmp_train
inner join lags on tmp_train.date = lags.date and tmp_train.numeric_id = lags.numeric_id
inner join cum_errors on tmp_train.date = cum_errors.date and tmp_train.numeric_id = cum_errors.numeric_id
"""

execute_sql(sql)

#%%

execute_sql(f"create INDEX date_{year}_idx ON train_{year} (date)")