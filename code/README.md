# Bollinger Bands + Moving Average Crossover — Quant Feeder Project

A multi-strategy backtesting framework built from scratch in pure Python. Reads or generates price data, computes Bollinger Bands and SMA/EMA crossover signals, runs all 8 strategy combinations, and compares results with proper quant methodology.

Based on John Bollinger's *"Using Bollinger Bands"* (1992).

---

## Project structure

```
code/
├── indicators.py           # SMA, EMA, std_dev, Bollinger Bands, all signal generators
├── engine.py               # backtest() and sharpe_ratio()
├── main.py                 # main() + multi-seed comparison
├── generate_prices.py      # synthetic price generator (t-dist, vol regimes, jumps)
├── prices.csv              # generated 1000-row dataset
└── README.md               # project conclusion
```

---

## The 8 strategies

| # | Strategy | Type |
|---|---|---|
| 1 | SMA crossover (20 × 50) | Trend-following |
| 2 | EMA crossover (20 × 50) | Trend-following |
| 3 | Bollinger Bands (20, 2σ) | Mean reversion |
| 4 | BB + SMA | Confluence (signal averaging) |
| 5 | BB + EMA | Confluence (signal averaging) |
| 6 | SMA + EMA | Confluence (signal averaging) |
| 7 | All Three | Confluence (signal averaging) |
| 8 | Buy & Hold | Baseline benchmark |

Combined strategies use **signal averaging** — the mean of all signals at each bar, with a threshold of 0.33. Not binary "all must agree."

---

## Methodology (what makes this different from a beginner project)

| Fix | Why it matters |
|---|---|
| **Look-ahead bias** | Signal fires at bar `i`, execution at `prices[i+1]`. You can't trade on today's close at today's close. |
| **Transaction costs** | 0.1% per trade. Strategies that look good without costs often fail with them. |
| **Position sizing** | `capital_per_trade` parameter (default all-in). Tracks cash + shares separately. |
| **Middle-band exit** | BB exits when price crosses back to the SMA(20), not just on opposite signals. |
| **Train/test split** | 70/30 split. Only test results matter. Prevents overfitting. |
| **Multi-seed average** | Runs on 10 different random seeds. Averages across all to reduce luck. |
| **Sharpe ratio** | Risk-adjusted return. A strategy with 10% return and 20% volatility is worse than 5% with 5% vol. |
| **Drawdown tracking** | Negative max drawdown tracked on every exit, reported as positive convention. |
| **Population std dev** | Correct for Bollinger Bands (divides by n, not n-1). |

---

## Results (synthetic data, 10 seeds averaged, test period only)

```
Strategy             Avg Ret%
SMA Crossover        -6.29
EMA Crossover        -5.30
Bollinger Bands      1.81
BB + SMA             4.22
BB + EMA             1.28
SMA + EMA            -7.24
All Three            1.53
```

### Key findings

- **BB + SMA** is the best combination on synthetic data — it fuses a mean reversion signal with a trend signal, filtering false signals from either direction
- **Pure trend strategies (SMA/EMA crossover)** lose money on random walk data, as expected (random walks have no trend to capture)
- **All three combined** does worse than BB+SMA — adding more signals adds noise, not edge
- **Signal averaging works** — the combined strategies outperform their individual components in most seeds
- **No strategy beats buy & hold** on the synthetic test period on this seed (buy & hold returned ~42.95% across seeds), which is also expected — random walks drift upward, and active trading adds friction

---

## What this project taught

1. **Papers → code**: Reading original sources (Bollinger, 1992) and implementing from scratch builds real understanding
2. **Bugs you find yourself stick**: Identifying look-ahead bias, padding issues, and drawdown gaps without being told
3. **More complexity ≠ better returns**: The "All Three" strategy underperforms "BB + SMA" — extra signals dilute conviction
4. **Train/test split is non-negotiable**: Strategies that look amazing in-sample (SMA+EMA at 408%) fail out-of-sample
5. **File separation scales naturally**: Pure functions in `indicators.py`, evaluation in `engine.py`, orchestration in `main.py`

---

## Phase 2 — Coming next

| # | Item | Status |
|---|---|---|
| 1 | Live data (yfinance — SPY, real prices) | Planned |
| 2 | Multi-instrument (QQQ, AAPL, MSFT, GOOG) | Planned |
| 3 | Walk-forward validation (rolling windows) | Planned |
| 4 | Visualisation (matplotlib charts) | Planned |
| 5 | ML signal (logistic regression on BB features) | Planned |

### Run it

```bash
python3 generate_prices.py     # regenerate prices.csv
python3 main.py                 # run all 8 strategies
```