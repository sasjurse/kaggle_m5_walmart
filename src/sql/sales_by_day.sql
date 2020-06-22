CREATE UNLOGGED TABLE sales_by_day as (
select
    se.date
    ,weekday
    ,wday
    ,year
    ,dept_id
    ,store_id
    ,cat_id
    ,state_id
    ,sum(quantity) as quantity
from sales_ext as se
group by 1,2,3,4,5,6,7,8
)