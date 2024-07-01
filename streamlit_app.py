from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account
from google.cloud import bigquery
import hmac
import streamlit as st
import pandas as pd
from pandas import DataFrame
import numpy as np
import time
import vertexai
import streamlit as st

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 Ukendt bruger eller adgangskode")
    return False

if not check_password():
    st.stop()

# Main Streamlit app starts here
LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE, link="https://bonnierpublications.com/en/bonnier-publications-2/")

# Page title
st.set_page_config(page_title='SQL', page_icon='👨‍💻')
st.title('Bonnier Data Assistent 👨‍💻')

with st.expander('Om assistenten'):
  st.markdown('**Brug**')
  st.info('Denne assistent benytter Generativ AI til at genererer SQL queries ud fra en brugers spørgsmål. Herefter oprettes forbindelse til BigQuery klienten hvor den relevant data vil blive indhentet.')

  
with st.sidebar:
    st.write(f'Eksempler på spørgsmål ang. data')
    st.write(f'- Hvor mange sessions var der på de forskellige brands i hhv. 1 og 4 quarter af 2023')
    st.write(f'- Hvor mange salg, klik, sessioner havde hvert brand i 2023? og hvordan så deres clicks per session ud?')





    # Dropdown list with options
    option = st.selectbox('1. Vælg et datasæt', ['dummy dataset', 'kpi dataset'])

# Set variables based on the selected option
    if option == 'dummy dataset':
        project = st.secrets["project"]
        dataset = st.secrets["dataset"]
        table = st.secrets["table"]
        fieldNames = '[Date, Brand, Market, Sessions, Clicks, Purchases]'
        descriptions = ""
    elif option == 'kpi dataset':
        project = st.secrets["project"]
        dataset = st.secrets["kpi_dataset"]
        table = st.secrets["kpi_table"]
        fieldNames = "[dato, publication_name, media, country, activity_type, ownedPaid]"
        descriptions ="Description of the available field names:
        [antal] = an interger equalling the number of sales\n[Dato]: equals a date field\n[publication_name]: euqls a brand name which can be used in where statements in order to filter the right brand\n[media]: equals a mediacode/mediakode which is commonly associated with different commercial placements. this field can be used in where statements when users ask questions around mediacodes\n[country]: equals a country/market and can only be DK, NO, SE, or FI\n[activity_type]: equals the source of a sale and can be either [egne sites, internet]\n[ownedPaid]: the field is used to define whether a sale has been conducted from an owned or paid channel
        "

    else:
    # Set default values or other values for Option 2
        project = 'default_project'
        dataset = 'default_dataset'
        table = 'default_table'

# Display the selected option and corresponding variables
st.subheader("Info om valgt datakilde")
with st.expander('Se info'):
    st.write(f'Du har valgt: {option}')
    st.code(f'Projekt: {project}', language='markdown')
    st.code(f'Datasæt: {dataset}', language='markdown')
    st.code(f'Tabel: {table}', language='markdown')
    st.code(f'Attributer: {fieldNames}', language='markdown')

# Sidebar for accepting input parameters
#with st.sidebar:
    # Load data
    #st.header('1. Kom i gang med assistenten')



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



#queryModel_response = queryModel_response.text

#user_prompt_test = st.text_input("User prompt:")
#button_test = st.button("Generate")

client = bigquery.Client(credentials=credentials)
maximum_bytes_billable = 100000000 # = 100 Mb

#project = st.secrets["project"]
#dataset = st.secrets["dataset"]
#table = st.secrets["table"]

st.subheader("Stil et spørgsmål til assistenten")
user_prompt = st.text_input("Indtast spørgsmål herunder")
button = st.button("Søg")


if button and user_prompt:
    with st.spinner('Opretter query...'):
        time.sleep(3)
    queryModel_response = model.generate_content(
          [f""" [System instruction: you are a professional data engineer with a proficiency in BigQuery SQL, only output the SQL query from a question. You are given a user question and instructions. Always only handle queries in english]
          User question: {user_prompt}
          Instruction: write a script always only using the following dataset, table and field names.
          project: {project}
          dataset: {dataset}
          table: {table}

          field names: {fieldNames}.
          in where statements use lower() when necessary to avoid lower/uppercase issues

          """],
    generation_config= generation_config,

    )
    queryModel_response_text = queryModel_response.text
    st.subheader("Under the hood")
    with st.expander('Se query'):
        st.markdown(queryModel_response.text)
    
    
    #st.subheader("Respons efter cleaning af query")

    cleaned_query = (
    queryModel_response_text
    .replace("\\n", " ")
    .replace("\n", " ")
    .replace("\\", "")
    .replace("```","")
    .replace("sql", "")
    )
    #print(cleaned_query)

    dryRun_job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

# Start the query, passing in the extra configuration.
    dryRun_query_job = client.query(
        (cleaned_query),
        job_config=dryRun_job_config,
        location = "EU",
    )  # Make an API request.

    bytes_billed = dryRun_query_job.total_bytes_processed

  #Sætter maksimum på bytes som kan queries (100 mb)
  #BigQuery API kald
    if bytes_billed < maximum_bytes_billable:
        with st.spinner('Henter data fra BigQuery...'):
            time.sleep(3)
        job_config = bigquery.QueryJobConfig(maximum_bytes_billed = maximum_bytes_billable)  # Data limit per query job
        query_job = client.query(cleaned_query, location = "EU", job_config=job_config)
        api_response = query_job.result()
        bytes_billed = query_job.total_bytes_billed
        bytes_billed_result = (bytes_billed / 1.048576e6)
        api_response = str([dict(row) for row in api_response])
        api_response = api_response.replace("\\", "").replace("\n", "")
        st.subheader("Respons fra BigQuery API kald")
        #df = client.query_and_wait(cleaned_query).to_dataframe()
        with st.expander('Se BigQuery API respons'):
            st.markdown(api_response)
            st.text("This query processes {:.2f} Mb".format(bytes_billed_result))
        with st.spinner('Genererer svar fra data...'):
            time.sleep(8)
        answerModel_response = model.generate_content(
            [f"""[System instruction: you are a professional data analyst. You are given a user question and the answer to the question. Always only handle answers and responses in danish]
            Please give a concise, high-level summary with relevant information for the following user question: {user_prompt} followed by detail in
            plain language about where the information in your response is coming from in the database and how much was billed:
            project: {project}
            dataset: {dataset}
            table: {table}.
            query billed in Mb: {bytes_billed_result}
            Only use information that you learn from BigQuery:´´´{api_response}´´´.
            {descriptions}
            Do not make up information. Always present numbers in list formats """],
        generation_config = generation_config,
        )
        answerModel_response = answerModel_response.text
        st.subheader("Assistent svar 🎈")
        st.markdown(answerModel_response)

        chartModel_response = model.generate_content(
            [f"""use the following streamlit framework structure:  st.line_chart(df, x="col1", y=["col2", "col3"], color=["#FF0000", "#0000FF"] # Optional)
            then output only the information within parenthesis  from the following json data:´´´{api_response}´´´.
            Do not make up information."""],
        generation_config = generation_config,
        )
        chartModel_response = chartModel_response.text
        st.subheader("Assistent svar")
        st.markdown(chartModel_response)
    else:
        print('Query exceeds billing quota')

### big query test API


# Initiate the model building process
