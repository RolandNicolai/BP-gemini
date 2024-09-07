import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
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
    st.title(":orange[God aften] " + first_name.capitalize())




with st.popover("Open popover"):
    st.markdown("Hello World 👋")
    name = st.text_input("What's your name?")

st.write("Your name:", name)


# Sample notebooks data
notebooks = [
    {"title": "Untitled notebook", "date": "6 Sept 2024", "sources": 2},
]

# Inject some custom CSS for styling
st.markdown("""
    <style>
    .notebook-card {
        background-color: #f9f9f9;
        padding: 15px;
        margin: 10px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    .notebook-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
        cursor: pointer;
    }
    .notebook-date {
        font-size: 14px;
        color: #555;
    }
    .notebook-btn {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 5px;
        cursor: pointer;
        margin-right: 5px;
    }
    .notebook-btn:hover {
        background-color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

# Iterate over each notebook and create an expander pop-up effect
for idx, notebook in enumerate(notebooks):
    with st.expander(f"📓 {notebook['title']} - {notebook['date']}"):
        # Display the notebook's detailed information and buttons inside the expanded view
        st.write(f"**Sources:** {notebook['sources']}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(f"Edit {notebook['title']}", key=f"edit_{idx}"):
                st.write(f"You clicked to edit: {notebook['title']}")
        
        with col2:
            if st.button(f"Delete {notebook['title']}", key=f"delete_{idx}"):
                st.write(f"You clicked to delete: {notebook['title']}")
        
        with col3:
            if st.button(f"View Sources for {notebook['title']}", key=f"view_{idx}"):
                st.write(f"Displaying sources for {notebook['title']}")

# Create a "New Notebook" button below all notebooks
st.markdown("""
    <div style="margin-top: 20px;">
        <button class="notebook-btn">Create New Notebook</button>
    </div>
""", unsafe_allow_html=True)

        
