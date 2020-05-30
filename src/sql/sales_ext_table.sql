CREATE UNLOGGED TABLE sales_ext (
    id varchar(31)
    ,item_id varchar(31)
    ,dept_id varchar(11)
    ,cat_id varchar(9)
    ,store_id varchar(4)
    ,state_id varchar(2)
    ,d varchar(6)
    ,quantity INT
    ,PRIMARY KEY (id, d)
)