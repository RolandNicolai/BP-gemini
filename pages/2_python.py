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

st.set_page_config(page_title="Python", page_icon="📈")
st.sidebar.header("Python")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
st.write(f"- hvor mange sessioner havde de forskellige brands, vis mig sessioner fordelt på dato")
st.write(f"- hvor mange sessioner havde de forskellige brands, vis mig udviklingen fordelt på dato i barchart")
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)

vertexai.init(project=st.secrets["project"], location=st.secrets["location"], credentials=credentials)
client = bigquery.Client(credentials=credentials)

generation_config = {
  "temperature": 0,

  "max_output_tokens": 8192,
  #"response_mime_type": "text/plain",
}
model = GenerativeModel(
    "gemini-1.5-pro-001",
    generation_config=generation_config,
)

project = st.secrets["project"]
dataset = st.secrets["dataset"]
table = st.secrets["table"]
fieldNames = '[Date, Brand, Market, Sessions, Clicks, Purchases]'
descriptions = ""

user_prompt = st.text_input("Indtast spørgsmål herunder")
button = st.button("Søg")


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

#------------------ works up until here
# Clean the DataFrame
#df['Sessions'] = df['Sessions'].str.replace(',', '').astype(int)

# Aggregate data by 'Market'
chart_data = df.groupby('Market')['Sessions'].sum().reset_index()

# Display the bar chart in Streamlit
st.bar_chart(chart_data.set_index('Market'))

if button and user_prompt:
    with st.spinner('Opretter query...'):
        time.sleep(3)
    queryModel_response = model.generate_content(
          [f""" only output the python script
          from the user question: {user_prompt}
          create a python script always only using the available relevant fieldNames: {fieldNames} 
          only use the dataframe called df_cleaned to create a variable named chart data followed by st.bar_chart(chart_data) or st.line_chart(chart_data) based on the context
          use appropriate width and height
          
          """],
    generation_config= generation_config,

    )
    queryModel_response_text = queryModel_response.text
    st.subheader("Under the hood")
    st.markdown(queryModel_response.text)
    #code = queryModel_response_text
    #cleaned_script = (queryModel_response_text.replace("\\n", " ").replace("\n", " ").replace("\\", "").replace("```","").replace("python", ""))
    #print(cleaned_query)
    def extract_code(script):
        lines = script.split('\n')
        code_lines = []
        for line in lines:
            if line.strip().startswith('```python') or line.strip().endswith('```'):
                continue
            code_lines.append(line)
        return '\n'.join(code_lines).strip()
    cleaned_script = extract_code(queryModel_response_text)

    # Define a function to execute the generated code
    def execute_generated_code(code):
        global df_cleaned, st, pd
        exec(code, globals())

    # Execute the cleaned script
    try:
        execute_generated_code(cleaned_script)
    except Exception as e:
        st.error(f"Error executing the script: {e}")
    
