create unlogged table prices (
    store_id TEXT
    ,item_id TEXT
    ,wm_yr_wk int
    ,sell_price NUMERIC(8,2)
    ,primary key (item_id, store_id, wm_yr_wk)
)
