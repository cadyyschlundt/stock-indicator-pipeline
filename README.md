# stock-indicator-pipeline



\## About

This project computes over 15 financial indicators for over 30 tickers, creates signal visualizations for each ticker, and provides position signals according to some of the indicators. A goal of mine this summer is to improve my ability to code and understand important financial concepts and market dynamics. This project is the foundation for future projects, which will feed into a full-stack ML app that predicts short-term stock direction.



\## AI Usage

This project was built with the help of AI, mainly in the first three notebooks. A goal of mine this summer is to improve my ability to code and understand important financial concepts and market dynamics. I instructed the AI to guide me through the project, so if I got stuck it would help me get to where I need to be. Additionally, I would not let it generate code unless explicitly told. Notebooks 02 and 03 were built with more AI assistance to make sure I understood the pattern for certain functions. I then used them as a reference to build 04 and 05 independently, which loop through all 35 tickers.



\## Architecture



yfinance → data\_loader → indicators → visualizers → signals

&#x20;                               ↓

&#x20;                        results/charts (PNG + HTML)



\## Indicators



| Indicator | Category | What it measures |

|-----------|----------|-----------------|

| RSI (14) | Momentum | Overbought/oversold conditions |

| Stochastic %K/%D | Momentum | Price position relative to recent range |

| Williams %R | Momentum | Closing price relative to high-low range |

| ROC (12) | Momentum | Rate of price change over 12 days |

| MACD | Trend | Difference between 12 and 26 day EMAs |

| SMA (20, 50, 200) | Trend | Average price over 20, 50, and 200 days |

| EMA (12, 26) | Trend | Exponentially weighted average moving average |

| Bollinger Bands (20, 2) | Volatility | Price envelope based on standard deviation |

| ATR (14) | Volatility | Average range between high and low over 14 days |

| OBV | Volume | Cumulative buying and selling pressure |



\## How to Run



1\. Clone the repo

git clone https://github.com/yourusername/stock-indicators-pipeline.git

cd stock-indicators-pipeline



2\. Create a virtual environment and install dependencies

python -m venv .venv

.venv\\Scripts\\activate

pip install -r requirements.txt



3\. Download historical data

python src/data\_loader.py



4\. Compute technical indicators

python src/indicators.py



5\. Generate charts

python src/visualizers.py



6\. Generate trading signals

python src/signals.py



7\. Run tests

pytest tests/test\_indicators.py -v



Charts are saved to results/charts/ as both PNG and interactive HTML files.





\## Results



!\[SPY Chart](results/charts/SPY\_chart.png)



Running the full pipeline produces:

\- 35 feature CSVs with 23 indicator columns each (\~2,940 rows per ticker)

\- 35 interactive HTML charts saved to results/charts/

\- 35 static PNG charts saved to results/charts/

\- 35 signal CSVs with long/short/hold positions for each ticker



\## Tech Stack

\- Data: yfinance, pandas, numpy

\- Indicators: ta

\- Visualization: plotly, matplotlib

\- Testing: pytest













