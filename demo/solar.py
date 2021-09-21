from dash import html

import dash_datatables as ddt
import dash_html_components as html

import pandas as pd

# https://dash.plot.ly/datatable

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

column_defs = [{"title": i, "data": i} for i in df.columns]

layout = html.Div([
    html.Div([
        html.Div([], className="col-md-2"),
        html.Div([
            html.H2('US Solar Capacity'),
            html.Br(),
            ddt.DashDatatables(
                id='solar',
                columns=column_defs,
                column_defs=[{ "width": "20%", "targets": 0 }],
                data=df.to_dict('records'),
                width="100%",
                editable=True,
                order=[2, 'asc'],
            ),
        html.Div(id='output')
        ], className="col-md-8"),
        html.Div([], className="col-md-2")
    ], className='row')
], className="container-fluid")
