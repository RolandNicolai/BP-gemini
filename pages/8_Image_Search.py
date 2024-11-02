import streamlit as st
from google.oauth2 import service_account
#from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import time
import datetime
import pytz
import streamlit as st
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
        gcs_uri = image_results_list[i][0]
        text = f"Similarity score: {image_results_list[i][1]:.2f}"
        
        # Convert GCS URI to HTTP URL
        http_url = convert_gcs_to_http(gcs_uri)
        
        # Fetch the image from the URI using requests
        response = requests.get(http_url)
        img = Image.open(BytesIO(response.content))
        
        # Resize the image to half of its original size
        original_width, original_height = img.size
        img_resized = img.resize((original_width // 2, original_height // 2))
        
        # Store the resized image and the text in the list
        images_and_text.append((img_resized, text, http_url))

    # Display images in a 2x2 layout
    cols = st.columns(2)  # Define two columns
    for idx, (img, text, http_url) in enumerate(images_and_text):
        col = cols[idx % 2]  # Alternate between columns
        with col:
            # Create a "card" effect with background and padding
            st.markdown(
                """
                <div style="
                    border-radius: 10px;
                    padding: 10px;
                    margin: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    background-color: #f9f9f9;
                    text-align: center;
                ">
                """,
                unsafe_allow_html=True
            )
            # Display the image
            st.image(img, use_column_width=True)

            # Display similarity score and link below the image
            st.markdown(
                f"""
                <p style='color: #555; font-size: 18px; font-weight: bold;'>{text}</p>
                <p style='color: #888; font-size: 14px;'>Billede Link: <a href='{http_url}'>{http_url}</a></p>
                """,
                unsafe_allow_html=True
            )
            
            # Close the "card" container
            st.markdown("</div>", unsafe_allow_html=True)
# Streamlit app
st.title("🌟 Billedsøgning 🌟")

# User input for search query
user_query = st.text_input("Indtast søgeord her:")

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
        st.warning("Indtast søgeord")
