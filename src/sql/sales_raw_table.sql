CREATE UNLOGGED TABLE sales_raw (
    id VARCHAR(31)
    ,d VARCHAR(6)
    ,quantity INT
    ,PRIMARY KEY (id, d)
)