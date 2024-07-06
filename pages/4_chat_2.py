from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account
import vertexai
import streamlit as st

st.title("ChatGPT-like clone (Vertex AI)")

if "messages" not in st.session_state:
    st.session_state.messages = [
        ChatMessage(
            content="Hi! 👋 I'm a helpful AI assistant. Ask me anything.",
            role="assistant"
        ),
    ]

for message in st.session_state.messages:
    with st.chat_message(message.role):
        st.markdown(message.content)

if prompt := st.chat_input(""):
    st.session_state.messages.append(ChatMessage(content=prompt, role="user"))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        for response in chat_model.stream_generate_content(
            messages=st.session_state.messages,
        ):
            full_response += response.text
            response_placeholder.markdown(full_response, unsafe_allow_html=True)

        st.session_state.messages.append(
            ChatMessage(content=full_response, role="assistant")
        )
