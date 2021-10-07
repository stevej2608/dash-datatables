import dash
import dash_bootstrap_components as dbc
import dash_holoniq_components as dhc
import dash_html_components as html
from app import app
from dash import no_update as NOUPDATE
from dash.dependencies import Input, Output, State

from .employee_list import df, new_employee


def isTriggered(component_id, component_property):
    """Return true if given input triggered the callback"""
    ctx = dash.callback_context
    if not ctx.triggered:
        return False

    prop_id = f"{component_id}.{component_property}"
    return ctx.triggered[0]['prop_id'] == prop_id


def form_body(action="blank_form", row_data=None):
    """Return form that's fully populated with relevant fields and buttons for the given action"""

    def form_field(label, name, value):
        return dbc.FormGroup([dbc.Label(label), dbc.Input(name=name, value=value)])

    def form_builder(form, buttons):
        form.children = [

            # Hidden fields used to report the table row id & action

            dbc.Input(name='id', type="hidden", value=row_data['id']),
            dbc.Input(name='action', type="hidden", value=action),

            form_field("First Name", "first_name", row_data['First name']),
            form_field("Last Name", "last_name", row_data['Last name']),
            form_field("Office", "office", row_data['Office']),
            form_field("Position", "position", row_data['Position']),
            form_field("Start date", "start_date", row_data['Start date']),
            form_field("Salary", "salary", row_data['Salary']),

            dbc.ButtonGroup(buttons, className='float-right mt-2')
         ]
        return form

    header = "Header"

    # Only one of the folowing buttons appears on the form

    add_btn = dbc.Button('Add', type='submit', color="primary")
    delete_btn = dbc.Button('Delete', type='submit', color="primary")
    edit_btn = dbc.Button('Update', type='submit', color="primary")

    # Allways have a form body & cancel button

    employee_form = dhc.Form([], id='employee-form', preventDefault=True)
    cancel_btn = dbc.Button("Cancel", id="close-btn", className="ml-1", n_clicks=0)

    if action == 'add_row':
        header = "New Employee"
        form = form_builder(employee_form, [add_btn, cancel_btn])

    elif action == 'delete_row':
        header = "Delete Employee"
        form = form_builder(employee_form, [delete_btn, cancel_btn])

    elif action == 'edit_row':
        header = "Edit Employee"
        form = form_builder(employee_form, [edit_btn, cancel_btn])

    else:
        form = [employee_form, cancel_btn]

    return [
        dbc.ModalHeader(header),
        dbc.ModalBody(form),
    ]


modal_form = html.Div(dbc.Modal(form_body(), id="modal", is_open=False))

@app.callback(
    [Output("modal", "is_open"), Output("modal", "children")],
    [Input('editable-table', 'table_event'), Input("close-btn", "n_clicks"), Input("employee-form", "form_data")])
def toggle_modal(table_evt, close_btn, value):
    global df
    is_open = False
    form = NOUPDATE

    # print(f'toggle_modal {is_open}')

    def new_id():
        id = df['id'].max()
        return id + 1 if id == id else 0

    # Populate modal form fields based on table event

    if isTriggered('editable-table', 'table_event'):
        action = table_evt['action']
        if action == "add_row":
            id = new_id()
            row_data = new_employee(id)
        else:
            row_data = table_evt['data']
        form = form_body(action, row_data)
        is_open = True

    elif close_btn or value:
        is_open = False

    return is_open, form

@app.callback(Output('editable-table','data'), Input("employee-form", "form_data"))
def table_update(value):
    global df
    table_data = NOUPDATE

    if value:
        action = value['action']
        employee_data = {
            "id": int(value['id']),
            "First name": value["first_name"],
            "Last name": value["last_name"],
            "Office": value["office"],
            "Position": value["position"],
            "Start date": value["start_date"],
            "Salary": value["salary"],            
        }

        if action == 'add_row':
            df = df.append(employee_data, ignore_index=True)

        if action == 'delete_row':
            id = employee_data['id']
            df = df[df.id != id]

        if action == 'edit_row':
            id = employee_data['id']
            #df.loc[df['id'] == id, list(employee_data.keys())] = list(employee_data.values())
            # df = df[df.id != id]
            # df = df.append(employee_data, ignore_index=True)
            keys, values = zip(*employee_data.items())
            df.loc[df['id'] == id, keys] = values

    table_data = df.to_dict('records')
    return table_data
