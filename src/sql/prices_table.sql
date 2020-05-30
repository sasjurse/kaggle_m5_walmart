create unlogged table prices (
    item_id varchar(50)
    ,store_id varchar(10)
    ,wm_yr_wk int
    ,sell_price NUMERIC(8,2)
    ,primary key (item_id, store_id, wm_yr_wk)
)
