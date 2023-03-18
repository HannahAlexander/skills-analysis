from dash import Dash, dcc, html
import plotly.express as px
import ids
from dash.dependencies import Input, Output
import sys
import mpld3

#sys.path.insert(1, "../../../sharepoint_scrapper/")
from analysing_data_final import plotly_clusters

def render(app: Dash) -> html.Div:
    fig = plotly_clusters()
    #fig.update_layout(width = 900, height = 700)
    #fig.update_layout(
    #    margin=dict(l=10, r=10, t=50, b=10),
    #    paper_bgcolor="White",)
    return html.Div(dcc.Graph(figure = fig), id = ids.CLUSTER_PLOT)