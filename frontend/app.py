import streamlit as st
from datetime import date
from components.sidebar import sidebar_sections
from services.api import get_visits_by_date
from components.map import plot_routes
from components.stats import show_stats

st.set_page_config(page_title="Mapa de rutas", layout="wide")

# Sidebar: Map section only
sidebar_sections()

# Date filter in main area
selected_date = st.date_input("Selecciona la fecha", value=date(2015, 6, 30), key="main_date_input")

# Main UI
st.title(f"🗺️ Mapa de rutas - visitas del {selected_date.strftime('%d %b %Y')}")

# Get data from backend
visits = get_visits_by_date(selected_date)

# Business day label
if visits and "business_day" in visits[0]:
    if visits[0]["business_day"]:
        st.markdown("### 🟢 dia hábil")
    else:
        st.markdown("### 🚩 día no laboral")
else:
    st.markdown("### 🚩 día no laboral")  # Default if no data or key missing
# Map and stats
plot_routes(visits)
show_stats(visits)

# About section in main area
st.markdown("""
### ℹ️ Acerca de

¡Hola! 👋  
Esta página te permite explorar los lugares visitados por Uriel Mazabuel en días hábiles de los últimos 10 años.

**¿Cómo usarla?**
1️⃣ Selecciona una fecha usando el filtro principal.  
2️⃣ Observa si fue un 🟢 día hábil o 🚩 día no laboral.  
3️⃣ Mira la ruta y los puntos en el mapa.  
4️⃣ Consulta las estadísticas del recorrido.

¡Diviértete explorando! 😄
""")


