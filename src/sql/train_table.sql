create table train as
with base as (
select
    id
    ,quantity
    ,sales_ext.date
    ,weekday
    ,store_id
    ,dept_id
    ,sales_ext.state_id
    ,si.snap_status
    ,si.days_since_snap
from sales_ext
left join snap_info as si on sales_ext.state_id = si.state_id and si.date = sales_ext.date
where sales_ext.date between '2014-10-01' and '2016-01-31'
),

aggregates as (
select
    id
    ,date
    ,quantity as target
    ,base.weekday
    ,base.store_id
    ,base.dept_id
    ,state_id
    ,snap_status
    ,days_since_snap
    ,wa.relative_median
    ,sum(quantity) over w3 as quantity_last_3
    ,sum(quantity) over w7 as quantity_last_7
    ,sum(quantity) over w7 * wa.relative_median as wa_adjusted_quantity_last_7
    ,sum(quantity) over w21 as quantity_last_21
    ,sum(case when snap_status then quantity else 0 end ) over w21 as quantity_last_21_SNAP
from base
left join weekday_average as wa
    on base.weekday = wa.weekday and wa.dept_id = base.dept_id and wa.store_id = base.store_id
window
    w3 as (partition by id order by date asc rows between 3 preceding and 1 preceding)
    ,w7 as (partition by id order by date asc rows between 7 preceding and 1 preceding)
    ,w21 as (partition by id order by date asc rows between 21 preceding and 1 preceding)
)

select
*
from aggregates
where date > '2015-01-01'
;

ALTER TABLE train ADD CONSTRAINT date_item_id_pkey PRIMARY KEY(date, id)