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
where sales_ext.date between '2014-01-01' and '2015-04-01'

),

aggregates as (
select
    id
    ,date
    ,quantity as target
    ,weekday
    ,store_id
    ,dept_id
    ,state_id
    ,snap_status
    ,days_since_snap
    ,sum(quantity) over w3 as quantity_last_3
    ,sum(quantity) over w7 as quantity_last_7
    ,sum(quantity) over w21 as quantity_last_21
    ,sum(case when snap_status then quantity else 0 end ) over w21 as quantity_last_21_SNAP
from base
window
    w3 as (partition by id order by date asc rows between 3 preceding and 1 preceding)
    ,w7 as (partition by id order by date asc rows between 7 preceding and 1 preceding)
    ,w21 as (partition by id order by date asc rows between 21 preceding and 1 preceding)
)

select
*
from aggregates
where date > '2014-02-01'