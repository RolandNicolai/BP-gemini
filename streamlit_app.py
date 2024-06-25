import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
import zipfile

import hmac
import streamlit as st


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()

# Main Streamlit app starts here
st.write("Here goes your normal Streamlit app...")
st.button("Click me")

# Page title
st.set_page_config(page_title='Cobalt', page_icon='🤖')
st.title('🤖 Cobalt Assistant')

with st.expander('Om assistenten'):
  st.markdown('**Hvad kan denne assistent?**')
  st.info('This app allow users to build a machine learning (ML) model in an end-to-end workflow. Particularly, this encompasses data upload, data pre-processing, ML model building and post-model analysis.')

  st.markdown('**Hvordan bruger jeg denne applikation?**')
  st.warning('To engage with the app, go to the sidebar and 1. Select a data set and 2. Adjust the model parameters by adjusting the various slider widgets. As a result, this would initiate the ML model building process, display the model results as well as allowing users to download the generated models and accompanying data.')

  st.markdown('**Under the hood**')
  st.markdown('Data sets:')
  st.code('''- Drug solubility data set
  ''', language='markdown')
  


# Sidebar for accepting input parameters
with st.sidebar:
    # Load data
    st.header('1.1. Input data')

    st.markdown('**1. Use custom data**')
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, index_col=False)


"""
Working with cached data
    # Download example data
    @st.cache_data
    def convert_df(input_df):
        return input_df.to_csv(index=False).encode('utf-8')
    example_csv = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv')
    csv = convert_df(example_csv)
    st.download_button(
        label="Download example CSV",
        data=csv,
        file_name='delaney_solubility_with_descriptors.csv',
        mime='text/csv',
    )
"""

"""
for the Gemini model initiation
model = GModel(
    project="local-vehicle-415415", # replace with your project id
    location="us-central1", # keep this as is
    credentials_path="service_acc_key.json" # replace with your service account key file
)

response = model.generate_text("What is the meaning of life")
print(response)

"""
    # Select example data
 

# Initiate the model building process

