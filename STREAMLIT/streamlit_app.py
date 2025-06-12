import streamlit as st
import psycopg
import pandas as pd

st.title("BITCOIN TRACKER")
st.write("Dies ist meine erste Streamlit-App in VS Code.")

# Funktion für Bitcoin-Daten
def get_bitcoin_data(): 
    dbconn = st.secrets["DBCONN"]
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()

    cur.execute("SELECT timestamp, close FROM api_data ORDER BY timestamp;")
    rows = cur.fetchall()
    colnames = [desc.name for desc in cur.description]
    conn.close()

    df = pd.DataFrame(rows, columns=colnames)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

# Funktion für News-Ticker
def get_news():
    dbconn = st.secrets["DBCONN"]
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()

    cur.execute("SELECT date, title FROM news_ticker ORDER BY date DESC LIMIT 5;")
    rows = cur.fetchall()
    colnames = [desc.name for desc in cur.description]
    conn.close()

    df = pd.DataFrame(rows, columns=colnames)
    df["date"] = pd.to_datetime(df["date"])
    return df

# Daten laden
btc_df = get_bitcoin_data()
news_df = get_news()

# Linien-Diagramm anzeigen
st.subheader("Bitcoin Kursverlauf (Close-Preis)")
btc_df = btc_df.set_index("timestamp")
st.line_chart(btc_df["close"])

# News-Ticker anzeigen
st.subheader("Neueste Bitcoin News")
for _, row in news_df.iterrows():
    st.markdown(f"**{row['date'].strftime('%d.%m.%Y')}** – {row['title']}")
