import os
import requests
import datetime
# hat kein psycopg2


def get_api_data():
    api_key = os.getenv("API_ALPHA")
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    endpoint = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey="
    response = requests.get(f" {endpoint}{api_key}").json()
    data = response["Time Series (Digital Currency Daily)"][today]
    data["date"] = today
    #print(data) # kann später entfernt werden
    return data


    # Connect to the PostgreSQL database


#get_api_data() # kann auch später entfernt werden -nur zu test zwecken