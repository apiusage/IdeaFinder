
import streamlit as st
from services.discovery_service import discover

st.title("Discover")
if st.button("Find Ideas"):
    for x in discover():
        st.metric(x["title"],x["score"])
        st.write(x["description"])
        st.divider()
