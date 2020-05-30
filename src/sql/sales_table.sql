CREATE UNLOGGED TABLE sales (
    id VARCHAR(31)
    ,posting_date DATE
    ,quantity INT
    ,PRIMARY KEY (id, posting_date)
)