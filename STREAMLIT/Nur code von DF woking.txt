import streamlit as st
import psycopg
import pandas as pd

st.title("BITCOIN TRACKER")
st.write("Dies ist meine erste Streamlit-App in VS Code.")

def get_bitcoin_data(): 
    dbconn = st.secrets["DBCONN"]
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()

    cur.execute("SELECT * FROM api_data;")
    rows = cur.fetchall()
    colnames = [desc.name for desc in cur.description]
    conn.close()

    return rows, colnames


# Daten abrufen
rows, columns = get_bitcoin_data()

# Ausgabe in der App anzeigen
st.title("Bitcoin Daten")
st.write("Anzahl Datensätze:", len(rows))
st.dataframe(rows, column_config={col: None for col in columns})
