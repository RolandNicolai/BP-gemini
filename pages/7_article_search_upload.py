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
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {bucket_name}/{destination_blob_name}.")

# Replace these with your actual values
bucket_name = "vertex_search_assets"
#source_file_name = "/content/image.png"  # Replace with your local file path
#destination_blob_name = "your_file_in_bucket.txt"  # Replace with the desired name in the bucket

input_name = st.text_input("navn på din fil", "Lorem Ipsum", key="translated_from")
destination_blob_name = (input_name + ".pdf")
source_file_name = st.file_uploader("vælg din fil", type="pdf")

if st.button("Upload fil"):
    upload_blob(bucket_name, source_file_name, destination_blob_name)
    #st.write((f"File {source_file_name} uploaded to {bucket_name}/{destination_blob_name}.")
