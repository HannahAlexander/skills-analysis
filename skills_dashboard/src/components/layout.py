from cProfile import label
from pydoc import classname
from dash import Dash, html, dcc
import cluster_plot
import employee_dropdown
import wordclouds
import ids
from analysing_data_final import get_employee_names
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly_express as px

from analysing_data_final import top_skills_employees

SKILLS_DATA = top_skills_employees()

def create_layout(app: Dash) -> html.Div:

    return dcc.Tabs([
        dcc.Tab(label='Clustering', children=[
            html.H1([app.title], className="container_title"),
            dbc.Row(
                [
                    dbc.Col(html.Div([
                        employee_dropdown.render(app),
                        dbc.Button("View Employee Skills", id="open", n_clicks=0),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(dbc.ModalTitle("Top 10 Employee Skills")),
                                        dbc.ModalBody(html.Div([
                                            dcc.Graph(id=ids.BAR_CHART)])),
                                        dbc.ModalFooter(
                                            dbc.Button(
                                                "Close", id="close", className="ms-auto", n_clicks=0
                                            )
                                        ),
                                    ],
                                    id="modal",
                                    is_open=False,
                            
                        )
                        ]),
                    width = {'size': 3, 'offset': 0}
                    )
                ],
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                                    [
                                        cluster_plot.render(app)
                                     ], className = "nine columns pretty_container"
                                        ), width = {'size': 6, 'offset': 1, 'order': 1},
                                    ),
                                    
                    dbc.Col(
                        html.Div(
                                    [
                                            dbc.CardImg(src='/assets/wordclouds.png')
                                            ], className = "four columns pretty_container"
                                        ), width = {'size': 4, 'offset': 0, 'order': 2},
                                     ),
                                    
                                
                ]
                )
        ],
        ),
        dcc.Tab(label = "glassdoor")
        ])
        