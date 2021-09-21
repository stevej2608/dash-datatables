from dash import html
from dash.dependencies import Input, Output

import dash_datatables as ddt

from app import app

columnDefs = [
    {'title': "ID", 'data': 'id', 'visible': False},
    {'title': "Name", 'data': 'name'},
    {'title': "Owner", 'data': 'owner'},
    {'title': "Date", 'data': 'date'},
]

tableData = [
    {
        'id': 1,
        'name': 'XXX',
        'owner': 'YYY',
        'date': '2018',
    },
    {
        'id': 2,
        'name': 'XXX',
        'owner': 'YYY',
        'date': '2018',
    },
    {
        'id': 3,
        'name': 'XXX',
        'owner': 'YYY',
        'date': '2018',
    },
]

layout = html.Div([
    html.Div([
        html.Div([], className="col-md-2"),
        html.Div([
            html.H2('All Portfolios'),
            html.Br(),
            ddt.DashDatatables(
                id='editable#table',
                editable=True,
                data=tableData,
                columns=columnDefs,
                width="100%",
                order=[2, 'asc'],
            ),
        html.Div(id='editable#output')
        ], className="col-md-8"),
        html.Div([], className="col-md-2")
    ], className='row')
], className="container-fluid")

@app.callback(Output('editable#output', 'children'), [Input('editable#table', 'table_event')])
def display_output(value):
    print('display_output')
    return 'Table event {}'.format(value)

@app.callback(Output('editable#table', 'data'), [Input('editable#table', 'table_event')])
def add_row(value):
    if value and value['action'] == 'add_row':
        print('add_row')
        tableData.append({
            'id': 4,
            'name': 'New Data',
            'owner': 'ZZZ',
            'date': '2019',
        }),
    # print(str(tableData))
    return tableData
