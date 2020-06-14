create unlogged table if not exists validation (
    model_name TEXT
    ,date timestamp
    ,id TEXT
    ,predicted double precision
    ,primary key (model_name, date, id)
)
