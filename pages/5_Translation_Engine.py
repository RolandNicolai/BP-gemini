import streamlit as st
import base64
from vertexai.generative_models import Part
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
import time



LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE)

st.header('Oversæt tekster vha. AI', divider='rainbow')

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)

vertexai.init(project="bonnier-deliverables", location="europe-central2")
model = GenerativeModel("gemini-1.5-pro-001",
                       )

option_from = st.selectbox(
    "Oversæt fra",
    ("da", "fi", "no", "se"),
)

st.write("Oversæt fra:", option_from)

option_to = st.selectbox(
    "Oversæt til",
    ("da", "fi", "no", "se"),
)

st.write("Oversæt til:", option_to)

    

if 'translated_to' not in st.session_state:
    st.session_state['translated_to'] = ''

translation_text = st.text_input("Indtast tekst som ønskes oversat", "Lorem Ipsum", key="translation_text")
instructions = f"You are an expert Translator. You are tasked to translate documents from da to no.Please provide an accurate translation of this document and return translation text only:"




# Function to send the document to the AI model for analysis
def translate_with_model(document_part, model):
    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 0,
        "top_p": 0,
    }

   
    # Send the document and the analysis prompt to the AI model
    responses = model.generate_content(
        [instructions, translation_text],
        generation_config=generation_config,
    )

    # Collect and concatenate the model's responses
    translation_result = responses.text
    
    return translation_result

translate_button = st.button("Oversæt")

# If a file has been uploaded
if translate_button:
    # Display file details
    
    # Initialize the AI model

    # Analyze the document using the Vertex AI model
    st.write("Oversætter tekst...")
    
    # Process the uploaded file and create a document Part object
    

    translation_result = translate_with_model(translation_text, model)

    # Store the analysis result in session state
    st.session_state['translated_to'] = translation_result
    
    # Display the analysis result in a text area
    #st.text_area("Resultat", value=analysis_result, height=400)
st.text_area("Oversættelse", value=st.session_state['translated_to'], height=400)
