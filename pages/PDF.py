import streamlit as st
import base64
from vertexai.generative_models import Part
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
import time



LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE)

st.header('Artikel', divider='rainbow')

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)

vertexai.init(project="bonnier-deliverables", location="europe-central2")
model = GenerativeModel("gemini-1.5-flash-001",
                       system_instruction = ["You are a helpful assistant"])

# Function to process the uploaded file using base64 decoding and Part.from_data
def process_uploaded_file(uploaded_file):
    # Read the file content as binary
    file_content = uploaded_file.read()
    
    # Encode file content in base64 (if needed, otherwise use as is)
    file_base64 = base64.b64encode(file_content).decode('utf-8')
    
    # Decode the base64 encoded content back to binary for processing
    file_data = base64.b64decode(file_base64)
    
    # Create a Part object with the decoded file data
    document_part = Part.from_data(
        mime_type="application/pdf",  # Assuming a PDF file
        data=file_data
    )
    
    return document_part

# Streamlit app for file upload and processing
st.title("PDF Upload and Processing")

# File uploader widget - allows only PDF uploads
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# If a file has been uploaded
if uploaded_file is not None:
    # Display file details
    st.write(f"Filename: {uploaded_file.name}")
    st.write(f"File size: {uploaded_file.size} bytes")
    
    # Process the uploaded file
    processed_document = process_uploaded_file(uploaded_file)
    
    # Display confirmation that the file has been processed
    st.success("File uploaded and processed successfully!")


responses = model.generate_content(
    [uploaded_file, """analyze this document:"""],
)
