import psycopg2
import pandas as pd
import streamlit as st

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=st.secrets["db"]["host"],
        port=st.secrets["db"]["port"],
        dbname=st.secrets["db"]["dbname"],
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"]
    )

def run_query(query, params=None):
    conn = get_connection()
    return pd.read_sql(query, conn, params=params)
