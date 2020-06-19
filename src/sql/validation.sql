create unlogged table if not exists validation (
    model_name TEXT
    ,date timestamp
    ,numeric_id integer
    ,predicted real
    ,target smallint
)