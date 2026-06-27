import pandas as pd
import ta
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

# Build features for all tickers
def compute_indicators(ticker, output_dir=None):
    if output_dir is None:
        output_dir = PROCESSED_PATH
    df = pd.read_csv(RAW_PATH / f"{ticker}.csv", index_col="Date", parse_dates=True)
    rows_before = len(df)
    ## relative strength index
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()

    ##moving average convergence divergence
    macd = ta.trend.MACD(df["Close"], window_slow=26, window_fast=12, window_sign=9)

    df["MACD"] = macd.macd()
    df["MACD_Signal"] = macd.macd_signal()
    df["MACD_Hist"] = macd.macd_diff()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df["Close"], window=20, window_dev=2)

    df["BB_Upper"] = bb.bollinger_hband()
    df["BB_Middle"] = bb.bollinger_mavg()
    df["BB_Lower"] = bb.bollinger_lband()

    # Simple Moving Averages
    df["SMA_20"] = ta.trend.SMAIndicator(df["Close"], window=20).sma_indicator()
    df["SMA_50"] = ta.trend.SMAIndicator(df["Close"], window=50).sma_indicator()
    df["SMA_200"] = ta.trend.SMAIndicator(df["Close"], window=200).sma_indicator()

    # Exponential Moving Averages
    df["EMA_12"] = ta.trend.EMAIndicator(df["Close"], window=12).ema_indicator()
    df["EMA_26"] = ta.trend.EMAIndicator(df["Close"], window=26).ema_indicator()

    # ATR - Average True Range (volatility)
    df["ATR"] = ta.volatility.AverageTrueRange(
        df["High"], df["Low"], df["Close"], window=14
    ).average_true_range()

    # OBV - On Balance Volume
    df["OBV"] = ta.volume.OnBalanceVolumeIndicator(
        df["Close"], df["Volume"]
    ).on_balance_volume()
    ##Schochastic Oscillator
    stoch = ta.momentum.StochasticOscillator(
        df["High"], df["Low"], df["Close"], window=14, smooth_window=3
    )
    df["Stoch_K"] = stoch.stoch()
    df["Stoch_D"] = stoch.stoch_signal()

    # Williams %R
    df["Williams_R"] = ta.momentum.WilliamsRIndicator(
        df["High"], df["Low"], df["Close"], lbp=14
    ).williams_r()

    # Rate of Change
    df["ROC"] = ta.momentum.ROCIndicator(df["Close"], window=12).roc()

    df = df.dropna()

    rows_after = len(df)

    print(f"{ticker}: dropped {rows_before - rows_after} rows, {rows_after} rows remaining")

    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / f"{ticker}_features.csv")
    print(f"Saved to {output_dir / f'{ticker}_features.csv'}")

    return df


# Run
TICKERS = ["SPY", "QQQ", "IWM", "DIA", "GLD", "TLT", "XLE", "AAPL", "MSFT", "GOOGL", "NVDA", "META", "AMD", "JPM", "BAC", "GS", "V", "MA", "JNJ", "UNH", "PFE", "ABBV", "MRK", "XOM", "CVX", "COP", "SLB", "AMZN", "TSLA", "HD", "MCD", "CAT", "BA", "HON", "UPS"]

if __name__ == "__main__":
    for ticker in TICKERS:
        compute_indicators(ticker)

