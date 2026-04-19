import dash
from dash import Input, Output, State, callback
import dash_mantine_components as dmc

dash.register_page(__name__, path="/")

layout = [
    dmc.Title("Home Page", c="blue"),
]



