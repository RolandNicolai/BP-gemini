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
from datetime import datetime

# Define the Copenhagen timezone
copenhagen_tz = pytz.timezone('Europe/Copenhagen')

# Get the current time in Copenhagen
current_time_copenhagen = datetime.now(pytz.utc).astimezone(copenhagen_tz)

# Extract the hour part as an integer
current_hour = current_time_copenhagen.hour

email = st.experimental_user.email

first_name = email.split(".")[0]

# Conditional statements based on the time of the day
if 6 <= current_hour < 10:
    st.title(":orange[Godmorgen] " + first_name.capitalize())
elif 10<= current_hour < 12:
    st.title(":orange[God formiddag] " + first_name.capitalize())
elif 12 <= current_hour < 18:
    st.title(":orange[God eftermiddag] " + first_name.capitalize())
else:
    st.write("God aften" + first_name.capitalize())







st.page_link("streamlit_app.py", label="Forside")
st.page_link("pages/1_Data_Assistent.py", label="Data Assistent")

# Sample notebooks data (this would be dynamic or fetched in a real app)
notebooks = [
    {"title": "Untitled notebook", "date": "6 Sept 2024", "sources": 2},
    {"title": "Untitled notebook", "date": "6 Sept 2024", "sources": 1},
    {"title": "Untitled notebook", "date": "2 Sept 2024", "sources": 1},
    {"title": "Internationalisation of SMEs", "date": "25 Jun 2024", "sources": 2},
    {"title": "Systemic Wisdom", "date": "8 Jun 2024", "sources": 2},
    {"title": "Internationalization", "date": "4 Jul 2024", "sources": 1},
    {"title": "Runaway Blitzscaling", "date": "8 Jun 2024", "sources": 2},
]

# Page heading
st.title("My Notebooks")

# Create a grid layout for notebooks
cols = st.columns(2)  # Two columns for a grid-like structure

# Loop over notebooks and display them in the interface
for idx, notebook in enumerate(notebooks):
    # Alternate between columns
    col = cols[idx % 2]
    
    # Create an expander for each notebook
    with col.expander(f"{notebook['title']} - {notebook['date']}"):
        st.write(f"Sources: {notebook['sources']}")
        
        # Add interactive buttons for actions
        if st.button(f"Edit {notebook['title']}", key=f"edit_{idx}"):
            st.write(f"You clicked to edit: {notebook['title']}")
        
        if st.button(f"Delete {notebook['title']}", key=f"delete_{idx}"):
            st.write(f"You clicked to delete: {notebook['title']}")
        
        if st.button(f"View Sources for {notebook['title']}", key=f"view_{idx}"):
            st.write(f"Displaying sources for {notebook['title']}")
        
# Add a "New Notebook" button at the top or bottom
if st.button("Create New Notebook"):
    st.write("You clicked to create a new notebook!")





        
