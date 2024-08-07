import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import pandas as pd
from pandas import DataFrame
import numpy as np
import time




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
                "description": f"Python script on a single line that will help answer user's questions with line or barcharts. Always use the existing dataframe called df_cleaned and field names: [Date, Brand, Market, Sessions, Clicks, Purchases] to create a variable named chart data followed by st.bar_chart(chart_data) or st.line_chart(chart_data)",
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

def execute_generated_code(code):
    global df_cleaned, st, pd
    exec(code, globals())


def extract_code(script):
    lines = script.split('\n')
    code_lines = []
    for line in lines:
        if line.strip().startswith('```python') or line.strip().endswith('```'):
            continue
        code_lines.append(line)
    return '\n'.join(code_lines).strip()

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
        message_placeholder = st.empty()
        full_response = ""

        chat = model.start_chat()
        prompt += """
            Please give a concise, high-level summary followed by detail in
            plain language about where the information in your response is
            coming from in the database. Only use information that you learn
            from BigQuery, do not make up information.
            """

        response = chat.send_message(prompt)
        response = response.candidates[0].content.parts[0]

        print(response)
        api_requests_and_responses = []
        function_calling_in_process = True
        while function_calling_in_process:
            try:
                params = {}
                for key, value in response.function_call.args.items():
                    params[key] = value

                print(response.function_call.name)
                print(params)

                if response.function_call.name == "chart_script":
                    try:
                        cleaned_script = (
                            params["query"]
                            .replace("\\n", " ")
                            .replace("\n", "")
                            .replace("\\", "")
                            .replace("```python", "")
                            .replace("```", "")
                        )
                        cleaned_script = '\n'.join(
                        [line for line in cleaned_script.split('\n')
                        if not (line.strip().startswith('```python') or line.strip().endswith('```'))]
                        ).strip()
                        cleaned_script_1 = extract_code(params["query"])

                    except Exception as e:
                        api_response = f"{str(e)}"
                        api_requests_and_responses.append(
                            [response.function_call.name, params, response]
                        )

                print(cleaned_script)


                response = chat.send_message(
                    Part.from_function_response(
                        name=response.function_call.name,
                        response={
                            "content": cleaned_script,
                        },
                    ),
                )
                response = response.candidates[0].content.parts[0]


                api_requests_and_responses.append(
                        [response.function_call.name, params, response]
                    )
        
            except AttributeError:
                function_calling_in_process = False

        
        #time.sleep(3)
        #exec(cleaned_script, globals())

        full_response = response.text
        try:
            execute_generated_code(cleaned_script_1)
        except Exception as e:
            st.error(f"Error executing the script: {e}")


        #chart_data = df.groupby('Market')['Sessions'].sum().reset_index()
        #st.bar_chart(chart_data.set_index('Market'))

        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
