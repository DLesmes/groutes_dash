import streamlit as st
from datetime import date
from components.sidebar import sidebar_navigation
from services.api import get_visits_by_date
from components.map import plot_routes
from components.stats import show_stats

st.set_page_config(page_title="Mapa de rutas", layout="wide")

# Sidebar navigation
page = sidebar_navigation()

if page == "🏷️ Etiquetador":
    # Date filter in main area
    col1, col2, col3 = st.columns([1,6,1])
    with col2:

        # Main UI
        st.title("🗺️ Mapa de rutas")
    
        selected_date = st.date_input(
            "Selecciona la fecha",
            value=date(2015, 6, 30),
            key="main_date_input"
        )

        # Main UI
        st.title(f"visitas del {selected_date.strftime('%d %b %Y')}")
        # Get data from backend
    
        visits = get_visits_by_date(selected_date)

        # Business day label
        if visits and "business_day" in visits[0]:
            if visits[0]["business_day"]:
                st.success("### 🟢 Día hábil")
            else:
                st.warning("### 🚩 Día no laboral")
        else:
            st.info("No hay información de día hábil para esta fecha.")

        # If no visits, show warning and plot default route
        use_default_route = not visits
        if use_default_route:
            st.warning("⚠️ No hay datos para la fecha seleccionada. Mostrando la ruta de ejemplo por defecto.")
        plot_routes(visits, use_default=use_default_route)
        if not use_default_route:
            show_stats(visits)

elif page == "ℹ️ Cómo funciona":
    st.markdown("""
    # ¡Hola! 👋  
    Esta página te permite explorar los lugares visitados por Uriel Mazabuel en días hábiles de los últimos 10 años.

    ---

    ### **¿Cómo usarla?**
                
    1️⃣ Selecciona una fecha usando el filtro principal.  
    2️⃣ Observa si fue un 🟢 día hábil o 🚩 día no laboral.  
    3️⃣ Mira la ruta y los puntos en el mapa.  
    4️⃣ Consulta las estadísticas del recorrido.

    ¡Diviértete explorando! 😄
    """)
