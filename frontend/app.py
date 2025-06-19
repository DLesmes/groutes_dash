import streamlit as st
from components.sidebar import date_filter
from services.api import get_visits_by_date
from components.map import plot_routes
from components.stats import show_stats

st.set_page_config(page_title="Mapa de rutas", layout="wide")

# Sidebar: Date filter
selected_date = date_filter()

# Get data from backend
visits = get_visits_by_date(selected_date)

# Main UI
st.title(f"Mapa de rutas - visitas del {selected_date.strftime('%d %b %Y')}")
st.markdown("#### Filtros: fecha")
plot_routes(visits)
show_stats(visits)
