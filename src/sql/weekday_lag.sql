create unlogged table weekday_lag (
numeric_id Integer
,date date
,wday smallint
,weekday_last_1 real
,weekday_last_2 real
,weekday_last_8 real
)
;

insert into weekday_lag
with base as (
select
    numeric_id
    ,quantity
    ,sales.date
    ,c.wday
from sales
inner join calendar as c on sales.date = c.date
)

select
    numeric_id
    ,date
    ,wday
    ,avg(quantity) over w1 as weekday_last_1
    ,avg(quantity) over w2 as weekday_last_2
    ,avg(quantity) over w8 as weekday_last_8
from base
window
    w1 as (partition by numeric_id, wday order by date asc rows between 1 preceding and 1 preceding)
    ,w2 as (partition by numeric_id, wday order by date asc rows between 2 preceding and 1 preceding)
    ,w8 as (partition by numeric_id, wday order by date asc rows between 8 preceding and 1 preceding)
;

ALTER TABLE weekday_lag ADD CONSTRAINT weekday_lag_pkey PRIMARY KEY(date, numeric_id)