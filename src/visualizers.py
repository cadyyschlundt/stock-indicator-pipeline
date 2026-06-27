import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

#  Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"
CHARTS_PATH = PROJECT_ROOT / "results" / "charts"
CHARTS_PATH.mkdir(parents=True, exist_ok=True)

TICKERS = ["SPY", "QQQ", "AAPL"]
LOOKBACK_DAYS = 365

# Define function and set up chart structure
def plot_plotly(df, ticker):
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.5, 0.15, 0.15, 0.2],
        subplot_titles=(ticker, "Volume", "RSI", "MACD")
    )

    # Candlesticks
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'],
        name="Price"
    ), row=1, col=1)

    # Bollinger Bands
    for col, color, name in [
        ('BB_Upper', 'rgba(173,216,230,0.4)', 'BB Upper'),
        ('BB_Middle', 'rgba(100,149,237,0.8)', 'BB Mid'),
        ('BB_Lower', 'rgba(173,216,230,0.4)', 'BB Lower'),
    ]:
        fig.add_trace(go.Scatter(
            x=df.index, y=df[col],
            line=dict(color=color, width=1),
            name=name
        ), row=1, col=1)

    # SMAs
    for col, color, name in [
        ('SMA_20', 'orange', 'SMA 20'),
        ('SMA_50', 'purple', 'SMA 50'),
        ('SMA_200', 'red', 'SMA 200'),
    ]:
        fig.add_trace(go.Scatter(
            x=df.index, y=df[col],
            line=dict(color=color, width=1),
            name=name
        ), row=1, col=1)

    # Volume
    colors = ['green' if c >= o else 'red' for c, o in zip(df['Close'], df['Open'])]
    fig.add_trace(go.Bar(
        x=df.index, y=df['Volume'],
        marker_color=colors, name="Volume",
        showlegend=False
    ), row=2, col=1)

    # RSI
    fig.add_trace(go.Scatter(
        x=df.index, y=df['RSI'],
        line=dict(color='orange', width=1), name="RSI",
        showlegend=False
    ), row=3, col=1)
    for level, color in [(70, 'red'), (30, 'green')]:
        fig.add_hline(y=level, line_dash="dash", line_color=color, row=3, col=1)

    # MACD
    fig.add_trace(go.Scatter(
        x=df.index, y=df['MACD'],
        line=dict(color='blue', width=1), name="MACD",
        showlegend=False
    ), row=4, col=1)
    fig.add_trace(go.Scatter(
        x=df.index, y=df['MACD_Signal'],
        line=dict(color='orange', width=1), name="Signal",
        showlegend=False
    ), row=4, col=1)
    fig.add_trace(go.Bar(
        x=df.index, y=df['MACD_Hist'],
        marker_color=['green' if v >= 0 else 'red' for v in df['MACD_Hist']],
        name="Histogram",
        showlegend=False
    ), row=4, col=1)

    # Layout
    fig.update_layout(
        title=f"{ticker} — Technical Analysis",
        xaxis_rangeslider_visible=False,
        height=900,
        template="plotly_dark",
        showlegend=True
    )
    fig.write_html(CHARTS_PATH / f"{ticker}_chart.html")
    print(f"Saved {ticker}_chart.html to {CHARTS_PATH}")

