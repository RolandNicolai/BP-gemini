import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel
import vertexai


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
    "gemini-1.5-flash-001",
    generation_config=generation_config,
)

#gemini-1.5-flash-001
#gemini-1.5-pro-001

if "vertex_model" not in st.session_state:
    st.session_state["vertex_model"] = model

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Hvad kan jeg hjælpe med?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using Vertex AI model
    with st.chat_message("assistant"):
        response = st.session_state["vertex_model"].generate_content(prompt)
        st.markdown(response.text)
        
    st.session_state.messages.append({"role": "assistant", "content": response.text})
