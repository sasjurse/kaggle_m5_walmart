create unlogged table sales (
    numeric_id Integer
    ,date date
    ,quantity smallint
)
;
insert into sales
select
    item_info.numeric_id
    ,c.date
    ,sr.quantity
from
    sales_raw as sr
    inner join item_info  on sr.id = item_info.id
    left join calendar as c on c.d = sr.d
;
ALTER TABLE sales ADD CONSTRAINT sales_pkey PRIMARY KEY(date, numeric_id)