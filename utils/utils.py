import streamlit as st
import pandas as pd

def show_csv(filepath):
    df = pd.read_csv(filepath)

    column_config = {}
    for col in df.columns:
        if df[col].astype(str).str.startswith(("http://", "https://")).any():
            column_config[col] = st.column_config.LinkColumn(col)

    st.dataframe(df, column_config=column_config)
    return df

def export_csv(data,path):
    pd.DataFrame(data).to_csv(path,index=False)

