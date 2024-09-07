import streamlit as st

hjem = st.Page("pages/1_Hjem.py", title="Hjem")
data_assistent = st.Page("pages/2_Data_Assistent.py", title="Data Assistent")
#create_page = st.Page("pages/1_Data_Assistent.py", title="Data Assistent", icon=":material/add_circle:")
artikel_assistent = st.Page("pages/3_Artikel_assistent.py", title="Artikel Assistent", icon=":material/delete:")

pg = st.navigation([data_assistent, artikel_assistent])
#st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()



        
