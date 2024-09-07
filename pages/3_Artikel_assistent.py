import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import time
import datetime
import pytz

# Define the Copenhagen timezone
copenhagen_tz = pytz.timezone('Europe/Copenhagen')


# Get the current date and time in Copenhagen timezone
today = datetime.datetime.now(copenhagen_tz)

current_date_str = today.strftime('%Y-%m-%dT%H:%M:%S')


LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE)

st.header('Artikel', divider='rainbow')





credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)
client = bigquery.Client(credentials=credentials)
maximum_bytes_billable = 100000000 # = 100 Mb


vertexai.init(project=st.secrets["project"], location=st.secrets["location"], credentials=credentials)
