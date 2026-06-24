## Current Progress
- Finished 01_data_loader.ipynb ✅
- Finished 02_indicators.ipynb ✅
- Finished 03_visualization.ipynb ✅

## Where we left off
- All three notebooks complete and committed
- Next step: 04_ notebook — run `ta` indicators on QQQ and AAPL to generate their feature CSVs (same way SPY_features.csv was made in 02_indicators.ipynb)
- After that, visualization will work for all 3 tickers automatically via the ticker loop in Cell 7

## Key decisions made
- Using `ta` library instead of pandas-ta (compatibility)
- Using CSV instead of parquet (pyarrow/fastparquet incompatible with Windows ARM)
- 3 tickers for now (SPY, QQQ, AAPL), expanding to 30+ later
- Working in notebooks first, then converting to .py files
- Feature table saved to data/processed/SPY_features.csv (2317 rows, 23 columns)
- Only SPY has a feature CSV right now — QQQ and AAPL only have raw data
- Matplotlib uses range(len(df)) for x-axis with manual date tick labels (Matplotlib doesn't handle datetime x-axes cleanly with candlesticks)
- Volume formatted as 100M instead of 1e8
- showlegend=False on RSI, MACD, Volume traces to avoid duplicate legend entries

## Notebook Summaries

### 01_data_loader.ipynb
- Downloads historical OHLCV data for SPY, QQQ, AAPL using yfinance
- Extracts each ticker into its own dataframe using xs()
- Saves each ticker as a CSV to data/raw/
- Shows how to reload from CSV to avoid re-downloading

### 02_indicators.ipynb
- Loads SPY from data/raw/SPY.csv
- Computes 23 columns of technical indicators using the `ta` library
- Indicators cover momentum (RSI, Stochastic, Williams %R, ROC), trend (MACD, SMA, EMA), volatility (Bollinger Bands, ATR), and volume (OBV)
- Drops NaN rows from indicator warmup periods (2516 → 2317 rows)
- Saves final feature table to data/processed/SPY_features.csv

## What 03_visualization.ipynb does
- Loads SPY_features.csv, filters to last 1 year (252 rows)
- `plot_plotly(df, ticker)` — interactive candlestick chart with hover tooltips
- `plot_matplotlib(df, ticker)` — same layout, saves PNG to results/charts/
- Both charts have 4 panels: price (candlesticks + BB + SMAs), volume, RSI, MACD
- Cell 7 loops through TICKERS and calls both functions — ready for 30+ tickers later