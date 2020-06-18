drop table if exists tmp_train
;
create unlogged table tmp_train as
select
se.numeric_id
, se.date
, se.weekday
, se.store_id
, se.dept_id
, se.state_id
, si.snap_status
, si.days_since_snap
, wa.relative_median
, pc.price_change_w1
, pc.price_change_w3
from sales_ext as se
inner join price_changes as pc on se.store_id = pc.store_id and se.item_id = pc.item_id and se.wm_yr_wk = pc.wm_yr_wk
inner join snap_info as si on se.state_id = si.state_id and si.date = se.date
inner join weekday_average as wa
    on se.weekday = wa.weekday and wa.dept_id = se.dept_id and wa.store_id = se.store_id
inner join snap_influence as sinf
    on se.dept_id = sinf.dept_id and se.store_id = sinf.store_id
        and sinf.snap_status = si.snap_status
where se.date between '2013-01-01' and '2016-01-31'
;

create unlogged table train as
select
    tmp_train.numeric_id
    ,tmp_train.date
    ,tmp_train.weekday
    ,tmp_train.store_id
    ,tmp_train.dept_id
    ,tmp_train.state_id
    ,tmp_train.snap_status
    ,tmp_train.days_since_snap
    ,lags.avg_last_1
    ,lags.avg_last_3
    ,lags.avg_last_7
    ,lags.avg_last_21
    ,lags.max_last_21
    ,lags.min_last_21
    ,lags.std_last_21
    ,lags.max_last_42
    ,lags.min_last_42
    ,lags.avg_last_42
    ,tmp_train.relative_median
    ,avg_last_7 * tmp_train.relative_median as wa_adjusted_quantity_last_7
    ,tmp_train.relative_median as sinf_relative_median
    ,avg_last_7 * tmp_train.relative_median as sinf_adjusted_quantity_last_7
    ,tmp_train.price_change_w1
    ,tmp_train.price_change_w3
    ,lags.target
from tmp_train
inner join lags on tmp_train.date = lags.date and tmp_train.numeric_id = lags.numeric_id
;
create INDEX date_idx ON train (date)
;
drop table if exists tmp_train
;