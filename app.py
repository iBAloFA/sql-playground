import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os

st.set_page_config(page_title="SQL Playground", layout="wide")
st.title("SQL Playground")
st.caption("Connect to any SQLite/PostgreSQL · Run safe SELECT queries · Export results")

# Sidebar connection
with st.sidebar:
    st.header("Database Connection")
    db_type = st.radio("Database type", ["SQLite", "PostgreSQL"])
    
    if db_type == "SQLite":
        db_path = st.text_input("SQLite file path", "naija_employees.db")
        db_url = f"sqlite:///{db_path}"
    else:
        user = st.text_input("User", "postgres")
        password = st.text_input("Password", type="password")
        host = st.text_input("Host", "localhost")
        port = st.text_input("Port", "5432")
        dbname = st.text_input("Database name", "mydb")
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

    if st.button("Connect"):
        st.session_state.engine = create_engine(db_url)
        st.success("Connected successfully!")

# Main app
if "engine" in st.session_state:
    engine = st.session_state.engine
    
    # Show tables
    try:
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", engine)
        if not tables.empty:
            st.subheader("Tables")
            st.dataframe(tables, use_container_width=True)
    except:
        pass

    st.subheader("Run Query (SELECT only)")
    query = st.text_area("SQL", "SELECT * FROM employees LIMIT 10", height=150)

    if st.button("Run Query", type="primary"):
        if "SELECT" not in query.upper() or any(x in query.upper() for x in ["DROP","DELETE","UPDATE","INSERT","CREATE"]):
            st.error("Only SELECT queries allowed for safety!")
        else:
            with st.spinner("Running..."):
                try:
                    df = pd.read_sql(query, engine)
                    st.success(f"Query successful – {len(df):,} rows")
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False)
                    st.download_button("Download as CSV", csv, "result.csv", "text/csv")
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.info("Connect to a database using the sidebar →")

st.caption("Built by you · Day 6/31 of real Python database tools")
