create table snap_influence as
with base as (
select
    sbd.store_id
    ,sbd.dept_id
    ,snap_status
    ,sbd.date
    ,sum(quantity) as quantity
from
    sales_by_day as sbd
    left join snap_info si on sbd.date = si.date and sbd.state_id = si.state_id
where
    sbd.date between '2011-01-01' and '2012-12-31'
group by 1,2,3,4
),
wd as
(
select
    base.store_id
    ,base.dept_id
    ,base.snap_status
    ,avg(quantity) as weekday_quantity
    ,percentile_cont(0.5) within group (order by quantity) as weekday_median
from
    base
group by 1,2,3)

select
    wd.store_id
    ,wd.dept_id
    ,wd.snap_status
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