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
    import plotly.express as px
except Exception as e:
    print("Error : {} ".format(e))

storage_client = storage.Client.from_service_account_json(
            'C:\\Users\\Raj\\PycharmProjects\\Sensitive_Info\\DEF-MFS-MVP-Configuration.json')

bucket = storage_client.get_bucket('bucket_stock')
df_list = []

app = dash.Dash(__name__)

class IntVisual:


    def read_data(self):
        # Getting all files from GCP bucket
        filename = [filename.name for filename in list(bucket.list_blobs(prefix=''))]

        # Reading a CSV file directly from GCP bucket
        for file in filename:
            df_list.append(pd.read_csv(
                io.BytesIO(
                    bucket.blob(blob_name = file).download_as_string()
                    ),
                    encoding = 'UTF-8',
                    sep = ',',
                    index_col=None
                ))

    def dash_board(self):
        concatenated_df = pd.concat(df_list, ignore_index=True)
        fig =px.line(concatenated_df, x="Date", y="Volume", title="Stock of Tesla")
        app.title="Stock Prices"

        app.layout = html.Div(
            id="app-container",
            children=[
                html.H1("Stock of Tesla"),
                html.P("Results in USD/oz"),
                dcc.Graph(figure=fig)
            ]
        )

Visual = IntVisual()
Visual.read_data()
Visual.dash_board()

if __name__ == "__main__":
    app.run_server(debug=True)

# concatenated_df = pd.concat(df_list, ignore_index=True)
# print(concatenated_df)

