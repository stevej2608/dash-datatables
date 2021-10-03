import dash_datatables as ddt

from .employee_list import df

editable_table = ddt.DashDatatables(
    id='editable-table',
    editable=True,
    columns=[{"title": i, "data": i} for i in df.columns],
    data=df.to_dict('records'),
    width="100%",
    pagelength=20,
    order=[2, 'asc'],
)
