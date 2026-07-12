import streamlit as st


def home_page():
    st.title("⚽ Soccer Analytic")
    st.markdown("### Análisis de Posesión en las 5 Grandes Ligas Europeas")

    league_names = {
        "England": "Premier League",
        "Spain": "La Liga",
        "France": "Ligue 1",
        "Germany": "Bundesliga",
        "Italy": "Serie A",
    }

    st.markdown("---")
    st.markdown("Bienvenido al dashboard de análisis de posesión de balón en las cinco grandes ligas europeas.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Ligas Analizadas", "5")

    with col2:
        st.metric("Equipos", "100+")

    with col3:
        st.metric("Partidos", "1000+")
