import streamlit as st
import pageManager
import dataManager
import encrypt
import _pages.loginPage as auth


def page():
    st.query_params['settings'] = 'open'
    st.title("Account Settings")
    with (st.form("change_account_password")):
        st.header("Change Password")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        change_password_button = st.form_submit_button("Change Password")
        if (change_password_button):
            def rg():
                if (len(current_password) <= 0):
                    st.error("Please input your current password.")
                    return
                if (len(new_password) <= 0):
                    st.error("Please input the password you'd like.")
                    return
                dataManager.RefreshData()
                users = dataManager.Data['users']
                status = auth.GetAuthStatus()
                if (not auth.IsAuthenticated()):
                    pageManager.set_page("index")
                    return
                user = users[status.get("name")]
                encrypted_current_password = encrypt.sha256(current_password)
                encrypted_new_password = encrypt.sha256(new_password)
                if (encrypted_new_password == user.get("password")):
                    st.warning("This is already your current password.")
                    return
                if (encrypted_current_password == user.get("password")):
                    user['password'] = encrypted_new_password
                    dataManager.Commit()
                    auth.Authenticate(user['name'], encrypted_new_password)
                    st.success("Successfully changed your password!")
                else:
                    st.error("Invalid Credentials")

            rg()
