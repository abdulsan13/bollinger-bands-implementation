# Bollinger Bands Mean Reversion Backtester

Based on John Bollinger's *"Using Bollinger Bands"* (1992).

## What it does

Reads price data, computes three bands from the paper:

- **Middle** = 20-day simple moving average
- **Upper** = Middle + 2 × standard deviation
- **Lower** = Middle − 2 × standard deviation

When price dips below the lower band, it buys (mean reversion expects a bounce). When price spikes above the upper band, it sells. Otherwise it sits on its hands.

```
Price < lower band → BUY
Price > upper band → SELL
Everything else  → HOLD
```

## Files

| File | What it is |
|---|---|
| `generate_prices.py` | Builds 250 days of fake prices via random walk |
| `prices.csv` | The fake prices |
| `bollinger.py` | All the logic — bands, signals, backtest, main() |

## Functions

| Function | Job |
|---|---|
| `sma(data, window)` | Simple moving average |
| `std_dev(data)` | Standard deviation (population) |
| `bollinger_bands(prices, window, k)` | Returns upper, middle, lower |
| `generate_signals(prices, upper, lower)` | Returns 1 (buy), -1 (sell), or 0 (hold) |
| `backtest(prices, signals)` | Runs the simulation, returns performance numbers |

## Run it

```bash
python3 generate_prices.py
python3 bollinger.py
```

## Stuff I'd add later

- Real data from Yahoo Finance
- The %B indicator and Bandwidth
- Optimising the window and std multiplier
- Charts with matplotlib
- Compare against buy and hold