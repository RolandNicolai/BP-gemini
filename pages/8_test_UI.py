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


def printImages(results):
    image_results_list = list(results)
    amt_of_images = len(image_results_list)

    for i in range(amt_of_images):
        gcs_uri = image_results_list[i][0]
        text = image_results_list[i][1]
        
        # Read the image from the GCS URI
        f = tf.io.gfile.GFile(gcs_uri, 'rb')
        stream = io.BytesIO(f.read())
        img = Image.open(stream)
        
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

