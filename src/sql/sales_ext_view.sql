create or replace view sales_ext  as (
select 
    sr.id
    ,sr.quantity
    ,c.date
    ,c.weekday
    ,c.year
    ,c.wm_yr_wk
    ,c.event_name_1
    ,c.event_name_2
    ,c.event_type_1
    ,c.event_type_2
    ,i.dept_id
    ,i.cat_id
    ,i.store_id
    ,i.state_id
from 
    sales_raw as sr
    left join calendar as c on c.d = sr.d
    left join item_info as i on sr.id = i.id
)