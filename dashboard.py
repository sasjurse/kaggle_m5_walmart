import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, State, Input
import plotly.graph_objects as go

from src.postgres import dataframe_from_sql, execute_sql
from src.analysis import update_search_term, get_search_term

server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server)


def search_term_input():
    current_settings = get_search_term()
    return html.Div(id='input', children=[
        dcc.Input(id='query', value=current_settings['search_term'], type='text'),
        html.Button(id='submit-button', type='submit', children='Update search term'),
        html.Div(id='current-search', children=f"Current search is {current_settings['search_term']}")
    ])


@app.callback(Output('current-search', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('query', 'value')],
              )
def update_search_on_changes(n_clicks, input_value):
    current_settings = get_search_term()
    if input_value != current_settings['search_term']:
        update_search_term(search=input_value, location=current_settings['location'])
    return f"Current search is {input_value}"


def location_input():
    current_settings = get_search_term()
    return html.Div(id='location-input', children=[
        dcc.Input(id='location', value=current_settings['location'], type='text'),
        html.Button(id='location-submit-button', type='submit', children='Update location'),
        html.Div(id='current-location', children=f"Current location is {current_settings['location']}")
    ])


@app.callback(Output('current-location', 'children'),
              [Input('location-submit-button', 'n_clicks')],
              [State('location', 'value')],
              )
def update_location_on_changes(n_clicks, location):
    current_settings = get_search_term()
    if location != current_settings['location']:
        update_search_term(search=current_settings['search_term'], location=location)
    text = f"Current location is {location}"
    return text


def refresh_data_button():
    return html.Button(id='refresh-data', type='submit', children='Refresh data')


def clear_data_button():
    return html.Div(children=[html.Button(id='clear-data', type='submit', children='Clear data'),
                              # empty-id is used to target the callbacks from this action without doing anything
                              html.Div(id='empty-id', children='')
                              ])


@app.callback(Output('empty-id', 'children'),
              [Input('clear-data', 'n_clicks')],
              )
def clear_data(n_clicks):
    if n_clicks and n_clicks > 0:  # n_clicks starts as None
        execute_sql('DELETE FROM examples')
    return ''  # FIXME do a proper empty


@app.callback(Output('table', 'data'),
              [Input('refresh-data', 'n_clicks')],
              )
def collect_data_for_table(clicks):
    df = dataframe_from_sql('select * from examples order by id DESC limit 25')
    return df.to_dict('records')


def examples_table():
    #  FIXME: the data collection here could be handled by collect_data_for_table,
    #   but I also want dynamic column definitions..
    df = dataframe_from_sql('select * from examples order by id DESC limit 25')
    return dash_table.DataTable(id='table',
                                columns=[{"name": i, "id": i} for i in df.columns],
                                data=df.to_dict('records'),
                                sort_action='native',
                                style_cell_conditional=[
                                    {'if': {'column_id': 'text'},
                                     'textAlign': 'left'}],
                                style_data_conditional=[
                                    {'if': {'column_id': 'sentiment', 'filter_query': '{sentiment} > 0.8'},
                                     'backgroundColor': 'green',
                                     'color': 'white'},
                                    {'if': {'column_id': 'sentiment', 'filter_query': '{sentiment} < 0.2'},
                                     'backgroundColor': 'red',
                                     'color': 'white'}]
                                )


@app.callback(Output('histogram', 'children'),
              [Input('refresh-data', 'n_clicks')],
              )
def create_histogram(n_clicks=None):
    df = dataframe_from_sql('select sentiment from examples')
    if len(df) < 1000:
        hist_slice = 0.05
    else:
        hist_slice = 0.02
    trace = go.Histogram(x=df['sentiment'], xbins=dict(start=0, end=1, size=hist_slice))
    layout = go.Layout(title='Histogram of sentiment')
    return dcc.Graph(figure=go.Figure(trace, layout=layout))


app.layout = html.Div(children=dcc.Tabs(children=[
    dcc.Tab(label='main', children=[
        html.H1(children='Sentiment analysis'),

        search_term_input(),

        location_input(),

        refresh_data_button(),

        clear_data_button(),

        html.Div(children=[html.H2('Examples'), examples_table()]),

        html.Div(id='histogram')]),
    dcc.Tab(label='other', children=html.H1('Hello'))]
))


if __name__ == '__main__':
    app.run_server(debug=True)

# source venv/bin/activate
# python app.py
# gunicorn dashboard:rapp -b :8049

