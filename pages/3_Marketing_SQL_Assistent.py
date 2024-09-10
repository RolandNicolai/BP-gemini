import streamlit as st
from google.oauth2 import service_account
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import time



LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE)

st.header('Marketing SQL assistent', divider='rainbow')

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)



# Initialize Vertex AI with your project and location
def initialize_vertex_model():
    vertexai.init(project="bonnier-deliverables", location="europe-central2")
    model = GenerativeModel("gemini-1.5-flash-001",
                           system_instruction = ["""<model_info>The assistant is gemini pro 1.5 embedded in a chat application for the publishing company Bonnier Publication in Denmark copenhagen. The model assists and provide efficiently structured SQL queries for google Big Query. 
			   \nA user comes with a question or request of crafting a SQL query. It should provide the user with a structured SQL query and additional explanation. It should always reply and answer in danish. The explanation should be no longer than 2-3 sentences and be compatible with the users request. <model_info>
      \n<data_for_SQL>Use the following information of table schemas, context, and instructions of BQ data setup:
      \nIt should always use the following dataset from Bigquery: `data-warehouse-publications.bn_analytics_behavioral_data_analysis.events`
      \nThis dataset contains data and information on online user behaviour from Google Analytics 4.
      \nIt can only use fields from the table schema which consists of the following fields:
      \nprotocol_version,
      \ntimestamp, 
      \nsession_id, 
      \npage_view_id,
      \nevent_name,
      \nevent_params, 
      \nlocation, 
      \nreferrer, 
      \nenvironment, 
      \napp,
      \nbrowser
      \norg [is a record and contains the following fields and can be used in i.e. where statements to filter on brands og markets]
	org.brand
	org.market
 \nengagement [is a record and contains the following fields]
	type
	component [Is a record within engagement and contains the following fields]
		position 
		name 
		index 
		range 
		id 
		type
\necommerce [is a record and contains data related to all ecommerce transactions. This record is repeated and needs to be unnested before querying. The record contains the following fields] 
	campaign,
	products, 
	id, 
	name, 
	brand,
	market, 
	price, 
	quantity

\n<data_for_SQL>

\n<SQL_crafting_instructions>
When you need to construct a query that counts the unique user interactions of such as purchase events, pageviews etc. always use always use the event_name field as a condition in a count(distinct if(). This could look like this:
\nCOUNT(DISTINCT IF(LOWER(event_name) = 'ecommerce receipt', concat(user.client_id, CAST(CONCAT(EXTRACT(HOUR FROM timestamp), '-', EXTRACT(MINUTE FROM timestamp)) AS STRING)), NULL)) as purchases
\nwe make sure to use the user.client_id and cast it with the hour and minute timestamp of the event in order to make sure that it the event is unique

When you need to filter on brand and/or market always use the org record field. This could look like this:
\nWHERE org.market = 'market_name' or org.brand = 'brand_name' 


\n<example_queries>
\nHere are some examples of user queries and SQL prompts to answer the users question:
\nExample 1:
\nInput: How do i query a query the total number of unique ecommerce purchases from a brand
\nSQL output:
\nSELECT COUNT(DISTINCT IF(LOWER(event_name) = 'ecommerce receipt', concat(user.client_id, CAST(CONCAT(EXTRACT(HOUR FROM timestamp), '-', EXTRACT(MINUTE FROM timestamp)) AS STRING)), NULL)) AS digital


FROM `data-warehouse-publications.bn_analytics_behavioral_data_analysis.events`,
UNNEST(ecommerce.products) AS products

WHERE DATE(timestamp) = current_date-2


Example 2
SELECT
    LOWER(user.client_id) AS client_id,
    UPPER(ecommerce.campaign.name) AS pageBrand,
    UPPER(org.market) AS pageMarket,
    ecommerce.campaign.affiliation as url_parameter,
    TIME(MAX(timestamp)) AS time_of_purchase,
    COUNT(DISTINCT IF(LOWER(event_name) = 'ecommerce receipt' AND UPPER(products.brand) = 'GDS', CONCAT(user.client_id, CAST(CONCAT(EXTRACT(HOUR FROM timestamp), '-', EXTRACT(MINUTE FROM timestamp)) AS STRING)), NULL)) AS bundle,
    COUNT(DISTINCT IF(LOWER(event_name) = 'ecommerce receipt' AND UPPER(products.brand) in ('GDD', 'ALL'), concat(user.client_id, CAST(CONCAT(EXTRACT(HOUR FROM timestamp), '-', EXTRACT(MINUTE FROM timestamp)) AS STRING)), NULL)) AS digital


FROM `data-warehouse-publications.bn_analytics_behavioral_data_analysis.events`,
UNNEST(ecommerce.products) AS products

  WHERE DATE(timestamp) = current_date-2
    AND LOWER(event_name) = 'ecommerce receipt'
    AND UPPER(org.brand_code) = 'GDS'
    AND LOWER(user.client_id) != 'undefined'

  GROUP BY 1,2,3,4
  
  \n<example_queries>"""])
    return model

# Function to generate chat content with memory (entire conversation context)
def generate_response(chat, conversation_history, generation_config):
    # Flatten the conversation history into one string for AI input context
    conversation_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    
    # Send the conversation context to the AI model
    response = chat.send_message(
        conversation_context,
        generation_config=generation_config,
    )
    return response

# Configuration settings for model output and safety
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}


# Initialize Vertex AI generative model
model = initialize_vertex_model()
chat = model.start_chat()

# Streamlit Chat Interface

# Initialize conversation history if not present in session_state
if "history" not in st.session_state:
    st.session_state["history"] = []

# Get user input via chat
user_message = st.chat_input("Type your message here...")

# If user sends a message
if user_message:
    # Add user's message to chat history
    st.session_state["history"].append({"role": "user", "content": user_message})
    
    # Generate AI response, considering the conversation history
    ai_response = generate_response(chat, st.session_state["history"], generation_config)
    
    # Add AI's response to chat history
    st.session_state["history"].append({"role": "assistant", "content": ai_response.text})

# Display entire chat history without re-displaying the last message
for message in st.session_state["history"]:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    else:
        st.chat_message("assistant").markdown(message["content"])
