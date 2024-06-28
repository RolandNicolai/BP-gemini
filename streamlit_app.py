import streamlit as st
import pandas as pd
import numpy as np
import time
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account
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
        st.error("😕 Ukendt bruger eller adgangskode")
    return False


if not check_password():
    st.stop()

# Main Streamlit app starts here
LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE, link="https://bonnierpublications.com/en/bonnier-publications-2/")

# Page title
st.set_page_config(page_title='BP assistant', page_icon='⚙️')
st.title('Performance Marketing Assistant')

with st.expander('Om assistenten'):
  st.markdown('**Hvad kan denne assistent?**')
  st.info('This app allow users to build a machine learning (ML) model in an end-to-end workflow. Particularly, this encompasses data upload, data pre-processing, ML model building and post-model analysis.')

  st.markdown('**Opret en API nøgle**')
  st.warning('Find service account key: https://www.youtube.com/watch?v=I8W-4oq1onY&t=99s')

  st.markdown('**Under the hood**')
  st.markdown('Om')
  st.code('''Empty''', language='markdown')
  


# Sidebar for accepting input parameters
with st.sidebar:
    # Load data
    st.header('1. Kom i gang med assistenten')



credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)



vertexai.init(project=st.secrets["project"], location=st.secrets["location"], credentials=credentials)
model = GenerativeModel(
    "gemini-1.5-pro-001",
)


#queryModel_response = queryModel_response.text

user_prompt = st.text_input("User prompt:")
button = st.button("Generate")

if button and user_prompt:
    response = model.generate_content(user_prompt, 
                                      generation_config={"temperature": 0}, 
    )
    st.subheader("Svar: ")
    st.markdown(response.text)





 

# Initiate the model building process
