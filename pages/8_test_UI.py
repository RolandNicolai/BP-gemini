import streamlit as st
from google.oauth2 import service_account
#from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import time
import datetime
import pytz
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)
client = bigquery.Client(credentials=credentials)




def convert_gcs_to_http(gcs_uri):
    # Replace 'gs://' with 'https://storage.googleapis.com/'
    return gcs_uri.replace('gs://', 'https://storage.googleapis.com/')


def printImages(results):
    image_results_list = list(results)
    amt_of_images = len(image_results_list)

    # Create a list to store fetched images and their corresponding text
    images_and_text = []

    # Fetch all images first
    for i in range(amt_of_images):
        # Get the GCS URI and similarity score
        gcs_uri = image_results_list[i][0]  # Example: 'gs://vertex_search_images/graestrimmer.png'
        text = f"Similarity score: {image_results_list[i][1]}"  # Display the similarity score
        
        # Convert GCS URI to HTTP URL
        http_url = convert_gcs_to_http(gcs_uri)
        
        # Fetch the image from the URI using requests
        response = requests.get(http_url)
        img = Image.open(BytesIO(response.content))
        
        # Get the original size of the image
        original_width, original_height = img.size
        
        # Resize the image to half its original size
        img_resized = img.resize((original_width // 2, original_height // 2))
        
        # Store the resized image and the text in the list
        images_and_text.append((img_resized, text))

    # Display all images at once in columns (5 images per row)
    cols = st.columns(5)
    
    for i, (img, text) in enumerate(images_and_text):
        with cols[i % 5]:  # Use modulus to loop across 5 columns
            st.image(img, caption=text)
            

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
        results = client.query(results_query)


        # Display the images using printImages function
        printImages(results)
    else:
        st.warning("Please enter a search query.")


