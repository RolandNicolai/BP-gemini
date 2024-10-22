import streamlit as st
from google.oauth2 import service_account
#from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
import vertexai
from google.cloud import bigquery
import time
import datetime
import pytz

import io
from PIL import Image
import matplotlib.pyplot as plt
import tensorflow as tf

def printImages(results):
 image_results_list = list(results)
 amt_of_images = len(image_results_list)

 fig, axes = plt.subplots(nrows=amt_of_images, ncols=2, figsize=(50, 50))
 fig.tight_layout()
 fig.subplots_adjust(hspace=0.5)
 for i in range(amt_of_images):
   gcs_uri = image_results_list[i][0]
   text = image_results_list[i][1]
   f = tf.io.gfile.GFile(gcs_uri, 'rb')
   stream = io.BytesIO(f.read())
   img = Image.open(stream)
   axes[i, 0].axis('off')
   axes[i, 0].imshow(img)
   axes[i, 1].axis('off')
   axes[i, 1].text(0, 0, text, fontsize=20)
 plt.show()

email = st.experimental_user.email

user_first_name = email.split(".")[0]

# Define the Copenhagen timezone
copenhagen_tz = pytz.timezone('Europe/Copenhagen')


# Get the current date and time in Copenhagen timezone
today = datetime.datetime.now(copenhagen_tz)

current_date_str = today.strftime('%Y-%m-%dT%H:%M:%S')


LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE)

st.header('Bonnier Data Assistent', divider='rainbow')



credentials = service_account.Credentials.from_service_account_info(
    st.secrets["vertexAI_service_account"]
)
client = bigquery.Client(credentials=credentials)

user_query = "Image of a grass"

search_query =f"""CREATE OR REPLACE TABLE `bonnier-deliverables.LLM_vertex.GDS_query_embeddings`
AS
SELECT * FROM ML.GENERATE_EMBEDDING(
 MODEL `bonnier-deliverables.ML_generate_text.ml_generate_text_v1`,
 (
   SELECT '{user_query}' AS content
 )
);
"""

client.query(search_query).result()

results = """WITH query_embedding AS (
  SELECT ml_generate_embedding_result AS embedding
  FROM `bonnier-deliverables.LLM_vertex.GDS_query_embeddings`
)

SELECT
  base.uri,
  (1 - distance) AS similarity_score
FROM
  VECTOR_SEARCH(
    TABLE `bonnier-deliverables.LLM_vertex.gds_images_embeddings`,
    'ml_generate_embedding_result',
    (SELECT embedding FROM query_embedding),
    top_k => 5,
    distance_type => 'COSINE'
  );"""


results_list = list(client.query(results).result())

print(results_list)
printImages(client.query(results))


        
