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



# Initialize Vertex AI with your project and location
def initialize_vertex_model():
    vertexai.init(project="bonnier-deliverables", location="europe-central2")
    model = GenerativeModel("gemini-1.5-flash-001",
                           system_instruction=["""Youm are a helpful assistant. Always only reply in danish"""])
    return model

# Function to generate chat content with memory (entire conversation context)
def generate_response(chat, conversation_history, generation_config):
    # Flatten the conversation history into one string for AI input context
    conversation_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    
    # Send the conversation context to the AI model
    response = chat.send_message(
        conversation_context,
        generation_config=generation_config,
    )
    return response

# Configuration settings for model output and safety
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}



# Initialize Vertex AI generative model
model = initialize_vertex_model()
chat = model.start_chat()

# Streamlit Chat Interface
st.title("AI Chat Interface with Vertex AI Memory")

# Initialize conversation history if not present in session_state
if "history" not in st.session_state:
    st.session_state["history"] = []

# Get user input via chat
user_message = st.chat_input("Type your message here...")

# If user sends a message
if user_message:
    # Add user's message to chat history
    st.session_state["history"].append({"role": "user", "content": user_message})
    
    # Display user's message in the chat (no need to loop over history here)
    st.chat_message("user").markdown(user_message)

    # Generate AI response, considering the conversation history
    ai_response = generate_response(chat, st.session_state["history"], generation_config)
    
    # Display AI's response in the chat
    st.chat_message("assistant").markdown(ai_response.text)

    # Add AI's response to chat history
    st.session_state["history"].append({"role": "assistant", "content": ai_response.text})

# Display entire chat history (without re-displaying the last messages that were just sent)
for message in st.session_state["history"][:1]:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    else:
        st.chat_message("assistant").markdown(message["content"])
