create unlogged table grouped_lags(
item_id text
,date date
,state_id text
,state_average_last_7 real
,state_average_last_21 real
)
;

insert into grouped_lags
select
    item_info.item_id
    ,lags.date
    ,item_info.state_id
    ,avg(avg_last_7) state_average_last_7
    ,avg(avg_last_21) state_average_last_21
from lags
inner join item_info on lags.numeric_id = item_info.numeric_id
group by 1,2,3
;

create INDEX grouped_lags_date_idx ON grouped_lags (date)