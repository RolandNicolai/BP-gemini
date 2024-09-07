import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import pandas as pd
from pandas import DataFrame
import numpy as np
import time



email = st.experimental_user.email

first_name = email.split(".")[0]
st.title("Goodmorning :blue[cool]" + first_name.capitalize())

st.write(first_name.capitalize())
st.subheader("Bygget på Google Gemini")

st.subheader("Vælg en applikation")


st.page_link("streamlit_app.py", label="Forside")
st.page_link("pages/1_Data_Assistent.py", label="Data Assistent")





        
