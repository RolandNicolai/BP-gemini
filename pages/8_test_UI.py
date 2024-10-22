import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import pytz
import datetime

# Get the current date and time in Copenhagen timezone
copenhagen_tz = pytz.timezone('Europe/Copenhagen')
today = datetime.datetime.now(copenhagen_tz)
current_date_str = today.strftime('%Y-%m-%dT%H:%M:%S')

# Logo and header
LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.image(LOGO_URL_LARGE)
st.header('Bonnier Data Assistent', divider='rainbow')

# Authenticate credentials
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)
client = bigquery.Client(credentials=credentials)
vertexai.init(project=st.secrets["project"], location=st.secrets["location"], credentials=credentials)

# Create the task buttons
st.markdown("## Select Your Task")
task = st.radio(
    "Choose a task",
    ("Brainstorm", "Article Writer", "Document Reader"),
    horizontal=True
)

# Define the prompts and routing to different models
def handle_brainstorm():
    st.markdown("### Brainstorm Mode")
    prompt = st.text_input("What would you like to brainstorm?")
    if prompt:
        chat = model_brainstorm.start_chat()
        response = chat.send_message(prompt).candidates[0].content
        st.write(response)

def handle_article_writer():
    st.markdown("### Article Writer Mode")
    prompt = st.text_input("Provide a topic for the article")
    if prompt:
        chat = model_writer.start_chat()
        response = chat.send_message(prompt).candidates[0].content
        st.write(response)

def handle_document_reader():
    st.markdown("### Document Reader Mode")
    uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])
    if uploaded_file:
        chat = model_reader.start_chat()
        response = chat.send_message(f"Summarize the following document: {uploaded_file.read()}").candidates[0].content
        st.write(response)

# Load different models for different tasks
generation_config = {
    "temperature": 0.7,
    "max_output_tokens": 512,
}

# Instantiate separate models for different tasks
model_brainstorm = GenerativeModel("gemini-1.5-pro-001", generation_config=generation_config)
model_writer = GenerativeModel("gemini-1.5-pro-002", generation_config=generation_config)
model_reader = GenerativeModel("gemini-1.5-pro-003", generation_config=generation_config)

# Route the user based on their selection
if task == "Brainstorm":
    handle_brainstorm()
elif task == "Article Writer":
    handle_article_writer()
elif task == "Document Reader":
    handle_document_reader()
