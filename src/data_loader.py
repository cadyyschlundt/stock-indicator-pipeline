#imports
import yfinance as yf
import pandas as pd
import os

#Paths
RAW_DATA_DIR = "../data/raw"

# Download OHLCV data for a list of tickers and save to CSV
def download_data(tickers, start_date):
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    data = yf.download(tickers, start=start_date)
    #Iterate through tickers and pull out data
    for ticker in tickers:
        df = data.xs(ticker, axis=1, level=1)
        df.to_csv(f"{RAW_DATA_DIR}/{ticker}.csv")
        print(f"Saved {ticker}.csv to {RAW_DATA_DIR}")

# Run the fuction
TICKERS = ["SPY", "QQQ", "AAPL"]
START_DATE = "2014-01-01"

download_data(TICKERS, START_DATE)

