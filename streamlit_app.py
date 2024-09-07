import streamlit as st

Data_assistent = st.Page("pages/2_Data_Assistent.py", title="Data Assistent")
#create_page = st.Page("pages/1_Data_Assistent.py", title="Data Assistent", icon=":material/add_circle:")
Artikel_assistent = st.Page("pages/3_Artikel_assistent.py", title="Artikel Assistent", icon=":material/delete:")

pg = st.navigation([Data_assistent, Artikel_assistent])
#st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()



        
