create table weekday_average as
with base as (
select
    store_id
    ,dept_id
    ,weekday
    ,date
    ,sum(quantity) as quantity
from
    sales_by_day
where
    date between '2011-01-01' and '2012-12-31'
group by 1,2,3,4
),
wd as
(
select
    base.store_id
    ,base.dept_id
    ,base.weekday
    ,avg(quantity) as weekday_quantity
    ,percentile_cont(0.5) within group (order by quantity) as weekday_median
from
    base
group by 1,2,3)

select
    wd.store_id
    ,wd.dept_id
    ,wd.weekday
    ,wd.weekday_quantity / actual_avg as relative_average
    ,wd.weekday_median / actual_avg as relative_median
from
    wd
left join (
    select
        store_id
        ,dept_id
        ,avg(quantity) as actual_avg
    from base
    group by 1,2
) as agg on wd.store_id = agg.store_id and wd.dept_id = agg.dept_id
