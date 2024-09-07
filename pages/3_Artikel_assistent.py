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
import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.generative_models as generative_models

# Initialize Vertex AI with your project and location
def initialize_vertex_model():
    vertexai.init(project="bonnier-deliverables", location="europe-central2")
    model = GenerativeModel("gemini-1.5-flash-001")
    return model

# Function to generate chat content based on user input
def generate_response(chat, user_message, generation_config, safety_settings):
    # Send the user's message to the model
    response = chat.send_message(
        user_message,
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    # Return the model's response as text
    return response

# Configuration settings for model output and safety
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

# Initialize Vertex AI generative model
model = initialize_vertex_model()
chat = model.start_chat()

# Streamlit Chat Interface
st.title("AI Chat Interface with Vertex AI")

# List to store chat history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Get user input via chat
user_message = st.chat_input("Type your message here...")

# If user sends a message
if user_message:
    # Display user's message
    st.chat_message("user").markdown(user_message)

    # Add user's message to chat history
    st.session_state["history"].append({"role": "user", "content": user_message})

    # Generate AI response
    ai_response = generate_response(chat, [user_message], generation_config, safety_settings)

    # Display AI's response
    st.chat_message("assistant").markdown(ai_response.text)

    # Add AI's response to chat history
    st.session_state["history"].append({"role": "assistant", "content": ai_response.text})

# Display chat history (preserves messages between interactions)
for message in st.session_state["history"]:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    else:
        st.chat_message("assistant").markdown(message["content"])
