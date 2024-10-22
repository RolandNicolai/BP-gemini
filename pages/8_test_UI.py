import streamlit as st
from google.oauth2 import service_account
#from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import time
import datetime
import pytz

email = st.experimental_user.email

user_first_name = email.split(".")[0]

# Define the Copenhagen timezone
copenhagen_tz = pytz.timezone('Europe/Copenhagen')


# Get the current date and time in Copenhagen timezone
today = datetime.datetime.now(copenhagen_tz)

current_date_str = today.strftime('%Y-%m-%dT%H:%M:%S')


LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE)

st.header('Bonnier Data Assistent', divider='rainbow')


st.markdown(
    """
    <style>
    .stMarkdown code {
        color: blue;
        background-color: #f5f5f5;
    }
    .stMarkdown pre code {
        color: green;
        background-color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)
client = bigquery.Client(credentials=credentials)
maximum_bytes_billable = 100000000 # = 100 Mb

        
