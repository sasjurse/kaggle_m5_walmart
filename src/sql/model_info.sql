create unlogged table if not exists model_info (
    model_name text
    ,created_at TIMESTAMP
    ,params TEXT
    ,features TEXT
    ,rmse double precision
    ,git_commit TEXT
)