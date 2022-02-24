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

<<<<<<< HEAD
storage_client = storage.Client.from_service_account_json(
            'C:\\Users\\Raj\\PycharmProjects\\Sensitive_Info\\DEF-MFS-MVP-Configuration.json')

bucket = storage_client.get_bucket('bucket_stock')
df_list = []

class Storage:

    def __init__(self, files, UPLOADFILE):
        self.files=files
        self.UPLOADFILE=UPLOADFILE

    def upload_to_bucket(self):
        """ Upload data to a bucket"""
        blob = bucket.blob(self.files)
        blob.upload_from_filename(self.UPLOADFILE)

    def read_data(self):
=======
class Storage:

    def upload_to_bucket(self, blob_name, path_to_file):
        """ Upload data to a bucket"""

        # Explicitly use service account credentials by specifying the private key
        # file.
        storage_client = storage.Client.from_service_account_json(
            'C:\\Users\\Raj\\PycharmProjects\\Sensitive_Info\\DEF-MFS-MVP-Configuration.json')

        bucket = storage_client.get_bucket('bucket_stock')
        blob = bucket.blob(files)
        blob.upload_from_filename(UPLOADFILE)

>>>>>>> main
        # Getting all files from GCP bucket
        filename = [filename.name for filename in list(bucket.list_blobs(prefix=''))]

        # Reading a CSV file directly from GCP bucket
        for file in filename:
<<<<<<< HEAD
            df_list.append(pd.read_csv(
=======
            df = pd.read_csv(
>>>>>>> main
                io.BytesIO(
                    bucket.blob(blob_name = file).download_as_string()
                    ),
                    encoding = 'UTF-8',
                    sep = ',',
                    index_col=None
<<<<<<< HEAD
                ))

for files in glob.glob("*.csv"):
    UPLOADFILE = os.path.join(os.getcwd(), files)
    store = Storage(files, UPLOADFILE)
    store.upload_to_bucket()
    store.read_data()

concatenated_df = pd.concat(df_list, ignore_index=True)
print(concatenated_df)
=======
                )
            print(df.head())

        #returns a public url
        return blob.public_url

for files in glob.glob("*.csv"):
    UPLOADFILE = os.path.join(os.getcwd(), files)
    store = Storage()
    store.upload_to_bucket(files, UPLOADFILE)
>>>>>>> main
