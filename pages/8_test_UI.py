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

import io
from PIL import Image
import tensorflow as tf
import streamlit as st



LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE)

st.header('Bonnier Data Assistent', divider='rainbow')

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)
client = bigquery.Client(credentials=credentials)

def printImages(results):
    image_results_list = list(results)
    amt_of_images = len(image_results_list)

    for i in range(amt_of_images):
        gcs_uri = image_results_list[i][0]
        text = image_results_list[i][1]
        
        # Load the image from Google Cloud Storage
        f = tf.io.gfile.GFile(gcs_uri, 'rb')
        stream = io.BytesIO(f.read())
        img = Image.open(stream)
        
        # Display the image and text in Streamlit
        st.image(img, caption=f"Image {i+1}")
        st.text(text)

# Streamlit app
st.title("Image Search Application")

# User input for search query
user_query = st.text_input("Enter your search query:")

# Button to perform the search
if st.button("Search"):
    if user_query:
        # Perform the search query
        search_query = f"""CREATE OR REPLACE TABLE `bonnier-deliverables.LLM_vertex.GDS_query_embeddings`
        AS
        SELECT * FROM ML.GENERATE_EMBEDDING(
        MODEL `bonnier-deliverables.ML_generate_text.ml_generate_text_v1`,
        (
            SELECT '{user_query}' AS content
        )
        );
        """

        client.query(search_query).result()

        results_query = """WITH query_embedding AS (
          SELECT ml_generate_embedding_result AS embedding
          FROM `bonnier-deliverables.LLM_vertex.GDS_query_embeddings`
        )

        SELECT
          base.uri,
          (1 - distance) AS similarity_score
        FROM
          VECTOR_SEARCH(
            TABLE `bonnier-deliverables.LLM_vertex.gds_images_embeddings`,
            'ml_generate_embedding_result',
            (SELECT embedding FROM query_embedding),
            top_k => 5,
            distance_type => 'COSINE'
          );"""

        # Execute the results query
        results_list = list(client.query(results_query).result())

        # Display the images using printImages function
        printImages(results_list)
    else:
        st.warning("Please enter a search query.")
