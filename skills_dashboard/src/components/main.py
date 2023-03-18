from dash import Dash, html, dcc
from dash_bootstrap_components.themes import CYBORG, SOLAR, PULSE, UNITED, SPACELAB, SUPERHERO
from layout import create_layout
from dash import Dash, html
import ids
from dash.dependencies import Input, Output, State
from analysing_data_final import top_skills_employees
import plotly_express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import sys
SKILLS_DATA = top_skills_employees()

import os

def main() -> None:
    print(os.getcwd())
    app = Dash(external_stylesheets = [PULSE])
    app.title = "Skills Analysis Dashboard"
    app.layout = create_layout(app)
    @app.callback(
        Output(ids.BAR_CHART, "figure"),
        Input(ids.EMPLOYEE_DROPDOWN, "value")
    )
    def update_bar_chart(employee):
        df = SKILLS_DATA[SKILLS_DATA["Employee"] == employee]
        if df.shape[0] == 0:
            return html.Div("No data selected")

        fig = px.bar(df, x = "Word", y = "Count")
        return fig

    @app.callback(
        Output("modal", "is_open"),
        [Input("open", "n_clicks"), Input("close", "n_clicks")],
        [State("modal", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    app.run()

if __name__ == "__main__":
    main()