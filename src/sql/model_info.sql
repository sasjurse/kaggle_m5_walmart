create unlogged table if not exists model_info (
    model_name text
    ,created_at TIMESTAMP
    ,rmse double precision
--    ,params TEXT
    ,git_commit TEXT
    ,PRIMARY KEY (model_name, created_at)
)