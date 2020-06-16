create unlogged table calendar (
    date timestamp PRIMARY KEY
    ,wm_yr_wk INT
    ,weekday TEXT
    ,wday INT4
    ,month INT4
    ,year INT
    ,d text
    ,event_name_1 text
    ,event_type_1 text
    ,event_name_2 text
    ,event_type_2 text
    ,snap_CA bool
    ,snap_TX bool
    ,snap_WI bool
)
