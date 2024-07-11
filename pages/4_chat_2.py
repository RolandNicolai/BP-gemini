from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account
import vertexai
import streamlit as st
from langchain.llms import VertexAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from google.cloud import bigquery
import pandas as pd


#from langchain.agents import create_pandas_dataframe_agent


st.title("VertexAI assistant")

# Set OpenAI API key from Streamlit secrets
#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)


client = bigquery.Client(credentials=credentials)


vertexai.init(project=st.secrets["project"], location=st.secrets["location"], credentials=credentials)



#gemini-1.5-flash-001
#gemini-1.5-pro-001

sql = """
    SELECT *
    FROM `bonnier-deliverables.dummy_dataset.dummy_data`

"""
project_id = "bonnier-deliverables"
query_job = client.query(sql)
results = query_job.result()
rows = [dict(row) for row in results]

# Create DataFrame from the list of dictionaries
df = pd.DataFrame(rows)

# If necessary, clean or transform your DataFrame here
df_cleaned = df.applymap(lambda x: x if not isinstance(x, dict) else str(x))

# Display the DataFrame in Streamlit
st.dataframe(df_cleaned)

generation_config = {
  "temperature": 0,

  "max_output_tokens": 8192,
  #"response_mime_type": "text/plain",
}
model = GenerativeModel(
    "gemini-1.5-pro-001",
    generation_config=generation_config,
)

llm = VertexAI("gemini-1.5-pro-001")


agent = create_pandas_dataframe_agent(llm, df_cleaned, verbose=True)

