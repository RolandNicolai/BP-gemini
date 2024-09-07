import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import pandas as pd
from pandas import DataFrame
import numpy as np
import time
import datetime
import pytz

# Define the Copenhagen timezone
copenhagen_tz = pytz.timezone('Europe/Copenhagen')

# Get the current date and time in Copenhagen timezone
today = datetime.datetime.now(copenhagen_tz)

current_date_str = today.strftime('%H:%M:%S')

st.write(current_date_str)



email = st.experimental_user.email

first_name = email.split(".")[0]
st.title(":orange[Godmorgen] " + first_name.capitalize())

st.write(first_name.capitalize())
st.subheader("Bygget på Google Gemini")

st.subheader("Vælg en applikation")


st.page_link("streamlit_app.py", label="Forside")
st.page_link("pages/1_Data_Assistent.py", label="Data Assistent")





        
