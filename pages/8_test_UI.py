import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel
import vertexai
import datetime
import pytz

# Custom CSS for clickable block components
st.markdown(
    """
    <style>
    .task-box {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.3s;
        cursor: pointer;
    }
    
    .task-box:hover {
        transform: translateY(-10px);
        box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    .task-box img {
        width: 50px;
        margin-bottom: 10px;
    }
    
    .task-text {
        font-size: 18px;
        font-weight: bold;
        color: #333;
    }

    .selected-box {
        background-color: #f0f0f0;
        box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
        transform: translateY(-10px);
    }
    
    </style>
    """, 
    unsafe_allow_html=True
)

# Initialize session state to store the selected task
if 'selected_task' not in st.session_state:
    st.session_state['selected_task'] = None

# Logo and header
LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.image(LOGO_URL_LARGE)
st.header('Bonnier Data Assistant', divider='rainbow')

# Define timezone and current time
copenhagen_tz = pytz.timezone('Europe/Copenhagen')
today = datetime.datetime.now(copenhagen_tz)
current_date_str = today.strftime('%Y-%m-%dT%H:%M:%S')

# Authenticate credentials
credentials = service_account.Credentials.from_service_account_info(st.secrets["vertexAI_service_account"])
vertexai.init(project=st.secrets["project"], location=st.secrets["location"], credentials=credentials)

# Task selection function
def set_task(task_name):
    st.session_state['selected_task'] = task_name

# Task selection using visual blocks (simulated click with session state)
st.markdown("## Select a Task")
col1, col2, col3 = st.columns(3)

# Interactive task boxes
with col1:
    if st.button("", key="brainstorm_task"):
        set_task("Brainstorm")
    st.markdown(
        """
        <div class="task-box">
            <img src="https://img.icons8.com/ios/50/000000/idea.png"/>
            <p class="task-text">Brainstorm</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col2:
    if st.button("", key="article_task"):
        set_task("Article Writer")
    st.markdown(
        """
        <div class="task-box">
            <img src="https://img.icons8.com/ios/50/000000/typewriter-with-paper.png"/>
            <p class="task-text">Article Writer</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

with col3:
    if st.button("", key="reader_task"):
        set_task("Document Reader")
    st.markdown(
        """
        <div class="task-box">
            <img src="https://img.icons8.com/ios/50/000000/read.png"/>
            <p class="task-text">Document Reader</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Load different models based on the selected task
if st.session_state['selected_task']:
    st.markdown(f"## You selected {st.session_state['selected_task']} mode")

    generation_config = {"temperature": 0.7, "max_output_tokens": 512}
    
    if st.session_state['selected_task'] == "Brainstorm":
        model_brainstorm = GenerativeModel("gemini-1.5-pro-001", generation_config=generation_config)
        prompt = st.text_input("Enter your brainstorming topic")
        if prompt:
            chat = model_brainstorm.start_chat()
            response = chat.send_message(prompt).candidates[0].content
            st.write(response)
            
    elif st.session_state['selected_task'] == "Article Writer":
        model_writer = GenerativeModel("gemini-1.5-pro-002", generation_config=generation_config)
        prompt = st.text_input("Enter the article topic")
        if prompt:
            chat = model_writer.start_chat()
            response = chat.send_message(prompt).candidates[0].content
            st.write(response)
    
    elif st.session_state['selected_task'] == "Document Reader":
        model_reader = GenerativeModel("gemini-1.5-pro-003", generation_config=generation_config)
        uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])
        if uploaded_file:
            chat = model_reader.start_chat()
            doc_content = uploaded_file.read().decode("utf-8") if uploaded_file.type == "text/plain" else "PDF file uploaded."
            response = chat.send_message(f"Summarize the following document: {doc_content}").candidates[0].content
            st.write(response)
