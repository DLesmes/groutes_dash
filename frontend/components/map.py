import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import BeautifyIcon

# Default route coordinates (example: two points in Bogotá)
DEFAULT_ROUTE = [
    (4.753851, -74.1019103),
    (4.7579942, -74.1059858)
]

def plot_routes(visits, use_default=False):
    if not visits and not use_default:
        st.info("No hay datos para mostrar en el mapa.")
        return

    # Use default route if requested
    if use_default:
        coordinates = DEFAULT_ROUTE
    else:
        # Extract coordinates in order
        coordinates = []
        for v in visits:
            lat = v.get("latitude") or v.get("lat")
            lon = v.get("longitude") or v.get("lon") or v.get("lng")
            if lat is not None and lon is not None:
                coordinates.append((lat, lon))

    if not coordinates:
        st.warning("No se encontraron coordenadas para el mapa.")
        return

    # Center map on the first point
    m = folium.Map(location=coordinates[0], zoom_start=12)

    # Draw the route as a line
    folium.PolyLine(coordinates, color="blue", weight=4, opacity=0.7, tooltip="Ruta").add_to(m)

    # Add friendly numbered markers using BeautifyIcon
    for idx, (lat, lon) in enumerate(coordinates, start=1):
        folium.Marker(
            [lat, lon],
            popup=f"Punto {idx}",
            icon=BeautifyIcon(
                number=idx,
                icon_shape='marker',
                border_color='#4a89dc',
                text_color='white',
                background_color='#4a89dc'
            )
        ).add_to(m)

    st_folium(m, width=1000, height=500)
