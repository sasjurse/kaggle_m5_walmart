#%%
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, State, Input
import logging
import plotly.graph_objects as go
import plotly
import plotly.express as px

import pandas as pd

from generics.postgres import dataframe_from_sql
from generics.file_locations import plots_folder

sql = """
with base as (
select 
    id
    ,quantity
    ,date
    ,weekday
    ,dept_id
from sales_ext
where date between '2014-01-01' and '2014-06-01'
-- and id = 'HOUSEHOLD_2_516_WI_3_validation'
),

aggregates as (
select 
    id
    ,date
    ,quantity as target
    ,weekday
    ,dept_id
    ,sum(quantity) over w7 as quantity_last_7 
    ,sum(quantity) over w21 as quantity_last_21     
from base
window 
    w7 as (partition by id order by date asc rows between 7 preceding and 1 preceding)
    ,w21 as (partition by id order by date asc rows between 21 preceding and 1 preceding)
)

select 
*
from aggregates
where date > '2014-02-01'


order by 1 desc"""


df = dataframe_from_sql(sql)

#%%

sql = "select * from sales_ext where id = 'HOUSEHOLD_2_516_WI_3_validation' and date between '2014-01-01' and '2014-02-01'"
df2 = dataframe_from_sql(sql)