create table cum_errors as
with base as (
select
    se.id
    ,se.quantity
    ,se.date
from sales_ext as se
inner join price_changes as pc on se.store_id = pc.store_id and se.item_id = pc.item_id and se.wm_yr_wk = pc.wm_yr_wk
where se.date < '2016-01-31'
),
daily_error as (
select
    b1.id
    ,b1.date
    ,POWER(b1.quantity -b2.quantity,2) as square_error
from base as b1
inner join base as b2 on b1.id=b2.id and b1.date=b2.date + interval '1 day'
)

select
    id
    ,date
    ,avg(square_error)
from
    daily_error
group by 1,2
window
    hist as (partition by id order by date asc rows between unbounded preceding and 1 preceding)
;

ALTER TABLE cum_errors ADD CONSTRAINT cum_errors PRIMARY KEY(date, id)