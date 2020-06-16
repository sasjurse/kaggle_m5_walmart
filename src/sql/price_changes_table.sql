create table price_changes as
with base as (
select
    item_id
    ,store_id
    ,wm_yr_wk
    ,sell_price as current_price
    ,avg(sell_price) over w1 as last_price
    ,avg(sell_price) over w3 as avg_price
from prices
window
     w1 as (partition by item_id, store_id order by wm_yr_wk asc rows between 1 preceding and 1 preceding)
    ,w3 as (partition by item_id, store_id order by wm_yr_wk asc rows between 3 preceding and 1 preceding)
)

select
    item_id
    ,store_id
    ,wm_yr_wk
    ,coalesce(current_price/last_price, current_price) as price_change_w1
    ,coalesce(current_price/avg_price, current_price) as price_change_w3
from base
;

ALTER TABLE price_changes ADD CONSTRAINT price_changes_pkey PRIMARY KEY(item_id, store_id, wm_yr_wk)