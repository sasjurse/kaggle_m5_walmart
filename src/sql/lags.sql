create table lags as
with base as (
select
    id
    ,quantity
    ,date
from sales_ext
where sales_ext.date between '2014-10-01' and '2016-01-31'
),

aggregates as (
select
    id
    ,date
    ,quantity as target
    ,sum(quantity) over w1 as quantity_last_1
    ,sum(quantity) over w3 as quantity_last_3
    ,sum(quantity) over w7 as quantity_last_7
    ,sum(quantity) over w21 as quantity_last_21
from base
window
    w1 as (partition by id order by date asc rows between 1 preceding and 1 preceding)
    ,w3 as (partition by id order by date asc rows between 3 preceding and 1 preceding)
    ,w7 as (partition by id order by date asc rows between 7 preceding and 1 preceding)
    ,w21 as (partition by id order by date asc rows between 21 preceding and 1 preceding)
)

select
*
from aggregates
where date > '2015-01-01'
;

ALTER TABLE lags ADD CONSTRAINT lags_pkey PRIMARY KEY(date, id)