import pandas as pd
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"


def generate_signals(ticker, output_dir=None):
    if output_dir is None:
        output_dir = PROCESSED_PATH
    df = pd.read_csv(PROCESSED_PATH / f"{ticker}_features.csv", index_col="Date", parse_dates=True)
    df["Signal"] = "hold"
    df.loc[(df["RSI"] < 30) & (df["MACD"] > df["MACD_Signal"]) & (df["Close"] < df["BB_Lower"]), "Signal"] = "long"
    df.loc[(df["RSI"] > 70) & (df["MACD"] < df["MACD_Signal"]) & (df["Close"] > df["BB_Upper"]), "Signal"] = "short"

    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / f"{ticker}_signals.csv")
    print(f"{ticker}: {(df['Signal'] == 'long').sum()} long, {(df['Signal'] == 'short').sum()} short, {(df['Signal'] == 'hold').sum()} hold")
    print(f"Saved to {output_dir / f'{ticker}_signals.csv'}")

    return df

# Run
TICKERS = ["SPY", "QQQ", "AAPL"]

for ticker in TICKERS:
    generate_signals(ticker)
