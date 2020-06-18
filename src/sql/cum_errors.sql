create unlogged table cum_errors as
with base as (
select
    se.id
    ,se.quantity
    ,se.date
from sales_ext as se
inner join price_changes as pc on se.store_id = pc.store_id and se.item_id = pc.item_id and se.wm_yr_wk = pc.wm_yr_wk
inner join (select id, min(date) as min_date from sales_ext where quantity>0 group by id) as
    start_sales on se.id=start_sales.id and (start_sales.min_date <= se.date)
where se.date < '2016-01-31'
-- and se.id = 'FOODS_1_004_CA_4_validation'
),
daily_error as (
select
    b1.id
    ,b1.date
    ,b1.quantity
    ,b2.quantity as b2_quantity
    --fixme We are using price changes to filter on items being on sale, as an estimate to "RMSE" is only calculated from first day of sale
    ,POWER(b1.quantity -coalesce(b2.quantity, 0),2) as square_error
from base as b1
left join base as b2 on b1.id=b2.id and b1.date=b2.date + interval '1 day'
)

select
    id
    ,date
    ,quantity
    ,square_error
    ,avg(square_error) over hist as cum_mse
from
    daily_error
group by 1,2,3,4
window
    hist as (partition by id order by date asc rows between unbounded preceding and 0 preceding)
;

ALTER TABLE cum_errors ADD CONSTRAINT cum_errors_pkey PRIMARY KEY(date, id)