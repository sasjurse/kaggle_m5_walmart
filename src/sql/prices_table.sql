create unlogged table prices (
    store_id varchar(10)
    ,item_id varchar(50)
    ,wm_yr_wk int
    ,sell_price NUMERIC(8,2)
    ,primary key (item_id, store_id, wm_yr_wk)
)
