import streamlit as st

def show_stats(visits):
    st.markdown("#### Estadísticas")
    if not visits:
        st.write("No hay datos para mostrar estadísticas.")
        return

    # Example: show origin, destination, duration if available
    # You can customize this based on your CSV columns
    try:
        origen = visits[0].get("place", "N/A")
        destino = visits[-1].get("place", "N/A")
        st.write(f"Origen: {origen}")
        st.write(f"Destino: {destino}")

        # If you have a duration column, show it; else, calculate from timestamps
        if "duration" in visits[0]:
            st.write(f"Duración: {visits[0]['duration']}")
        elif "timestamp" in visits[0]:
            from pandas import to_datetime
            t0 = to_datetime(visits[0]["timestamp"])
            t1 = to_datetime(visits[-1]["timestamp"])
            duration = (t1 - t0).total_seconds() / 3600
            st.write(f"Duración: {duration:.2f} horas")
    except Exception:
        st.write("No se pudieron calcular todas las estadísticas.")
