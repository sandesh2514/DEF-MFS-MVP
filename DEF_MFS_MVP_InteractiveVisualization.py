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
    import urllib.request, json
    import plotly.graph_objects as go
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

image_filename = 'stock_logo.jpg'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

image_filename1 = 'tesla.png'  # replace with your own image
encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())

resp = urllib.request.urlopen('https://query2.finance.yahoo.com/v10/finance/quoteSummary/tsla?modules=price')
data = json.loads(resp.read())
price = data['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw']
print(price)

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
                                         style={"padding-left": "35px"}))
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
                        dbc.NavLink(" Dashboard", href="/", active="exact", className="fa fa-dashboard"),
                        dbc.NavLink(" Analytics", href="/analytics", active="exact", className="fa fa-line-chart"),
                        dbc.NavLink(" Comparison", href="/comparison", active="exact", className="fa fa-exchange"),
                    ],
                    vertical=True,
                    pills=True,
                    className="mr-2"
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

        from datetime import date, timedelta
        import pandas_datareader.data as web

        start = date.today()-timedelta(days=1)
        now = date.today()

        df = web.DataReader("TSLA", 'yahoo', start, now)

        if pathname == "/":
            return [
                html.H4('Dashboard',
                        style={'textAlign': 'left'}),
                dbc.Container([
                    dbc.Row([
                        dcc.Graph(id='indicator-graph',
                                  figure=px.line(concatenated_df[concatenated_df['ticker'] == 'F'], x='Date',
                                                 y=['Volume']),
                                  style={"width": "600px", "height": "400px", "box-shadow": "0 6px 5px #aaaaaa"}),
                        dbc.Col([
                            dbc.CardImg(
                                src='data:image/png;base64,{}'.format(encoded_image1.decode()),
                                top=True,
                                style={"width": "6rem"}
                            ),
                            dbc.Row([
                                dbc.Label(id='high-price', children=now.strftime(" %Y-%m-%d"),
                                          className="fa fa-calendar"),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label(id='low-price', children="Open"),
                                ]),
                                dbc.Col([
                                    dbc.Label(id='high-price', children="Low"),
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label(id='low-price', children=(round(df['Open'], 2))),
                                ]),
                                dbc.Col([
                                    dbc.Label(id='high-price', children=(round(df['Low'], 2))),
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label(
                                        id='low-price', children="Close"),
                                ]),
                                dbc.Col([
                                    dbc.Label(id='high-price', children="High"),
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Label(id='low-price', children=(round(df['Close'], 2))),
                                ]),
                                dbc.Col([
                                    dbc.Label(id='high-price', children=(round(df['High'], 2))),
                                ])
                            ]),
                        ]),
                    ]),
                ]),
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

    # Indicator Graph
    # @app.callback(
    #     Output('indicator-graph', 'figure'),
    #     Input('update', 'n_intervals')
    #     )
    # def update_graph(timer):
    #     dff_rv = dff.iloc[::-1]
    #     day_start = dff_rv[dff_rv['date'] == dff_rv['date'].min()]['rate'].values[0]
    #     day_end = dff_rv[dff_rv['date'] == dff_rv['date'].max()]['rate'].values[0]
    #
    #     fig = go.Figure(go.Indicator(
    #         mode="delta",
    #         value=day_end,
    #         delta={'reference': day_start, 'relative': True, 'valueformat': '.2%'}))
    #     fig.update_traces(delta_font={'size': 12})
    #     fig.update_layout(height=30, width=70)
    #
    #     if day_end >= day_start:
    #         fig.update_traces(delta_increasing_color='green')
    #     elif day_end < day_start:
    #         fig.update_traces(delta_decreasing_color='red')
    #
    #     return fig


Visual = IntVisual()
Visual.read_data()
Visual.dash_board()

if __name__ == "__main__":
    app.run_server(debug=True)
