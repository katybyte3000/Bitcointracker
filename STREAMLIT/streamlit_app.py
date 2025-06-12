import streamlit as st

st.title("BITCOIN TRACKER")
st.write("Dies ist meine erste Streamlit-App in VS Code.")

import streamlit as st
import pandas as pd
import psycopg
from datetime import datetime

# Titel
st.title("📰 Bitcoin News Dashboard")

# Verbindung zur Supabase-Datenbank herstellen
db_url = st.secrets["DBCONN"]

@st.cache_data
def load_data():
    conn = psycopg.connect(db_url)
    query = "SELECT date, title FROM news_ticker;"
    df = pd.read_sql(query, conn)
    conn.close()

    # Datum konvertieren, falls noch nicht im datetime-Format
    df['date'] = pd.to_datetime(df['date'])

    return df

df = load_data()

# Gruppieren: Anzahl News pro Tag
df_count = df.groupby(df['date'].dt.date).size().reset_index(name='count')

# Plot
st.subheader("📈 Anzahl der Bitcoin-News pro Tag")
st.line_chart(df_count.set_index("date"))

# Optional: Liste der Titel unterhalb
with st.expander("🗂️ Alle News anzeigen"):
    st.dataframe(df.sort_values("date", ascending=False), use_container_width=True)
