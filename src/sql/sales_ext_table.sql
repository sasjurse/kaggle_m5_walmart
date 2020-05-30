CREATE UNLOGGED TABLE sales_ext (
    id varchar(31)
    ,item_id varchar(31)
    ,dept_id varchar(20)
    ,cat_id varchar(20)
    ,store_id varchar(10)
    ,state_id varchar(10)
    ,d varchar(6)
    ,quantity INT
    ,PRIMARY KEY (id, d)
)