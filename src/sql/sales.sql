create table sales as (
select
    sr.id
    ,c.date
    ,sr.quantity
from
    sales_raw as sr
    left join calendar as c on c.d = sr.d
)
;
ALTER TABLE sales ADD CONSTRAINT sales_pkey PRIMARY KEY(date, id)