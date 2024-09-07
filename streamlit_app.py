import streamlit as st

hjem = st.Page("pages/1_Hjem.py", title="Hjem")
data_assistent = st.Page("pages/2_Data_Assistent.py", title="Data Assistent")
#create_page = st.Page("pages/1_Data_Assistent.py", title="Data Assistent", icon=":material/add_circle:")
artikel_assistent = st.Page("pages/3_Artikel_Assistent.py", title="Artikel Assistent")
pdf_assistent = st.Page("pages/4_PDF_Assistent.py", title="PDF Assistent")


pg = st.navigation([hjem, data_assistent, artikel_assistent, pdf_assistent])
#st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()



        
