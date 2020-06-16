create table snap_info as
with base as (
    select
        date
        ,state_id
        ,case
            when state_id ='CA' then snap_ca
            when state_id ='WI' then snap_tx
            when state_id ='TX' then snap_tx
            end
        as snap_status
from calendar
cross join (select distinct state_id from item_info) as si
)

select 
d1.date
,d1.state_id
,d1.snap_status
,min(DATE_PART('day', d1.date-d2.date)) as days_since_snap
from base as d1
left join base as d2 on d2.date < d1.date and d2.state_id = d1.state_id and d2.snap_status = True
group by 1,2,3
;

ALTER TABLE snap_info ADD CONSTRAINT date_state_idx PRIMARY KEY(date, state_id)