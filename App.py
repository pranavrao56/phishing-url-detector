import streamlit as st
from streamlit_navigation_bar import st_navbar
import pages as pg

st.set_page_config(initial_sidebar_state="collapsed")

pages = ['Home','About','Analysis','GitHub']

urls = {"GitHub": "https://github.com/pranavrao56/phishing-url-detector"}

options = {
    "show_sidebar": False,
}

page = st_navbar(
    pages,
    urls=urls,
    options=options,
)

functions = {
    "Home": pg.show_app,
    "About": pg.show_about,
    "Analysis": pg.show_analysis
}

go_to = functions.get(page)

if go_to:
    go_to()
    