# Create png of chart
def plot_matplotlib(df, ticker):
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(4, 1, figure=fig,
                  height_ratios=[0.5, 0.15, 0.15, 0.2],
                  hspace=0.03)

    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    ax4 = fig.add_subplot(gs[3], sharex=ax1)
    for idx, (date, row) in enumerate(df.iterrows()):
        color = 'green' if row['Close'] >= row['Open'] else 'red'

        # Wick
        ax1.plot([idx, idx], [row['Low'], row['High']],
                 color=color, linewidth=0.8)

        # Body
        ax1.add_patch(mpatches.Rectangle(
            (idx - 0.3, min(row['Open'], row['Close'])),
            0.6,
            abs(row['Close'] - row['Open']),
            facecolor=color, edgecolor=color
        ))
    # Bollinger Bands
    ax1.plot(range(len(df)), df['BB_Upper'], color='#4fc3f7', linewidth=0.8, alpha=0.6, label='BB Upper')
    ax1.plot(range(len(df)), df['BB_Middle'], color='#81d4fa', linewidth=0.8, alpha=0.8, label='BB Mid')
    ax1.plot(range(len(df)), df['BB_Lower'], color='#4fc3f7', linewidth=0.8, alpha=0.6, label='BB Lower')
    ax1.fill_between(range(len(df)), df['BB_Upper'], df['BB_Lower'], alpha=0.05, color='#4fc3f7')

    # SMAs
    ax1.plot(range(len(df)), df['SMA_20'], color='orange', linewidth=1, label='SMA 20')
    ax1.plot(range(len(df)), df['SMA_50'], color='purple', linewidth=1, label='SMA 50')
    ax1.plot(range(len(df)), df['SMA_200'], color='red', linewidth=1, label='SMA 200')
    # Volume
    colors = ['green' if c >= o else 'red' for c, o in zip(df['Close'], df['Open'])]
    ax2.bar(range(len(df)), df['Volume'], color=colors, width=0.8)
    ax2.set_ylabel('Volume', fontsize=8)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.0f}M'))
    # RSI
    ax3.plot(range(len(df)), df['RSI'], color='orange', linewidth=1, label='RSI')
    ax3.axhline(y=70, color='red', linestyle='--', linewidth=0.8)
    ax3.axhline(y=30, color='green', linestyle='--', linewidth=0.8)
    ax3.set_ylabel('RSI', fontsize=8)
    ax3.set_ylim(0, 100)
    # MACD
    ax4.plot(range(len(df)), df['MACD'], color='blue', linewidth=1, label='MACD')
    ax4.plot(range(len(df)), df['MACD_Signal'], color='orange', linewidth=1, label='Signal')
    colors_macd = ['green' if v >= 0 else 'red' for v in df['MACD_Hist']]
    ax4.bar(range(len(df)), df['MACD_Hist'], color=colors_macd, width=0.8, label='Histogram')
    ax4.axhline(y=0, color='white', linestyle='--', linewidth=0.5)
    ax4.set_ylabel('MACD', fontsize=8)
    # Styling
    fig.patch.set_facecolor('#1a1a1a')
    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_facecolor('#1a1a1a')
        ax.tick_params(colors='white', labelsize=7)
        ax.yaxis.label.set_color('white')
        for spine in ax.spines.values():
            spine.set_edgecolor('#444444')

    # X axis labels only on bottom panel
    ax1.tick_params(labelbottom=False)
    ax2.tick_params(labelbottom=False)
    ax3.tick_params(labelbottom=False)

    # Legend
    ax1.legend(loc='upper left', fontsize=7, facecolor='#1a1a1a', labelcolor='white')

    # Title
    ax1.set_title(f"{ticker} — Technical Analysis", color='white', fontsize=12, pad=10)

    tick_positions = list(range(0, len(df), len(df) // 6))
    tick_labels = [df.index[i].strftime('%b %Y') for i in tick_positions]
    ax4.set_xticks(tick_positions)
    ax4.set_xticklabels(tick_labels, color='white', fontsize=7, rotation=0)
    ax1.set_xlim(0, len(df))
    ax2.set_xlim(0, len(df))
    ax3.set_xlim(0, len(df))
    ax4.set_xlim(0, len(df))
    # Save
    plt.savefig(CHARTS_PATH / f"{ticker}_chart.png",
                dpi=150, bbox_inches='tight',
                facecolor='#1a1a1a')
    plt.close()
    print(f"Saved {ticker}_chart.png to {CHARTS_PATH}")

# Load data and generate both charts
def create_visualizations(ticker):
    df = pd.read_csv(PROCESSED_PATH / f"{ticker}_features.csv", index_col="Date", parse_dates=True)
    cutoff = df.index.max() - pd.DateOffset(days=LOOKBACK_DAYS)
    df = df[df.index >= cutoff]
    print(f"\n{'=' * 40}")
    print(f"  {ticker}")
    print(f"{'=' * 40}")
    plot_plotly(df, ticker)
    plot_matplotlib(df, ticker)

# Run
TICKERS = ["SPY", "QQQ", "IWM", "DIA", "GLD", "TLT", "XLE", "AAPL", "MSFT", "GOOGL", "NVDA", "META", "AMD", "JPM", "BAC", "GS", "V", "MA", "JNJ", "UNH", "PFE", "ABBV", "MRK", "XOM", "CVX", "COP", "SLB", "AMZN", "TSLA", "HD", "MCD", "CAT", "BA", "HON", "UPS"]

for ticker in TICKERS:
    create_visualizations(ticker)

