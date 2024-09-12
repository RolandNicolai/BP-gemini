import streamlit as st

hjem = st.Page("pages/1_Hjem.py", title="Hjem")
data_assistent = st.Page("pages/2_Data_Assistent.py", title="Data Assistent")
#create_page = st.Page("pages/1_Data_Assistent.py", title="Data Assistent", icon=":material/add_circle:")
SQL_assistent = st.Page("pages/3_Marketing_SQL_Assistent.py", title="Marketing SQL Assistent")
pdf_assistent = st.Page("pages/4_PDF_Assistent.py", title="PDF Assistent")
translation_engine = st.Page("pages/5_Translation_Engine.py", title="Translation Engine")




pg = st.navigation([hjem, data_assistent, SQL_assistent, pdf_assistent, translation_engine])
#st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()



        
left, logout_button_column = st.columns(2)


with left:
    google_button = st.button("Login with Google")

    if google_button:
        st.experimental_user.login(provider="google")



st.write(":sparkles: :rainbow[User data]")
st.write(st.experimental_user)
