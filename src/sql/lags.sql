create unlogged table lags(
numeric_id Integer
,date date
,target smallint
,target10 smallint
,target20 smallint
,avg_last_1 real
,avg_last_3 real
,avg_last_7 real
,avg_last_21 real
,max_last_21 smallint
,min_last_21 smallint
,std_last_21 real
,avg_last_42 real
,max_last_42 smallint
,min_last_42 smallint
)
;
insert into lags
with base as (
select
    numeric_id
    ,quantity
    ,date
from sales
where sales.date between '2011-10-01' and '2016-01-31'
),

aggregates as (
select
    numeric_id
    ,date
    ,quantity as target
    ,sum(quantity) over f10 as target10
    ,sum(quantity) over f20 as target20
    ,avg(quantity) over w1 as avg_last_1
    ,avg(quantity) over w3 as avg_last_3
    ,avg(quantity) over w7 as avg_last_7
    ,avg(quantity) over w21 as avg_last_21
    ,max(quantity) over w21 as max_last_21
    ,min(quantity) over w21 as min_last_21
    ,stddev(quantity) over w21 as std_last_21
    ,avg(quantity) over w42 as avg_last_42
    ,max(quantity) over w42 as max_last_42
    ,min(quantity) over w42 as min_last_42
from base
window
    f10 as (partition by numeric_id order by date asc rows between 10 following and 10 following)
    ,f20 as (partition by numeric_id order by date asc rows between 20 following and 20 following)
    ,w1 as (partition by numeric_id order by date asc rows between 1 preceding and 1 preceding)
    ,w3 as (partition by numeric_id order by date asc rows between 3 preceding and 1 preceding)
    ,w7 as (partition by numeric_id order by date asc rows between 7 preceding and 1 preceding)
    ,w21 as (partition by numeric_id order by date asc rows between 21 preceding and 1 preceding)
    ,w42 as (partition by numeric_id order by date asc rows between 42 preceding and 1 preceding)
)

select
*
from aggregates
where date > '2013-01-01'
;

ALTER TABLE lags ADD CONSTRAINT lags_pkey PRIMARY KEY(date, numeric_id)