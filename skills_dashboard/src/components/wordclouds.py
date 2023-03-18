from dash import Dash, dcc, html
import plotly.express as px
import ids
from dash.dependencies import Input, Output
import sys
import mpld3

#sys.path.insert(1, "../../../sharepoint_scrapper/")
from analysing_data_final import wordcloud_clusters

def render(app: Dash) -> html.Div:
    fig = wordcloud_clusters()
    plotly_fig = mpld3.fig_to_html(fig)
    return plotly_fig


