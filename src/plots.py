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


def append_snap_to_fig(fig):
    for column in ['snap_CA', 'snap_TX', 'snap_WI']:
        snap_days = dataframe_from_sql(f'select date, "{column}" from calendar where "{column}"=1')
        trace_1 = go.Scatter(x=snap_days['date'], y=snap_days[column], name=column, mode='markers', yaxis='y2')
        fig.add_trace(trace_1)

    return fig

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
    ,dept_id
    ,sum(quantity) as quantity 
from sales_by_day 
where store_id ='CA_1'
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
fig = append_snap_to_fig(fig)

plotly.offline.plot(fig, filename=str(plots_folder() / 'sales_by_dept_one_store_MA.html'))


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

fig = append_snap_to_fig(fig)

plotly.offline.plot(fig, filename=str(plots_folder() / 'sales_by_store_MA.html'))

#%%

sql = """
select 
train.date
,validation.model_name
,SQRT(AVG(POWER((train.target - validation.predicted),2))) as rmse
from
train
inner join validation on train.date = validation.date and validation.id = train.id
group by 1,2
order by 1 desc"""


df = dataframe_from_sql(sql)

fig = px.line(df, x="date", y="rmse", color='model_name')

plotly.offline.plot(fig, filename=str(plots_folder() / 'RMSE_by_model.html'))

