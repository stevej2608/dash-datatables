import json
from dash import html
from dash.dependencies import Input, Output

import dash_datatables as ddt
import dash_html_components as html

import pandas as pd

from app import app

# https://dash.plot.ly/datatable

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

# Blank column for checkboxes

df.insert(0, '', '')

columns = [{"title": i, "data": i} for i in df.columns]

def solar_table():
    return ddt.DashDatatables(
        id='solar',
        columns=columns,
        data=df.to_dict('records'),
        width="100%",
        order=[2, 'asc'],

        # Following is needed for checkbox based row selection
        # https://datatables.net/extensions/select/examples/initialisation/checkbox

        column_defs = [ {
            "width": "5%", "targets": 0 ,
            'orderable': False,
            'className': 'select-checkbox',
            }],

        select = {
            'style':    'os',
            'selector': 'td:first-child'
            },
    )


layout = html.Div([
    html.Div([
        html.Div([], className="col-md-1"),
        html.Div([
            html.H2('US Solar Capacity'),
            html.Br(),
            html.Div(solar_table(), id='table-container'),
            html.Div(id='solar#output')
        ], className="col-md-10"),
        html.Div([], className="col-md-1")
    ], className='row')
], className="container-fluid")


@app.callback(Output('solar#output', 'children'), [Input('solar', 'table_event')])
def display_output(value):
    selected = None

    if value and value['action'] == 'selectItems':
        selected = value['indexes']
        selected = format(json.dumps(selected))

    print('Select rows: {}'.format(selected))
    return 'Select rows: {}'.format(selected)
