import streamlit as st
import psycopg
import pandas as pd

dbconn = st.secrets["DBCONN"]

@st.cache_data(ttl=600)
def load_api_data():
    query = "SELECT date, value FROM api_data ORDER BY date"
    with psycopg.connect(dbconn) as conn:
        df = pd.read_sql(query, conn)
    return df

@st.cache_data(ttl=600)
def load_news():
    query = "SELECT date, title FROM news_ticker ORDER BY date DESC LIMIT 5"
    with psycopg.connect(dbconn) as conn:
        df = pd.read_sql(query, conn)
    return df

# Daten laden
api_df = load_api_data()
news_df = load_news()

# Datum als Index setzen für Linienplot
api_df["date"] = pd.to_datetime(api_df["date"])
api_df = api_df.set_index("date")

st.title("Bitcoin Daten und News")

st.subheader("Bitcoin Wertentwicklung")
st.line_chart(api_df["value"])

st.subheader("Neueste News")
for idx, row in news_df.iterrows():
    date_str = pd.to_datetime(row["date"]).strftime("%d.%m.%Y")
    st.markdown(f"**{date_str}** – {row['title']}")
