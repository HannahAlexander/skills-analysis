from dash import Dash, html, dcc
import ids
from dash.dependencies import Input, Output
import sys

from analysing_data_final import get_employee_names

def render(app: Dash) -> html.Div:
    all_employees = get_employee_names()

    return html.Div(
        children = [
            html.H5("Select employee to see their skill set", className='mt-2'),
                dcc.Dropdown(
                id= ids.EMPLOYEE_DROPDOWN,
                value = all_employees[0],
                options= [{"label": employee, "value": employee} for employee in all_employees]),
        ]
    )