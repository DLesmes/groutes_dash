import streamlit as st
import folium
from streamlit_folium import st_folium

def plot_routes(visits):
    if not visits:
        st.info("No hay datos para mostrar en el mapa.")
        return

    # Use the first point as map center
    first = visits[0]
    lat = first.get("latitude") or first.get("lat")
    lon = first.get("longitude") or first.get("lon") or first.get("lng")
    if lat is None or lon is None:
        st.warning("No se encontraron coordenadas para el mapa.")
        return

    m = folium.Map(location=[lat, lon], zoom_start=12)

    # Plot all points
    for v in visits:
        lat1 = v.get("latitude") or v.get("lat")
        lon1 = v.get("longitude") or v.get("lon") or v.get("lng")
        if lat1 is not None and lon1 is not None:
            folium.Marker([lat1, lon1], popup=v.get("place", "Lugar")).add_to(m)

    st_folium(m, width=700, height=400)
