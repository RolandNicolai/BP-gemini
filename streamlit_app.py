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


col1, col2, col3, col4 = st.columns([4, 1])
with col1:
    st.page_link("streamlit_app.py", label="Forside")
with col2:
    st.page_link("pages/1_Data_Assistent.py", label="Data Assistent")
with col3:
    st.page_link("pages/2_chat.py", label="Chat#2")
with col3:
    st.page_link("pages/3_chat.py", label="Chat#3")




        
