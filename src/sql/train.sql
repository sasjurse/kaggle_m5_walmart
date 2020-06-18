create table train as
select
    se.id
    ,se.date
    ,se.weekday
    ,se.store_id
    ,se.dept_id
    ,se.state_id
    ,si.snap_status
    ,si.days_since_snap
    ,lags.quantity_last_1
    ,lags.quantity_last_3
    ,lags.quantity_last_7
    ,lags.quantity_last_21
    ,wa.relative_median
    ,quantity_last_7 * wa.relative_median as wa_adjusted_quantity_last_7
    ,sinf.relative_median as sinf_relative_median
    ,quantity_last_7 * sinf.relative_median as sinf_adjusted_quantity_last_7
    ,pc.price_change_w1
    ,pc.price_change_w3
    ,lags.target
from sales_ext as se
inner join price_changes as pc on se.store_id = pc.store_id and se.item_id = pc.item_id and se.wm_yr_wk = pc.wm_yr_wk
left join snap_info as si on se.state_id = si.state_id and si.date = se.date
left join lags on se.date = lags.date and se.id = lags.id
left join weekday_average as wa
    on se.weekday = wa.weekday and wa.dept_id = se.dept_id and wa.store_id = se.store_id
left join snap_influence as sinf
    on se.dept_id = sinf.dept_id and se.store_id = sinf.store_id
        and sinf.snap_status = si.snap_status
where se.date between '2015-01-01' and '2016-01-31'
;

ALTER TABLE train ADD CONSTRAINT date_item_id_pkey PRIMARY KEY(date, id)