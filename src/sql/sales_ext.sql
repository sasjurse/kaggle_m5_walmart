create or replace view sales_ext  as (
select 
    sr.numeric_id
    ,sr.quantity
    ,c.date
    ,c.wday
    ,c.weekday
    ,c.year
    ,c.wm_yr_wk
    ,c.event_name_1
    ,c.event_name_2
    ,c.event_type_1
    ,c.event_type_2
    ,c.snap_ca
    ,c.snap_tx
    ,c.snap_wi
    ,i.id
    ,i.dept_id
    ,i.item_id
    ,i.cat_id
    ,i.store_id
    ,i.state_id
from 
    sales as sr
    left join calendar as c on c.date = sr.date
    left join item_info as i on sr.numeric_id = i.numeric_id
)