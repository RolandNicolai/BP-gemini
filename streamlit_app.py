import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import pandas as pd
from pandas import DataFrame
import numpy as np
import time


st.header('Bonnier GenAI sandbox', divider='rainbow')


st.subheader("Bygget på Google Gemini")

st.subheader("Vælg en applikation")


st.page_link("streamlit_app.py", label="Forside")
st.page_link("pages/1_Data_Assistent.py", label="Data Assistent")
st.page_link("pages/2_Chat1.py", label="Chat#1")
st.page_link("pages/3_Chat2.py", label="Chat#2")




        
