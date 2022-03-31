import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.4) pip install plotly==4.5.4
import plotly.express as px

import dash             #(version 1.9.1) pip install dash==1.9.1
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__)

#---------------------------------------------------------------
#Taken from https://opendata.cityofnewyork.us/
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Dash%20Components/Dropdown/Urban_Park_Ranger_Animal_Condition.csv")

app.layout = html.Div([

    dbc.Nav(
            [
                            dcc.Dropdown(id='demo-dropdown',
                                         options=[
                                             {'label': 'TSLA', 'value': 'Tesla'},
                                             {'label': 'F', 'value': 'ford'},
                                         ],
                                         ),
                            dbc.NavLink(" Analytics", href="/analytics", active="exact", className="fa fa-line-chart"),
                            dbc.NavLink(" Comparison", href="/comparison", active="exact", className="fa fa-exchange"),
            ],
            vertical=True,
            pills=True,
            className="mr-2"
         ),
        html.Div(id='dd-output-container')
    ])

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    if value == 'Tesla':
        return [html.H4('Tesla',
                        style={'textAlign': 'left'})]

    elif value == 'ford':
        return [html.H4('Ford',
                        style={'textAlign': 'left'})]

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)