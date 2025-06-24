import streamlit as st
from datetime import date

def date_filter():
    st.sidebar.header("Filtros")
    selected_date = st.sidebar.date_input("Selecciona la fecha", value=date(2015, 6, 30))
    return selected_date
