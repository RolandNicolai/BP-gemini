import streamlit as st
from google.oauth2 import service_account
#from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import time
import datetime
import pytz
import io
from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf
import matplotlib.pyplot as plt


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)
client = bigquery.Client(credentials=credentials)

import io
from PIL import Image
import streamlit as st
from google.cloud import storage

# Initialize the Google Cloud Storage client
storage_client = storage.Client()

def read_image_from_gcs(gcs_uri):
    # Extract bucket name and blob name from the GCS URI
    parts = gcs_uri.replace("gs://", "").split("/", 1)
    bucket_name = parts[0]
    blob_name = parts[1]
    
    # Get the bucket and blob objects
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Download the image data as a bytes stream
    img_bytes = blob.download_as_bytes()
    img = Image.open(io.BytesIO(img_bytes))
    return img

def printImages(results):
    image_results_list = list(results)
    amt_of_images = len(image_results_list)

    for i in range(amt_of_images):
        gcs_uri = image_results_list[i][0]
        text = image_results_list[i][1]
        
        # Use the new GCS reading function
        img = read_image_from_gcs(gcs_uri)
        
        # Display the image and text in Streamlit
        st.image(img, caption=text, use_column_width=True)
        st.text(text)

# Query to fetch the images
inspect_obj_table_query = """
SELECT uri, content_type
FROM LLM_vertex.gds_images
WHERE content_type = 'image/png'
Order by uri
LIMIT 10;
"""

# Execute the query and print the images
printImages(client.query(inspect_obj_table_query))


