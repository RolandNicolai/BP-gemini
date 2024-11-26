import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
import time
import pytz
from datetime import datetime
import random


LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE)
# Define the Copenhagen timezone
copenhagen_tz = pytz.timezone('Europe/Copenhagen')

# Get the current time in Copenhagen
current_time_copenhagen = datetime.now(pytz.utc).astimezone(copenhagen_tz)

# Extract the hour part as an integer
current_hour = current_time_copenhagen.hour

email = str(st.experimental_user.email)
first_name = email.split(".")[0]

# Conditional statements based on the time of the day
if 6 <= current_hour < 10:
    st.title(":orange[Godmorgen] " + first_name.capitalize())
elif 10<= current_hour < 12:
    st.title(":orange[God formiddag] " + first_name.capitalize())
elif 12 <= current_hour < 18:
    st.title(":orange[God eftermiddag] " + first_name.capitalize())
else:
    st.title(":orange[Godaften] " + first_name.capitalize())

# List of quotes from renowned scientists and classical music artists
quotes = [
    "Imagination is more important than knowledge. For knowledge is limited, whereas imagination embraces the entire world. :orange[- Albert Einstein]",
    "Nothing in life is to be feared, it is only to be understood. Now is the time to understand more, so that we may fear less. :orange[- Marie Curie]",
    "If I have seen further, it is by standing on the shoulders of giants. :orange[- Isaac Newton]",
    "I would rather have questions that can't be answered than answers that can't be questioned. :orange[- Richard Feynman]",
    "Works of art make rules; rules do not make works of art. :orange[-Claude Debussy]",
    "A computer would deserve to be called intelligent if it could deceive a human into believing that it was human. :orange[- Alan Turing]",
    "The most dangerous phrase in the language is, ‘We’ve always done it this way.’ :orange[- Grace Hopper]",
]

# Function to get a random quote
def get_random_quote():
    return random.choice(quotes)

# Streamlit app
def main():
    # Display a random quote in st.caption
    random_quote = get_random_quote()
    st.caption(f"> {random_quote}")

main()



# Custom CSS to style the boxes
st.markdown(
    """
    <style>
    
    .priority-box {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .priority-box img {
        width: 100px;
    }
    
    .info-text {
        font-size: 18px;
        color: #333;
    }

    </style>
    """, unsafe_allow_html=True
)


# Priority message box
st.markdown(
    """
    <div class="priority-box">
        <div>
            <p class="info-text">Anbefalinger til dig:</p>
            <p class="info-text">- Træk data fra vores datawarehouse vha. AI genererede queries.</p>
            <p class="info-text">- Få hjælp til at skrive SQL queries</p>
            <p class="info-text">- Oværsæt tekster </p>

    </div>
    """, unsafe_allow_html=True
)

st.divider()
with st.popover("Om applikationen - Sikkerhed/Modeller"):
    st.markdown("""Denne app bygger på Google's katalog af Generative AI modeller herunder: Gemini-1.5-Pro og Gemini-1.5-Flash for at løse forskellige opgaver.
    Dette indebærer at én bruger skal være bevidst om at systemet til tider kan genererer usande/ ikke faktuelle svar.
    \n- Per default trænes Google's foundation modeller ikke igennem Google cloud. Dette indebærer både brugerens prompts/indhold samt modellens svar, se nærmere herfor i Google' data governance: 
    https://cloud.google.com/vertex-ai/generative-ai/docs/data-governance#foundation_model_training""")
    #st.divider()
    #st.markdown("Test 2 👋")
    #st.divider()


# Title for the app

# Embed the HTML and JavaScript
widget_code = """
<!-- Widget JavaScript bundle -->
<script src="https://cloud.google.com/ai/gen-app-builder/client?hl=en_GB"></script>

<!-- Search widget element is not visible by default -->
<gen-search-widget
  configId="d77c7c91-dd51-4eb4-8012-1d2353aa36e7"
  location="eu"
  triggerId="searchWidgetTrigger">
</gen-search-widget>

<!-- Element that opens the widget on click. It does not have to be an input -->
<input placeholder="Search here" id="searchWidgetTrigger" />
"""

# Display the widget using Streamlit's HTML component
st.components.v1.html(widget_code, height=300)
        
