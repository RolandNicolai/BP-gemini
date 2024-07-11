from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account
import vertexai
import streamlit as st
from langchain.llms import VertexAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

#from langchain.agents import create_pandas_dataframe_agent


st.title("VertexAI assistant")

# Set OpenAI API key from Streamlit secrets
#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)


vertexai.init(project=st.secrets["project"], location=st.secrets["location"], credentials=credentials)

generation_config = {
  "temperature": 0,

  "max_output_tokens": 8192,
  #"response_mime_type": "text/plain",
}
model = GenerativeModel(
    "gemini-1.5-pro-001",
    generation_config=generation_config,
)

