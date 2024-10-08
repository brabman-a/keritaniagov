import streamlit as st
import dataManager
import pageManager

def page():
    agent_name = st.query_params['agent']
    dataManager.RefreshData()
    agent = dataManager.Data['users'].get(agent_name)
    if (agent != None):
        st.title(agent_name)
        if (dataManager.Data['citizens'].get(agent_name) != None):
            citizen_data_view = st.button("View in Citizen Database")
            if (citizen_data_view):
                st.query_params['agent'] = None
                st.query_params['citizen'] = agent_name
                pageManager.set_page("citizen")
        st.header("Details")
        st.text(f"DAY REGISTERED: {agent.get('day_registered')}")
    else:
        st.error("Unable to locate agent")
