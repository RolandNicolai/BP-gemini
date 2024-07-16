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
maximum_bytes_billable = 100000000 # = 100 Mb


vertexai.init(project=st.secrets["project"], location=st.secrets["location"], credentials=credentials)



#gemini-1.5-flash-001
#gemini-1.5-pro-001

with st.sidebar:
    # Dropdown list with options
    option = st.selectbox('1. Vælg et datasæt', ['dummy dataset', 'kpi dataset', 'kalkule dataset'])

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
        fieldNames = "[dato, publication_name, media, country, activity_type, ownedPaid, purchases]"
        descriptions ="""
        Description of the available field names:
        always use the following field descriptions and field_information as guidance when creating the queries, always use the field [purchase] when asked about sales 
        \n[purchases]: the total number of purchases, must be refered to as purchases
        \n[Dato]: the date field
        \n[publication_name]: equals a name which can be used in where statements in order to filter brands
        \n[media]: equals a mediacode/mediakode which is commonly associated with different commercial placements. this field can be used in where statements when users ask questions around mediacodes
        \n[country]: equals a country/market. Only use the abbreviations in [DK, NO, SE, or FI]  
        \n[activity_type]: can be  either [egne sites, internet] only used when user explicitly needs information on activity_type
        \n[ownedPaid]: the field is used to define whether a sale has been conducted from an owned or paid channel, field can only be either [owned, paid]
        \nexample of query ['hvor mange salg havde GDS i juni 2024']
        '''SQL: SELECT
        sum(purchases)
        FROM
        `bonnier-deliverables.dummy_dataset.dummy_data`
        WHERE lower(publication_name) = 'gds'
        '''
        """
    elif option == 'kalkule dataset':
        project = st.secrets["project"]
        dataset = st.secrets["kalkule_dataset"]
        table = st.secrets["kalkule_table"]
        fieldNames = "[Country, Activity_type, No_in_offer, Price, Handling, Total_price, Total_price_currency, Response, Lifetime, Net_Lifetime, Media_cost, Cost_per_subscriber, Net_CPO, GP_activity, ROI, Premium_cost]"
        descriptions ="""
        Description of the available field names:
        \n[Country]: string - The country where the offer was made. Only use the abbreviations in [DK, NO, SE, or FI] 
        \n[Activity_type]: string - Type of activity.
        \n[No_in_offer]: integer - Number of items in the offer.
        \n[Price]: float - Price of the offer.
        \n[Handling]: float - Handling cost. 
        \n[Total_price]: float - Total price of the offer.
        \n[Total_price_currency]: float - Currency of the total price.
        \n[Response]: integer - Number of responses to the offer. 
        \n[Lifetime]: float - Lifetime value. 
        \n[Net_Lifetime]: float - Net lifetime value
        \n[Media_cost]: float - Media cost
        \n[Cost_per_subscriber]: float - Cost per subscriber  
        \n[Net_CPO]: float - Net Cost Per Order. 
        \n[GP_activity]: float - Gross Profit on activity
        \n[ROI]: float - Return on Investment.
        \n[Premium_cost]: float - Cost of the premium
        \nexample of query ['hvad var Net lifetime per marked']
        '''SQL: SELECT
        Country,
        sum(Net_Lifetime)
        FROM
        `bonnier-deliverables.dummy_dataset.dummy_data`
        GROUP BY 1
        """

    else:
    # Set default values or other values for Option 2
        project = 'default_project'
        dataset = 'default_dataset'
        table = 'default_table'
    st.write(f'Eksempler på spørgsmål ang. data')
    st.write(f'Kalkule dataset')
    st.write(f'- hvad var den gennemsnitlige ROI for hvert marked?')
    st.write(f'Dummy datasæt')
    st.write(f'- Hvor mange sessions var der på de forskellige brands i hhv. 1 og 4 quarter af 2023')
    st.write(f'- Hvor mange salg, klik, sessioner havde hvert brand i 2023? og hvordan så deres clicks per session ud?')
    st.write(f'KPI datasæt')
    st.write(f'- sorter salg på brands fra stigende til faldende i juni 2024')
    st.write(f'- giv mig et overview over salg i 2024 fordelt på måned')
    st.write(f'- hvor mange salg havde henholdsvis HIS og GDS i 2024 på mediekoden redteaser på owned channel i juni vs i maj')
    st.write(f'- hvor mange salg havde HIS i 2024 på mediekoden redteaser på owned channel')
    st.write(f'- hvor mange salg havde HIS i 2024 på mediekoden redteaser på owned channel i juni vs i maj')




