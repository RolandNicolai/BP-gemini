import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import pandas as pd
from pandas import DataFrame
import numpy as np



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

project = st.secrets["project"]
dataset = st.secrets["dataset"]
table = st.secrets["table"]
fieldNames = '[Date, Brand, Market, Sessions, Clicks, Purchases]'
descriptions = ""


chart_script_func = FunctionDeclaration(
    name="chart_script",
    description="Create streamlit charts using the streamlit python library ",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": f"Python script on a single line that will help give quantitative answers to the user's question. In the python script, always use the fully qualified dataframe df_cleaned and field names.",
            }
        },
        "required": [
            "query",
        ],
    },
)

python_chart_tool = Tool(
    function_declarations=[
        chart_script_func,
    ],
)

generation_config = {
  "temperature": 0,

  "max_output_tokens": 8192,
  #"response_mime_type": "text/plain",
}
model = GenerativeModel(
    "gemini-1.5-flash-001",
    generation_config=generation_config,
    tools=[python_chart_tool],
)


if "vertex_model" not in st.session_state:
    st.session_state["vertex_model"] = model

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Hvad kan jeg hjælpe med?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using Vertex AI model
    with st.chat_message("assistant"):
        response = st.session_state["vertex_model"].generate_content(prompt)
        st.markdown(response.text)
        response = chat.send_message(prompt)
        response = response.candidates[0].content.parts[0]
        print(response)
        function_calling_in_process = True
        while function_calling_in_process:
            try:
                params = {}
                for key, value in response.function_call.args.items():
                    params[key] = value

                print(response.function_call.name)
                print(params)

                if response.function_call.name == "chart_script":

                    api_requests_and_responses.append(
                        [response.function_call.name, params, response]
                    )
            except AttributeError:
                function_calling_in_process = False
        #chart_data = df.groupby('Market')['Sessions'].sum().reset_index()
        #st.bar_chart(chart_data.set_index('Market'))

        
    st.session_state.messages.append({"role": "assistant", "content": response.text})
