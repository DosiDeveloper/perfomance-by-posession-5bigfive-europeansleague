import streamlit as st


def objectives_page():
    st.title("Planteamiento del problema")
    st.text(
        "El fútbol es el deporte más popular del mundo, con millones de aficionados y una gran cantidad de datos disponibles. Sin embargo, el análisis de estos datos puede ser complejo y requiere herramientas adecuadas para extraer información útil. En este proyecto, nos proponemos analizar el rendimiento de los equipos en la posesión del balón en las cinco grandes ligas europeas (Premier League, La Liga, Serie A, Bundesliga y Ligue 1) utilizando técnicas de análisis de datos y visualización."
    )
    st.title("Objetivos")
    st.markdown("---")
    st.markdown("### Objetivos")
    st.markdown(
        "- Normalizar y limpiar los datos de posesión del balón de las cinco grandes ligas europeas para su análisis posterior."
    )
    st.markdown(
        "- Transformar los registros crudos en un Data Lake limpio (Parquet) para optimizar la carga computacional durante el análisis descriptivo."
    )
    st.markdown(
        "- Analizar el rendimiento de los equipos en la posesión del balón en las cinco grandes ligas europeas."
    )
    st.markdown(
        "- Identificar patrones y tendencias en el rendimiento de los equipos en la posesión del balón."
    )
    st.markdown(
        "- Desarrollar una aplicación web interactiva para visualizar los resultados del análisis de datos."
    )
    st.markdown(
        "- Proporcionar insights y recomendaciones basados en el análisis de datos para mejorar el rendimiento de los equipos en la posesión del balón."
    )
