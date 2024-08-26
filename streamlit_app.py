import streamlit as st
import pageManager
import dataManager
import _pages.loginPage as loginPage
import _pages.indexPage as indexPage
import _pages.citizenPage as citizenPage
import _pages.agentPage as agentPage

def get_current_page():
    query_params = st.query_params
    x = query_params.get("page", "index")
    print(x)
    return x

pages = {
    'login': loginPage.page,
    'index': indexPage.page,
    'citizen': citizenPage.page,
    'agent': agentPage.page
}

def NotFound():
    st.error("404: Page not found")

page = get_current_page()
if (page in pages):
    if (page == "index"):
        if (not loginPage.IsAuthenticated()):
            page = "login"
    elif (page == "login"):
        if (loginPage.IsAuthenticated()):
            page = "index"
    pages[page]()
else:
    NotFound()


