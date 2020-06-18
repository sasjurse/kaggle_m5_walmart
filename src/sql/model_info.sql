create unlogged table if not exists model_info (
    model_name text
    ,rmse double precision
    ,created_at TIMESTAMP
    ,params TEXT
    ,train_size integer
    ,features TEXT
    ,git_commit TEXT
)