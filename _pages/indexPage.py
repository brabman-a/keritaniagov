import streamlit as st
import _pages.loginPage as auth
import pageManager
import time

# placeholder = st.empty()

def page():
    # with (placeholder):
    if (not auth.IsAuthenticated()):
        pageManager.set_page("login")
        return
    AuthStatus = auth.GetAuthStatus()
    st.title(f"Welcome, {AuthStatus.get('name')}")
