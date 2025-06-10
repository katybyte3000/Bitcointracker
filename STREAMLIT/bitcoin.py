import streamlit as st
import psycopg
import pandas as pd

st.title("BITCOIN TRACKER")


def get_bitcoin_data(): 
    dbconn = st.secrets["DBCONN"]
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()

    cur.execute("SELECT * FROM api_data;")
    rows = cur.fetchall()
    colnames = [desc.name for desc in cur.description]
    conn.close()

    df = pd.DataFrame(rows, columns=colnames)
    return df

# Daten laden
df = get_bitcoin_data()

# Datum in Datumsformat umwandeln
df['date'] = pd.to_datetime(df['date'])

# Nach Datum sortieren
df = df.sort_values("date")

# Titel
st.title("Bitcoin Kursentwicklung")

selected_lines = st.multiselect(
    "Wähle Datenreihen:",
    ["open", "high", "low", "close", "volume"],
    default=["close"]
)

if selected_lines:
    st.line_chart(df.set_index("date")[selected_lines])
# Diagramm zeichnen: OHLC (Open, High, Low, Close)
#st.line_chart(df.set_index("date")[["open", "high", "low", "close"]])


def get_news_data():
    dbconn = st.secrets["DBCONN"]
    conn = psycopg.connect(dbconn)
    cur = conn.cursor()
    cur.execute("SELECT date, title FROM news_ticker ORDER BY date DESC LIMIT 5;")
    rows = cur.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=["date", "title"])

st.title("Bitcoin News")
st.write(get_news_data())