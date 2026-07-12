import streamlit as st
from dotenv import load_dotenv

from pages.home import home_page
from pages.objectives import objectives_page
from pages.analisis import analisis_page
from pages.conclusions import conclusions_page

load_dotenv()


def main():
    st.set_page_config(
        page_title="Soccer Analytic",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.navigation([
        st.Page("app.py", title="Inicio", icon="🏠"),
        st.Page("pages/objectives.py", title="Objetivos", icon="🎯"),
        st.Page("pages/analisis.py", title="Análisis", icon="📊"),
        st.Page("pages/conclusions.py", title="Conclusiones", icon="📝"),
    ], position="hidden")

    with st.sidebar:
        st.title("⚽ Soccer Analytic")
        st.subheader("Filtros")

        league_options = {
            "England": "Inglaterra",
            "Spain": "España",
            "France": "Francia",
            "Germany": "Alemania",
            "Italy": "Italia",
        }

        selected_league = st.selectbox(
            "Selecciona una liga",
            options=list(league_options.keys()),
            format_func=lambda x: league_options[x],
            index=0,
        )

    pages = {
        "Inicio": home_page,
        "Objetivos": objectives_page,
        "Análisis": analisis_page,
        "Conclusiones": conclusions_page,
    }

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Inicio"

    selected_page = st.radio(
        "Navegación",
        options=list(pages.keys()),
        index=list(pages.keys()).index(st.session_state["current_page"]),
        horizontal=True,
    )

    pages[selected_page]()


if __name__ == "__main__":
    main()
