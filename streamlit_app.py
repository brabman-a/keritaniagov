import streamlit as st
import pageManager
import dataManager
import _pages.loginPage as loginPage
import _pages.indexPage as indexPage

def get_current_page():
    query_params = st.query_params
    x = query_params.get("page", "index")
    print(x)
    return x

pages = {
    'login': loginPage.page,
    'index': indexPage.page
}

page = get_current_page()
if (page in pages):
    pages[page]()
else:
    st.error("404: Page not found")


