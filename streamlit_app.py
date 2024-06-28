from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account
from google.cloud import bigquery
import hmac
import streamlit as st
import pandas as pd
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
st.set_page_config(page_title='BP assistant', page_icon='⚙️')
st.title('Performance Marketing Assistant')

with st.expander('Om assistenten'):
  st.markdown('**Hvad kan denne assistent?**')
  st.info('This app allow users to build a machine learning (ML) model in an end-to-end workflow. Particularly, this encompasses data upload, data pre-processing, ML model building and post-model analysis.')

  st.markdown('**Opret en API nøgle**')
  st.warning('Find service account key: https://www.youtube.com/watch?v=I8W-4oq1onY&t=99s')

  st.markdown('**Under the hood**')
  st.markdown('Om')
  st.code('''Empty''', language='markdown')
  


# Sidebar for accepting input parameters
#with st.sidebar:
    # Load data
    #st.header('1. Kom i gang med assistenten')



credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)



vertexai.init(project=st.secrets["project"], location=st.secrets["location"], credentials=credentials)

queryModel = GenerativeModel(
    "gemini-1.5-pro-001",
)

answerModel = GenerativeModel(
    "gemini-1.5-pro-001",
)

#queryModel_response = queryModel_response.text

#user_prompt_test = st.text_input("User prompt:")
#button_test = st.button("Generate")

client = bigquery.Client(credentials=credentials)
maximum_bytes_billable = 100000000 # = 100 Mb

project = "bonnier-deliverables"
dataset = "dummy_dataset"
table = "dummy_data"

user_prompt = st.text_input("User prompt:")
button = st.button("Generate")

if button and user_prompt:
    queryModel_response = queryModel.generate_content(
          [f"""User question: {user_prompt}
          Instruction: write a script always only using the following dataset, table and field names.
          project: {project}
          dataset: {dataset}
          table: {table}

          field names: [Date, Brand, Market, Sessions, Clicks, Purchases].
          in where statements use lower() when necessary to avoid lower/uppercase issues

          """],
    generation_config={"temperature": 0},
    )
    queryModel_response_text = queryModel_response.text
    st.subheader("Respons før cleaning af query")
    st.markdown(queryModel_response.text)
    
    
    st.subheader("Respons efter cleaning af query")

    cleaned_query = (
    queryModel_response_text
    .replace("\\n", " ")
    .replace("\n", " ")
    .replace("\\", "")
    .replace("```","")
    .replace("sql", "")
    )
    print(cleaned_query)

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
        job_config = bigquery.QueryJobConfig(maximum_bytes_billed = maximum_bytes_billable)  # Data limit per query job
        query_job = client.query(cleaned_query, location = "EU", job_config=job_config)
        api_response = query_job.result()
        bytes_billed = query_job.total_bytes_billed
        bytes_billed_result = (bytes_billed / 1.048576e6)
        api_response = str([dict(row) for row in api_response])
        api_response = api_response.replace("\\", "").replace("\n", "")
        st.subheader("Respons fra BigQuery API kald")
        st.markdown(api_response)
        st.text("This query processes {:.2f} Mb".format(bytes_billed_result))

        st.subheader("AnswerModel Response")
        answerModel_response = answerModel.generate_content(
            [f""" Please give a concise, high-level summary with relevant information for the following user question: {user_prompt} followed by detail in
            plain language about where the information in your response is coming from in the database and how much was billed:
            project: {project}
            dataset: {dataset}
            table: {table}.
            query billed in Mb: {bytes_billed_result}
            Only use information that you learn from BigQuery:"{api_response}".
            Do not make up information. Always present numbers in list formats """],
        generation_config={"temperature": 0},
        )
        answerModel_response = answerModel_response.text
        st.markdown(answerModel_response)
    else:
        print('Query exceeds billing quota')

### big query test API



job_config = bigquery.QueryJobConfig(maximum_bytes_billed = maximum_bytes_billable)  # Data limit per query job
query_job = client.query("SELECT     Brand,     SUM(Sessions) AS TotalSessions,     SUM(Clicks) AS TotalClicks,     SUM(Purchases) AS TotalPurchases,     (SAFE_DIVIDE(SUM(Clicks), SUM(Sessions))) AS ClicksPerSession   FROM     `bonnier-deliverables.dummy_dataset.dummy_data`   WHERE CAST(Date as STRING) LIKE '2023%'   GROUP BY 1", location = "EU", job_config=job_config)
api_response = query_job.result()
bytes_billed = query_job.total_bytes_billed
bytes_billed_result = (bytes_billed / 1.048576e6)
api_response = str([dict(row) for row in api_response])
api_response = api_response.replace("\\", "").replace("\n", "")

st.write("Query result", api_response)



# Initiate the model building process
