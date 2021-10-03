from dash import html

from .editable_table import editable_table
from .editable_form import modal_form

layout = html.Div([
    html.Div([
        html.Div([], className="col-md-1"),
        html.Div([
            html.H2('Employees'),
            html.Div(editable_table),
        ], className="col-md-10"),
        html.Div([], className="col-md-1")
    ], className='row'),
    modal_form,
], className="container-fluid")
