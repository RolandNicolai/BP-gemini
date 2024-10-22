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

# Initialize session state if not already done
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

# Handle user interaction when a task block is clicked
def set_task(task_name):
    st.session_state['selected_task'] = task_name

# Task selection blocks
st.markdown("## Select a Task")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("", key="brainstorm_task"):
        set_task("Brainstorm")
    st.markdown(
        f"""
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
        f"""
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
        f"""
        <div class="task-box">
            <img src="https://img.icons8.com/ios/50/000000/read.png"/>
            <p class="task-text">Document Reader</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# Task-specific actions based on the selected task
if st.session_state['selected_task']:
    st.markdown(f"## You selected {st.session_state['selected_task']} mode")

    generation_config = {"temperature": 0.7, "max_output_tokens": 512}
    
    if st.session_state['selected_task'] == "Brainstorm":
        model_brainstorm = GenerativeModel("gemini-1.5-pro-001", generation_conf
