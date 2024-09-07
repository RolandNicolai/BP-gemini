import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import time



LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE)

st.header('Artikel', divider='rainbow')

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)

vertexai.init(project=st.secrets["project"], location=st.secrets["location"], credentials=credentials)

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.generative_models as generative_models


def multiturn_generate_content():
  vertexai.init(project="bonnier-deliverables", location="europe-central2")
  model = GenerativeModel(
    "gemini-1.5-flash-001",
  )
  chat = model.start_chat()
  print(chat.send_message(
      ["""hej"""],
      generation_config=generation_config,
      safety_settings=safety_settings
  ))
  print(chat.send_message(
      ["""hej"""],
      generation_config=generation_config,
      safety_settings=safety_settings
  ))
  print(chat.send_message(
      ["""kan du hjælpe"""],
      generation_config=generation_config,
      safety_settings=safety_settings
  ))


generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

multiturn_generate_content('hej')
