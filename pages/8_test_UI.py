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



def printImages(results):
    image_results_list = list(results)
    amt_of_images = len(image_results_list)

    for i in range(amt_of_images):
        # Get the GCS URI (which should be an HTTP URL) and the associated text
        gcs_uri = image_results_list[i][0]  # Example: 'https://storage.googleapis.com/your_bucket/your_image.jpg'
        text = image_results_list[i][1]
        
        # Fetch the image from the URI using requests
        response = requests.get(gcs_uri)
        img = Image.open(BytesIO(response.content))
        
        # Display the image in Streamlit
        st.image(img, caption=text, use_column_width=True)

# Example query to fetch the images (replace this with your actual query result fetching logic)
inspect_obj_table_query = """
SELECT uri, content_type
FROM LLM_vertex.gds_images
WHERE content_type = 'image/png'
Order by uri
LIMIT 10;
"""

# Assuming 'client.query' fetches the result set
# Replace the following line with the actual result from the query execution
results = client.query(inspect_obj_table_query)

# Display images using Streamlit
printImages(inspect_obj_table_query)

