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

#%%



sql = 'select date, store_id, sum(quantity) as quantity from sales_by_day group by 1,2 order by date desc'
df = dataframe_from_sql(sql)

fig = px.line(df, x="date", y="quantity", color='store_id')

plotly.offline.plot(fig, filename=str(plots_folder() / 'sales_by_store.html'))

#%%


sql = 'select date, dept_id, sum(quantity) as quantity from sales_by_day group by 1,2 order by 1 desc'
df = dataframe_from_sql(sql)

fig = px.line(df, x="date", y="quantity", color='dept_id')

plotly.offline.plot(fig, filename=str(plots_folder() / 'sales_by_dept.html'))

#%%

sql = """
with base as (
select 
    date
    ,dept_id
    ,sum(quantity) as quantity 
from sales_by_day 
group by 1,2
)

select 
    date
    ,dept_id
    ,sum(quantity) over w as quantity 
from base
window w as (partition by dept_id order by date desc rows between 3 preceding and 3 following)
order by 1 desc"""


df = dataframe_from_sql(sql)

fig = px.line(df, x="date", y="quantity", color='dept_id')

plotly.offline.plot(fig, filename=str(plots_folder() / 'sales_by_dept_MA.html'))


#%%

sql = """
with base as (
select 
    date
    ,store_id
    ,sum(quantity) as quantity 
from sales_by_day 
group by 1,2
)

select 
    date
    ,store_id
    ,sum(quantity) over w as quantity 
from base
window w as (partition by store_id order by date desc rows between 3 preceding and 3 following)
order by 1 desc"""


df = dataframe_from_sql(sql)

fig = px.line(df, x="date", y="quantity", color='store_id')

plotly.offline.plot(fig, filename=str(plots_folder() / 'sales_by_store_MA.html'))