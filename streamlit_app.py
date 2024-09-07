import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import pandas as pd
from pandas import DataFrame
import numpy as np
import time
import pytz
import datetime

# Define the Copenhagen timezone
copenhagen_tz = pytz.timezone('Europe/Copenhagen')

datetime_in_Lagos = datetime.now(pytz.timezone('Africa/Lagos'))

# Conditional statements based on the time of the day
if 6 <= current_hour < 12:
    st.write("Good morning!")
elif 12 <= current_hour < 18:
    st.write("Good afternoon!")
else:
    st.write("Good evening!")
name = get_name_from_db(st.experimental_user.email)
st.write('Hello, %s!' % name)


email = st.experimental_user.email

first_name = email.split(".")[0]
st.title(":orange[Godmorgen] " + first_name.capitalize())

st.write(first_name.capitalize())
st.subheader("Bygget på Google Gemini")

st.subheader("Vælg en applikation")


st.page_link("streamlit_app.py", label="Forside")
st.page_link("pages/1_Data_Assistent.py", label="Data Assistent")





        
