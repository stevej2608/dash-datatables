from dash import html
from dash.dependencies import Input, Output

import dash_datatables as ddt

import pandas as pd

# https://dash.plot.ly/datatable

df = pd.read_csv("demo/static/employees.csv")

layout = html.Div([
    html.Div([
        html.Div([], className="col-md-2"),
        html.Div([
            html.H2('Employees'),
            html.Br(),
            ddt.DashDatatables(
                id='employees',
                columns=[{"title": i, "data": i} for i in df.columns],
                data=df.to_dict('records'),
                width="100%",
                pagelength=20,
                order=[2, 'asc'],
            ),
        html.Div(id='output')
        ], className="col-md-8"),
        html.Div([], className="col-md-2")
    ], className='row')
], className="container-fluid")
