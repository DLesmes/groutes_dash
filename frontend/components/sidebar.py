import streamlit as st

def sidebar_navigation():
    st.sidebar.title("Secciones")
    page = st.sidebar.radio(
        "",
        ["ℹ️ Cómo funciona", "🏷️ Etiquetador"],
        index=2  # Default to how it works
    )
    return page
