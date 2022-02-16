try:
    # pip install --upgrade google-api-python-client
    # pip install --upgrade google-cloud-storage
    from google.cloud import storage
    import google.cloud.storage
    import json
    import os
    import sys
    import glob
    import pandas as pd
    import io
    from io import BytesIO
except Exception as e:
    print("Error : {} ".format(e))

PATH = os.path.join(os.getcwd() , 'C:\\Users\\Raj\\PycharmProjects\\Sensitive_Info\\DEF-MFS-MVP-Configuration.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH

# Create a Client Object
storage_client = storage.Client(PATH)

# Pushing a file on GCP bucket
for files in glob.glob("*.csv"):
    UPLOADFILE = os.path.join(os.getcwd(), files)
    bucket = storage_client.get_bucket('bucket_stock')
    blob = bucket.blob(files)
    blob.upload_from_filename(UPLOADFILE)

# Getting all files from GCP bucket
bucket = storage_client.get_bucket('bucket_stock')
filename = [filename.name for filename in list(bucket.list_blobs(prefix=''))]

# Reading a CSV file directly from GCP bucket
for file in filename:
    df = pd.read_csv(
        io.BytesIO(
            bucket.blob(blob_name = file).download_as_string()
            ),
            encoding = 'UTF-8',
            sep = ',',
            index_col=None
        )
    print(df.head())
