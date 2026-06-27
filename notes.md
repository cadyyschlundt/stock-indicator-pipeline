## Current Progress
- Finished 01_data_loader.ipynb 
- Finished 02_indicators.ipynb 
- Finished 03_visualization.ipynb 
- Finished 04_build_features.ipynb
- Finished 05_visualization_batch.ipynb
- Finished src/data_loader.py
- Finished src/indicators.py
- Finished src/visualizers.py

## Where I left off
- visualizers.py complete and committed
- Next step: signals.py (new logic, not from a notebook)
- After that: test_indicators.py in tests/

## Key decisions made
- Using `ta` library instead of pandas-ta (compatibility)
- Using CSV instead of parquet (pyarrow/fastparquet incompatible with Windows ARM)
- 3 tickers for now (SPY, QQQ, AAPL), expanding to 30+ later
- Working in notebooks first, then converting to .py files
- Feature table saved to data/processed/SPY_features.csv (2317 rows, 23 columns)
- Matplotlib uses range(len(df)) for x-axis with manual date tick labels (Matplotlib doesn't handle datetime x-axes cleanly with candlesticks)
- Volume formatted as 100M instead of 1e8
- showlegend=False on RSI, MACD, Volume traces to avoid duplicate legend entries
- LOOKBACK_DAYS = 365 (calendar days, results in ~252 trading day rows)
- Constants use all caps (TICKERS, START_DATE, etc.)
- Function parameters use lowercase (tickers, start_date, etc.)
- plot_plotly saves as HTML to results/charts/ instead of showing in browser
- plot_matplotlib saves as PNG to results/charts/

## .py File Conventions Established
- Comments above each section (# Imports, # Paths, # Run etc.)
- Constants defined at the top, caller block at the bottom
- Logic wrapped in functions so other files can import them
- Path(__file__).resolve().parent.parent for project root (replaces os.chdir approach)
- Path / operator for joining paths (replaces os.path.join)

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
- Hardcoded to SPY -- 04 is the scaled version

### 03_visualization.ipynb
- Loads SPY_features.csv, filters to last 1 year (365 days → ~252 rows)
- `plot_plotly(df, ticker)` — interactive candlestick chart with hover tooltips
- `plot_matplotlib(df, ticker)` — same layout, saves PNG to results/charts/
- Both charts have 4 panels: price (candlesticks + BB + SMAs), volume, RSI, MACD
- Hardcoded to SPY -- 05 is the scaled version

### 04_build_features.ipynb
- Loops through all 3 tickers (SPY, QQQ, AAPL)
- Parameterizes the indicator pipeline from 02_ using ticker as the loop variable
- For each ticker: loads raw CSV → computes 23 indicators → drops NaN rows → saves feature CSV
- All three feature CSVs are identical in structure (2317 rows, 23 columns)
- Uses os.chdir("..") to set working directory to project root before reading/writing files

### 05_visualization_batch.ipynb
- Scaled version of 03_visualization.ipynb
- Loops through SPY, QQQ, AAPL
- For each ticker: loads feature CSV from data/processed/, applies 365 day LOOKBACK_DAYS cutoff, calls plot_plotly and plot_matplotlib
- PNG charts saved to results/charts/ for all 3 tickers
- Ready to scale to 30+ tickers later
- Uses Path("..") for relative paths (same pattern as 03)

## src/ File Summaries

### data_loader.py
- Single function: download_data(tickers, start_date)
- Downloads OHLCV data via yfinance for all tickers in one call
- Loops through tickers, extracts each with xs(), saves to data/raw/
- Creates data/raw/ folder if it doesn't exist
- Caller at bottom: TICKERS = ["SPY", "QQQ", "AAPL"], START_DATE = "2014-01-01"

### indicators.py
- Single function: compute_indicators(ticker, output_dir=None)
- Loads raw CSV from data/raw/, computes 23 technical indicators using ta library
- Drops NaN rows from indicator warmup periods (199 rows dropped, SMA_200 is the longest)
- Saves feature CSV to data/processed/, returns dataframe
- Uses Path(__file__) for reliable path handling
- Caller at bottom: TICKERS = ["SPY", "QQQ", "AAPL"]

### visualizers.py
- Three functions: plot_plotly, plot_matplotlib, create_visualizations
- plot_plotly saves interactive chart as HTML to results/charts/
- plot_matplotlib saves static chart as PNG to results/charts/
- create_visualizations(ticker) loads feature CSV, applies LOOKBACK_DAYS cutoff, calls both plot functions
- Caller at bottom: TICKERS = ["SPY", "QQQ", "AAPL"]