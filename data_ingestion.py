import os
import requests
import pandas as pd
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

load_dotenv()
 # Alpaca
client = StockHistoricalDataClient(
    os.getenv("ALPACA_API_KEY"), 
    os.getenv("ALPACA_SECRET_KEY")
)

# Example request to get historical stock bars for AAPL
request_params = StockBarsRequest(
    symbol_or_symbols=["AAPL"],
    timeframe=TimeFrame.Day,
    start="2026-10-01"
)

bars = client.get_stock_bars(request_params)
df = bars.df
df['SMA_10'] = df['close'].rolling(window=10).mean()

print(df[['close', 'SMA_10']].tail())

# Marketaux
marketaux_token = os.getenv("MARKETAUX_API_TOKEN")

url = f"https://api.marketaux.com/v1/news/all?symbols=AAPL&filter_entities=true&limit=3&api_token={marketaux_token}"
response = requests.get(url)

if response.status_code == 200:
    news_data = response.json()
    for article in news_data.get('data', []):
        print(f"- {article['title']}")
else:
    print(f"Error fetching news: {response.status_code} - {response.text}")