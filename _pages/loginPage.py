import streamlit as st
import dataManager
import encrypt
from streamlit_cookies_controller import CookieController
import time
import encrypt

controller = CookieController()

# placeholder = st.empty()

def UpdateAuthStatus():
    # print("Updating auth status...")
    authStatus = controller.get("KGovAuth")
    if (authStatus == None): return
    userData = dataManager.GetUser(authStatus.get("name"))
    if (userData):
        if (authStatus.get("password") != userData.get("password")):
            print(authStatus.get("password"), userData.get("password"))
            print("Deauthenticating due to incorrect password")
            DeAuthenticate()
    else:
        # print("Deauthenticating due to no user data field")
        DeAuthenticate()

def GetAuthStatus():
    UpdateAuthStatus()
    return controller.get("KGovAuth")

def IsAuthenticated():
    return GetAuthStatus() != None

def Authenticate(name, password):
    # print(f"{name}: {password}")
    controller.set("KGovAuth", {
        'name': name,
        'password': password,
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
    encrypted_password = encrypt.sha256(password)
    if (encrypted_password == user.get("password")):
        if (user.get("permission") > 0):
            st.success("Logging in...")
            Authenticate(name, encrypted_password)
            time.sleep(0.5)
            if (IsAuthenticated()):
                # print("Successfully Authenticated")
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
    for key in st.query_params:
        if (key != "page"):
            st.query_params.pop(key)
    # if (IsAuthenticated()):
        # pageManager.set_page("index")
        # return
    # with (placeholder):
    with (st.form("login")):
        name = st.text_input("Identifier")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
    if (submit):
        doSubmit(name, password)
        # print('w')

