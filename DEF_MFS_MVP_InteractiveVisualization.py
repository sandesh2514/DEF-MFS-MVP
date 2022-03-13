try:
    # pip install --upgrade google-api-python-client
    # pip install --upgrade google-cloud-storage
    from google.cloud import storage
    import os
    import sys
    import glob
    import pandas as pd
    import io
    from io import BytesIO
    import dash
    from dash import html
    from dash import dcc
    import dash_bootstrap_components as dbc
    import plotly.express as px
    from dash.dependencies import Input, Output
    import base64
except Exception as e:
    print("Error : {} ".format(e))

storage_client = storage.Client.from_service_account_json(
    'C:\\Users\\Raj\\PycharmProjects\\Sensitive_Info\\DEF-MFS-MVP-Configuration.json')

bucket = storage_client.get_bucket('bucket_stock')

df_list = []

external_stylesheets = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets])

image_filename = 'stock_logo.jpg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

class IntVisual:

    def read_data(self):
        # Getting all files from GCP bucket
        filename = [filename.name for filename in list(bucket.list_blobs(prefix=''))]

        # Reading a CSV file directly from GCP bucket
        for file in filename:
            df_list.append(pd.read_csv(
                io.BytesIO(
                    bucket.blob(blob_name=file).download_as_string()
                ),
                encoding='UTF-8',
                sep=',',
                index_col=None
            ))

    def dash_board(self):

        # styling the sidebar
        SIDEBAR_STYLE = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "16rem",
            "padding": "2rem 1rem",
            "background-color": "#f8f9fa",
            "box-shadow": "1px 5px 10px  hsl(0deg 0% 0% / 0.38)",
        }

        # padding for the page content
        CONTENT_STYLE = {
            "margin-left": "18rem",
            "margin-right": "2rem",
            "padding": "2rem 1rem",
            "color": "grey"
        }

        # NAVBAR_STYLE={
        #     "box-shadow": "5px 10px 8px #888888",
        #     "width": 1600,
        #     "left": 0,
        #     "position": "fixed",
        #     "margin - top": "-20px",
        #     "height": "40px",
        #     "background - color":  "# 668284",
        # }

        concatenated_df = pd.concat(df_list, ignore_index=True)

        # navbar = dbc.NavbarSimple(
        #     children=[
        #         html.A(
        #             # Use row and col to control vertical alignment of logo / brand
        #             dbc.Row(
        #                 [
        #                     dbc.Col(html.Img(src='data:image/jpg;base64,{}'.format(encoded_image.decode()), height="60px")),
        #                     dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
        #                 ],
        #
        #             ),
        #             style=NAVBAR_STYLE,
        #         ),
        #     ],
        #     brand_href="#",
        #     color="Light",
        # )

        sidebar = html.Div(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(src='data:image/jpg;base64,{}'.format(encoded_image.decode()), height="140px",
                                         style={"padding-left":"35px"}))
                        ],

                    )
                ),
                html.Hr(),



                html.Li(
                    # use Row and Col components to position the chevrons
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.NavLink(className="fa fa-dashboard sm-1")
                            ),
                            dbc.Col("Dashboard"),
                        ],
                        className="mb-1",

                    ),
                    id="submenu-1",

                ),



                dbc.Nav(
                    [

                        dbc.NavLink(" Dashboard",href="/", active="exact", className="fa fa-dashboard"),
                        dbc.NavLink(" Analytics", href="/analytics", active="exact", className="fa fa-line-chart"),
                        dbc.NavLink(" Comparison", href="/comparison", active="exact", className="fa fa-exchange"),
                    ],
                    vertical=True,
                    pills=True,
                    className="ml-2"
                ),
            ],
            style=SIDEBAR_STYLE,
        )

        content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

        app.layout = html.Div([
            dcc.Location(id="url"),
            # navbar,
            sidebar,
            content
        ])

    @app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname")]
    )
    def render_page_content(pathname):
        concatenated_df = pd.concat(df_list, ignore_index=True)

        if pathname == "/":
            return [
                html.H4('Dashboard',
                        style={'textAlign': 'left'}),
                dcc.Graph(id='bargraph',
                          figure=px.bar(concatenated_df, barmode='group', x='Date',
                                        y=['Volume']))
            ]
        elif pathname == "/analytics":
            return [
                html.H4('Analytics',
                        style={'textAlign': 'left'}),
                dcc.Graph(id='bargraph',
                          figure=px.bar(concatenated_df, barmode='group', x='Date',
                                        y=['Volume']))
            ]
        elif pathname == "/comparison":
            return [
                html.H4('Comparison',
                        style={'textAlign': 'left'}),
                dcc.Graph(id='bargraph',
                          figure=px.bar(concatenated_df, barmode='group', x='Date',
                                        y=['Volume']))
            ]
        # If the user tries to reach a different page, return a 404 message
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )


Visual = IntVisual()
Visual.read_data()
Visual.dash_board()

if __name__ == "__main__":
    app.run_server(debug=True)
