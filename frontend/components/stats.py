import streamlit as st
from pandas import to_datetime

def show_stats(visits):
    st.markdown("#### Estadísticas")
    if not visits:
        st.write("No hay datos para mostrar estadísticas.")
        return

    try:
        # Calculate and show duration in a friendly format
        if "duration" in visits[0]:
            st.write(f"**Duración:** {visits[0]['duration']}")
        elif "timestamp" in visits[0]:
            t0 = to_datetime(visits[0]["timestamp"])
            t1 = to_datetime(visits[-1]["timestamp"])
            total_seconds = int((t1 - t0).total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            duration_str = []
            if hours:
                duration_str.append(f"{hours} hora{'s' if hours > 1 else ''}")
            if minutes or not duration_str:
                duration_str.append(f"{minutes} minuto{'s' if minutes != 1 else ''}")
            st.write(f"**Duración:** {' '.join(duration_str)}")
            
        # List all points with their order and place
        st.markdown("**Puntos del recorrido:**")
        for idx, v in enumerate(visits, start=1):
            st.write(f"{idx}. {v.get('place', 'N/A')}")


    except Exception:
        st.write("No se pudieron calcular todas las estadísticas.")