sql_script_func = FunctionDeclaration(
    name="sql_query",
    description="Create streamlit charts using the streamlit python library ",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": f"SQL query on a single line that will help give quantitative answers to the user's question when run on a BigQuery dataset and table. always only use the fieldNames: {fieldNames}. Always only use information that you learn from the description of fields in BigQuery:\n{descriptions}.\nWrite the script always only using the following project, dataset and table.\nproject: {project}\ndataset: {dataset}\ntable: {table}\nin where statements use lower() when necessary to avoid lower/uppercase issues and always cast date fields as date",
            }
        },
        "required": [
            "query",
        ],
    },
)

answer_func = FunctionDeclaration(
    name="answer",
    description="answer users' questions",
    parameters={
        "type": "object",
        "properties": {
            "answer": {
                "type": "string",
                "description": "give a helpful answer to the user",
            }
        },
        "required": [
            "answer",
        ],
    },
)




toolcase = Tool(
    function_declarations=[
        sql_script_func,
        #answer_func,
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
    tools=[toolcase],
)





if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"].replace("$", "\$"))  # noqa: W605
        try:
            with st.expander("Function calls, parameters, and responses"):
                st.markdown(message["backend_details"])
        except KeyError:
            pass

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
        client = bigquery.Client()

        prompt += """
            Please give a concise, high-level summary followed by detail in
            plain language about where the information in your response is
            coming from in the database. Only use information that you learn
            from BigQuery, do not make up information. Only write in danish
            """

        response = chat.send_message(prompt)
        response = response.candidates[0].content.parts[0]

        print(response)
        api_requests_and_responses = []
        backend_details = ""

        function_calling_in_process = True
        while function_calling_in_process:
            try:
                params = {}
                for key, value in response.function_call.args.items():
                    params[key] = value

                print(response.function_call.name)
                print(params)

                if response.function_call.name == "sql_query":
                    job_config = bigquery.QueryJobConfig(
                        maximum_bytes_billed=100000000
                    )  # Data limit per query job

                    try:

                        #cleaned_query = (
                            #params["query"]
                            #.replace("\\n", " ")
                            #.replace("\n", " ")
                            #.replace("\\", "")
                            #.replace("sql", "")
                            #.replace("SQL:", "")

                        #)
                        cleaned_query = (
                            model.text
                            .replace("\\n", " ")
                            .replace("\n", " ")
                            .replace("\\", "")
                            .replace("sql", "")
                            .replace("SQL:", "")
                            )
                        
                        print(cleaned_query)
                        #message.write(st.markdown(cleaned_query))

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
                            #job_config = bigquery.QueryJobConfig(maximum_bytes_billed = maximum_bytes_billable)  # Data limit per query job
                            query_job = client.query(cleaned_query, location = "EU", job_config=job_config)
                            api_response = query_job.result()
                            bytes_billed = query_job.total_bytes_billed
                            bytes_billed_result = (bytes_billed / 1.048576e6)
                            api_response = str([dict(row) for row in api_response])
                            api_response = api_response.replace("\\", "").replace("\n", "").replace("SQL:","")
                            print("Query result:", api_response[:100])  # Print first 100 chars of response
                            api_requests_and_responses.append(
                                [response.function_call.name, params, api_response]
                            )
                    except Exception as e:
                        api_response = f"{str(e)}"
                        api_requests_and_responses.append(
                            [response.function_call.name, params, response]
                        )

                print(api_response)


                response = chat.send_message(
                    Part.from_function_response(
                        name=response.function_call.name,
                        response={
                            "content": api_response,
                        },
                    ),
                )
                response = response.candidates[0].content.parts[0]

                backend_details += "- Function call:\n"
                backend_details += (
                    "   - Function name: ```"
                    + str(api_requests_and_responses[-1][0])
                    + "```"
                )
                backend_details += "\n\n"
                backend_details += (
                    "   - Function parameters: ```"
                    + str(api_requests_and_responses[-1][1])
                    + "```"
                )
                backend_details += "\n\n"
                backend_details += (
                    "   - API response: ```"
                    + str(api_requests_and_responses[-1][2])
                    + "```"
                )

                backend_details += "\n\n"
                with message_placeholder.container():
                    st.markdown(backend_details)

            except AttributeError:
                function_calling_in_process = False

        time.sleep(3)

        full_response = response.text
        with message_placeholder.container():
            st.markdown(full_response.replace("$", "\$"))  # noqa: W605
            with st.expander("Function calls, parameters, and responses:"):
                st.markdown(backend_details)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response,
                "backend_details": backend_details,
            }
        )
        


        
