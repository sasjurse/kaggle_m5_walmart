create unlogged table calendar (
    date date
    ,wm_yr_wk INT
    ,weekday TEXT
    ,wday INT4
    ,month INT4
    ,year INT
    ,d text PRIMARY KEY -- joins are usually on this column
    ,event_name_1 text
    ,event_type_1 text
    ,event_name_2 text
    ,event_type_2 text
    ,snap_CA bool
    ,snap_TX bool
    ,snap_WI bool
)
