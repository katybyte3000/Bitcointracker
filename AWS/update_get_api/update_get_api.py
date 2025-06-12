
import os
from datetime import datetime
import psycopg

# from dotenv import load_dotenv
# load_dotenv()


def update_data(data): 
  dbconn = os.getenv("DBCONN")
  print(dbconn)
  with psycopg.connect(dbconn) as conn:
          with conn.cursor() as cur:
              cur.execute(
                  '''
                  INSERT INTO api_data(date, open, high, low, close, volume)
                  VALUES (%s, %s, %s, %s, %s, %s)
                  ON CONFLICT (date) DO NOTHING;
                  ''',
                  (
                      datetime.strptime(data["date"], '%Y-%m-%d'),
                      float(data["1. open"]),
                      float(data["2. high"]),
                      float(data["3. low"]),
                      float(data["4. close"]),
                      float(data["5. volume"])
                  )
              )
          conn.commit()
          print(f"Daten für heute erfolgreich eingefügt.")

# for testing the function before AWS 
# update_data({
#   "1. open": "110300.25000000",
#   "2. high": "110306.91000000",
#   "3. low": "109832.68000000",
#   "4. close": "109862.29000000",
#   "5. volume": "87.23174785",
#   "date": "2025-06-11"
# }) 