CREATE UNLOGGED TABLE sales_ext (
    id varchar(50)
    ,item_id varchar(50)
    ,dept_id varchar(20)
    ,cat_id varchar(20)
    ,store_id varchar(10)
    ,state_id varchar(10)
    ,posting_date DATE
    ,quantity INT
    ,PRIMARY KEY (id, posting_date)
)