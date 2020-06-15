create unlogged table if not exists model_info (
    model_name text
    ,created_at TIMESTAMP
    ,params TEXT
    ,rmse double precision
    ,git_commit TEXT
    ,PRIMARY KEY (model_name, created_at)
)