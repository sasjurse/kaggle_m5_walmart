CREATE UNLOGGED TABLE sales (
    id VARCHAR(50)
    ,posting_date DATE
    ,quantity INT
    ,PRIMARY KEY (id, posting_date)
)