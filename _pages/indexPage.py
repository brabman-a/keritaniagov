import streamlit as st
import _pages.loginPage as auth
import _pages.settingsPage as settingsPage
import pageManager
import time
import dataManager
import encrypt

# placeholder = st.empty()

def page():
    # with (placeholder):
    # if (not auth.IsAuthenticated()):
        # pageManager.set_page("login")
        # return
    if (st.query_params.get("settings") == "open"):
        settingsPage.page()
        return
    AuthStatus = auth.GetAuthStatus()
    UserData = dataManager.GetUser(AuthStatus.get("name"))
    Permission = UserData.get("permission")
    st.title("Welcome, " + UserData.get("name"))
    with (st.form("citizen_lookup")):
        st.header("Citizen Lookup")
        st.text("Lookup a citizen in the Keritania Citizen Database")
        citizen_name = st.text_input("Name")
        search_citizen = st.form_submit_button("Lookup")
        if (search_citizen):
            citizen = dataManager.GetCitizenObj(citizen_name)
            if (citizen != None):
                st.success("Success! Redirecting...")
                time.sleep(0.2)
                st.query_params['citizen'] = citizen_name
                time.sleep(0.1)
                pageManager.set_page("citizen")
            else:
                st.error("Could not locate citizen in citizen database")
    if (Permission >= 2):
        with (st.form("citizen_register")):
            st.header("Register Citizen")
            st.text("Register a new citizen in the Keritania Citizen Database")
            new_name = st.text_input("Name")
            pfp = st.file_uploader("Image", type=["png"])
            day_registered = st.number_input("Day Registered", value = 0, step = 1, format="%d")
            register = st.form_submit_button("Register")
            if (register):
                st.text("Please wait...")
                print('register onclick')
                def rg():
                    print('register')
                    st.warning("Please wait...")
                    time.sleep(0.1)
                    if (len(new_name) <= 0):
                        st.error("Please input a name.")
                        return
                    if (pfp is None):
                        st.error("Please input an image of the Citizen.")
                        return
                    if (day_registered is None):
                        st.error("Please input a data registered for the citizen.")
                        return
                    if (dataManager.GetCitizenObj(new_name) != None):
                        st.error("This citizen already exists.")
                        return
                    with open(f"./citizen_pictures/{new_name}.png", "wb") as f:
                        f.write(pfp.getbuffer())
                    st.success("Success! Redirecting...")
                    citizen = dataManager.Citizen(new_name, [], [], dataManager.Citizenship(0), day_registered = day_registered)
                    citizen.commit()
                time.sleep(0.5)
                rg()
    if (Permission >= 3):
        with (st.form("Government Agent Lookup")):
            st.header("Government Agent Lookup")
            st.text("Lookup a government agent in the Keritania Government Database.")
            name = st.text_input("Name")
            lookup = st.form_submit_button("Lookup")
            if (lookup):
                def rg():
                    if (len(name) <= 0):
                        st.error("Please input a name.")
                        return
                    dataManager.RefreshData()
                    agent_found = dataManager.Data['users'].get(name)
                    if (agent_found != None):
                        st.query_params['agent'] = name
                        pageManager.set_page("agent")
                        
                rg()
        with (st.form("Government Register")):
            st.header("Register Government Agent")
            st.text("Register a new government agent in the Keritania Government Database.")
            name = st.text_input("Name")
            password = st.text_input("Password", type = "password")
            permissions_dropdown_options = {
                "0 (Cannot log into government terminal)": 0,
                "1 (Can perform Citizen Lookup and edit existing citizens)": 1,
                "2 (Can register new citizens)": 2,
                "3 (Can perform Government Agent Lookup, register new government agents, and edit existing government agents)": 3,
                "4 (View confidential documents)": 4,
                "5 (Give other agents permission to view confidential documents)": 5
            }
            permission_gov_input = st.selectbox(
                "Permission Level",
                list(permissions_dropdown_options.keys())
            )
            day_registered_gov = st.number_input("Day Registered", value = 0, step = 1, format="%d")
            register_gov_agent_button = st.form_submit_button("Register")
            if (register_gov_agent_button):
                def rg():
                    st.warning("Please wait...")
                    time.sleep(0.1)
                    if (name is None):
                        st.error("Please input a name.")
                        return
                    if (password is None):
                        st.error("Please input a password.")
                        return
                    if (permission_gov_input is None):
                        st.error("Please input a permission.")
                        return
                    if (day_registered_gov is None):
                        st.error("Please input a day registered.")
                        return
                    dataManager.RefreshData()
                    print(dataManager.Data)
                    if (dataManager.Data['users'].get(name) == None):
                        dataManager.SetUser(name, {
                            'name': name,
                            'password': encrypt.sha256(password),
                            'permission': permissions_dropdown_options.get(permission_gov_input),
                            'day_registered': day_registered_gov
                        })
                        st.success("Registered agent successfully")
                    else:
                        st.error("An agent with that username already exists")
                rg()
    logout_button = st.button("Logout")
    if (logout_button):
        auth.DeAuthenticate()
        pageManager.set_page("login")
    settings_button = st.button("Settings")
    if (settings_button):
        print("settings button pressed")
        auth.UpdateAuthStatus()
        if (not auth.IsAuthenticated()):
            pageManager.set_page("index")
            return
        st.query_params["settings"] = "open"
        pageManager.set_page("index")
                



    # st.title(f"Welcome, {AuthStatus.get('name')}")
