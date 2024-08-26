import streamlit as st
import dataManager
import encrypt
from streamlit_cookies_controller import CookieController
import time

controller = CookieController()

# placeholder = st.empty()

def UpdateAuthStatus():
    print("Updating auth status...")
    authStatus = controller.get("KGovAuth")
    if (authStatus == None): return
    userData = dataManager.GetUser(authStatus.get("name"))
    if (userData):
        if (authStatus.get("password") != encrypt.sha256(userData.get("password"))):
            print(authStatus.get("password"), userData.get("password"))
            print("Deauthenticating due to incorrect password")
            DeAuthenticate()
    else:
        print("Deauthenticating due to no user data field")
        DeAuthenticate()

def GetAuthStatus():
    UpdateAuthStatus()
    return controller.get("KGovAuth")

def IsAuthenticated():
    return GetAuthStatus() != None

def Authenticate(name, password):
    print(f"{name}: {password}")
    controller.set("KGovAuth", {
        'name': name,
        'password': encrypt.sha256(password),
        'auth': True
    })
    UpdateAuthStatus()

def DeAuthenticate():
    controller.set("KGovAuth", None)

def doSubmit(name, password):
    # print(len(name), len(password))
    if len(name) <= 0:
        st.error("You must input an identifier to login.")
        return
    if len(password) <= 0:
        st.error("You must input a password to login.")
        return
    user = dataManager.GetUser(name)
    if (not user):
        # print('invalid credentials')
        st.error("Invalid credentials")
        return
    if (user.get("password") == password):
        if (user.get("permission") > 0):
            st.success("Logging in...")
            Authenticate(name, password)
            if (IsAuthenticated()):
                print("Successfully Authenticated")
                import pageManager
                # st.session_state['page'] = 'index'
                pageManager.set_page("index")
                # pageManager.updatePage()
            else:
                print("Unverified Authentication")
        else:
            st.warning("You currently do not have permission to login.")
    else:
        st.error("Invalid credentials")


def page():
    import pageManager
    if (IsAuthenticated()):
        pageManager.set_page("index")
        return
    # with (placeholder):
    with (st.form("login")):
        name = st.text_input("Identifier")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    if (submit):
        doSubmit(name, password)
        # print('w')

