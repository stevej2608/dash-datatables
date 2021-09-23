import dash
from dash import html
from dash.dependencies import Input, Output

import dash_datatables as ddt

from app import app

NOUPDATE = dash.no_update

columnDefs = [
    {'title': "ID", 'data': 'id', 'visible': False},
    {'title': "Portfolio Name", 'data': 'name'},
    {'title': "Owner", 'data': 'owner'},
    {'title': "Date", 'data': 'date'},
]

tableData = [
    {
        'id': 1,
        'name': 'All share',
        'owner': 'Henry',
        'date': '2018',
    },
    {
        'id': 2,
        'name': 'Last Gasp',
        'owner': 'Big Joe',
        'date': '2021',
    },
    {
        'id': 3,
        'name': 'FT100 Main',
        'owner': 'Steve',
        'date': '2016',
    },
]

def editable_table():
    return ddt.DashDatatables(
        id='editable#table',
        editable=True,
        data=tableData,
        columns=columnDefs,
        width="100%",
        order=[2, 'asc'],
    ),

layout = html.Div([
    html.Div([
        html.Div([], className="col-md-2"),
        html.Div([
            html.H2('All Portfolios'),
            html.Div(editable_table(), id='editable#table-container'),
        ], className="col-md-8"),
        html.Div([], className="col-md-2")
    ], className='row')
], className="container-fluid")


@app.callback(Output('editable#table','data'), [Input('editable#table', 'table_event')])
def add_row(value):
    global tableData

    def row_index(id):
        for idx, row in enumerate(tableData):
            if row['id'] == id:
                return idx
        raise "id not in table"

    if value and value['action'] == 'add_row':
        print('add_row')
        tableData.append({
            'id': len(tableData) + 1,
            'name': 'Mega Bucks',
            'owner': 'Elizabeth Holmes',
            'date': '2019',
        }),
        return tableData

    if value and value['action'] == 'delete_row':
        id = value['data']['id']
        print(f'delete_row {id}')
        index = row_index(id)
        del tableData[index]
        return tableData

    if value and value['action'] == 'edit_row':
        id = value['data']['id']
        print(f'edit_row {id} - Not implemented yet')

    return NOUPDATE
