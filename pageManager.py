import streamlit as st

# placeholder = None

def set_page(page):
    st.query_params['page'] = page
    st.rerun()

# Function to get the current page from the URL
def get_current_page():
    query_params = st.query_params
    return query_params.get("page", ["home"])[0]

# def updatePage():
#     global placeholder
#     print("Updating page...")
#     if (placeholder != None):
#         placeholder.empty()
#     page = st.session_state['page']
#     print(f"Page: {page}")
#     match (page):
#         case ('login'):
#             if (loginPage.IsAuthenticated()):
#                 st.session_state['page'] = 'index'
#                 return updatePage()
#             loginPage.page()
#             placeholder = loginPage.placeholder
#         case ('index'):
#             if (not loginPage.IsAuthenticated()):
#                 st.session_state['page'] = 'login'
#                 return updatePage()
#             indexPage.page()
#             placeholder = indexPage.placeholder
#         case _:
#             st.session_state['page'] = 'index'
#             return updatePage()
