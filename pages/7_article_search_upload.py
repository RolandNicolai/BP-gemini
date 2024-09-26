import streamlit as st
import base64
from vertexai.generative_models import Part
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
import time



LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE)

st.header('Analysér dine dokumenter med GenAI', divider='rainbow')

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)
from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    with open(source_file_name, 'rb') as f:
        blob.upload_from_file(f)

    print(f"File {source_file_name} uploaded to {bucket_name}/{destination_blob_name}.")

# Replace these with your actual values
bucket_name = "vertex_search_assets"
source_file_name = "/content/image.png"  # Replace with your local file path
destination_blob_name = "your_file_in_bucket.txt"  # Replace with the desired name in the bucket

upload_blob(bucket_name, source_file_name, destination_blob_name)