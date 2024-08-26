import streamlit as st
import dataManager
from PIL import Image

def page():
    citizen_name = st.query_params['citizen']
    citizen = dataManager.GetCitizenObj(citizen_name)
    if (citizen != None):
        st.header(citizen_name)
        st.image(Image.open(f"./citizen_pictures/{citizen_name}.png"))
        # offenses = "OFFENSES"
        # for offense in citizen.offenses:
            # offense: dataManager.Offense
            # offenses += f"\n{offense.type}"
        # if (len(citizen.offenses) <= 0):
            # offenses = "NO OFFENSES"
        # st.text(offenses)
        st.text(f"CITIZENSHIP STATUS: {citizen.get_citizenship().status_str()}")
        if (len(citizen.offenses) > 0):
            st.button("View in Criminal Database")
    else:
        st.error("Unable to locate citizen")
