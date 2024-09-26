import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage

LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.image(LOGO_URL_LARGE)

st.header('Upload dine dokumenter til arkivet', divider='rainbow')

# Setup Google Cloud credentials
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)

def upload_blob(bucket_name, file_obj, destination_blob_name):
    """Uploads a file to the bucket from a file-like object."""
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    # Upload the file directly from the file-like object
    blob.upload_from_file(file_obj, content_type="application/pdf")
    
    st.write(f"File uploaded to {bucket_name}/{destination_blob_name}.")

# Streamlit file uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# File name in cloud storage
destination_blob_name = "test1.pdf"

# Handle file upload when button is clicked
if st.button("Upload fil"):
    if uploaded_file is not None:
        # Call the upload_blob function with the file object
        upload_blob("vertex_search_assets", uploaded_file, destination_blob_name)
    else:
        st.error("No file uploaded. Please upload a PDF file.")
