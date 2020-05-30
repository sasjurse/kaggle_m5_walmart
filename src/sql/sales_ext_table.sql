CREATE UNLOGGED TABLE sales_ext (
    id TEXT
    ,item_id TEXT
    ,dept_id TEXT
    ,cat_id TEXT
    ,store_id TEXT
    ,state_id TEXT
    ,d TEXT
    ,quantity INT
    ,PRIMARY KEY (id, d)
)