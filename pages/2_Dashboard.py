
import streamlit as st
import pandas as pd
st.title("Dashboard")
df=pd.DataFrame([
 {"Idea":"AI Proposal Writer","Score":88},
 {"Idea":"AI Compliance Copilot","Score":91},
])
st.dataframe(df,use_container_width=True)
