import pandas as pd
from src.indicators import compute_indicators


def test_output_is_dataframe():
    df = compute_indicators("SPY")
    assert isinstance(df, pd.DataFrame)

def test_expected_columns():
    df = compute_indicators("SPY")
    expected_columns = ["RSI", "MACD", "MACD_Signal", "MACD_Hist", "BB_Upper", "BB_Middle", "BB_Lower", "SMA_20",
                        "SMA_50", "SMA_200", "EMA_12", "EMA_26", "ATR", "OBV", "Stoch_K", "Stoch_D", "Williams_R",
                        "ROC"]
    assert all(col in df.columns for col in expected_columns)

def test_no_nulls():
    df = compute_indicators("SPY")
    assert df.isnull().any().any() == False

def test_rsi_range():
    df = compute_indicators("SPY")
    assert df["RSI"].min() >= 0
    assert df["RSI"].max() <= 100