def sma(data, window):
    result = []

    for i in range(len(data)):
        if i < window - 1:
            result.append(None)
        else:
            result.append(sum(data[i - window + 1 : i + 1]) / window)
    return result

def std_dev(data):
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std = variance ** 0.5
    return std

def bollinger_bands(prices, window, k=2):
    middle = sma(prices, window)
    upper = []
    lower = []

    for i in range(len(middle)):
        if middle[i] is None:
            upper.append(None)
            lower.append(None)
        else:
            price_window = prices[i - window + 1 : i + 1]
            std = std_dev(price_window)
            upper.append(middle[i] + k * std)
            lower.append(middle[i] - k * std)
    
    return middle, upper, lower

def generate_signals(prices, upper, lower):
    signals = []
    
    for i in range(len(prices)):
        if upper[i] is None:
            signals.append(0)
        elif prices[i] < lower[i]:
            signals.append(1)
        elif prices[i] > upper[i]:
            signals.append(-1)
        else:
            signals.append(0)
    
    return signals

def backtest(prices, signals, initial_capital=1000):
    capital = initial_capital
    position = 0
    buy_price = 0
    trades = []
    peak = initial_capital
    max_dd = 0

    for i in range(len(signals)):
        if signals[i] == 1 and position == 0:
            buy_price = prices[i]
            position = 1
        elif signals[i] == -1 and position == 1:
            sell_price = prices[i]
            trade_return = (sell_price - buy_price) / buy_price * 100
            trades.append({"buy": buy_price, "sell": sell_price, "return_pct": trade_return})
            capital = capital * (1 + trade_return / 100)
            if capital > peak:
                peak = capital
            dd = (capital - peak) / peak * 100
            if dd < max_dd:
                max_dd = dd
            position = 0
            
    final_capital = capital
    total_return_pct = (final_capital/initial_capital - 1) * 100

    total_trades = len(trades)
    if total_trades > 0:
        wins = sum(1 for t in trades if t["return_pct"] > 0)
        win_rate = wins / total_trades * 100
    else:
        win_rate = 0

    return {
    "total_return_pct": round(total_return_pct, 2),
    "num_trades": total_trades,
    "win_rate": round(win_rate, 2),
    "final_value": round(final_capital, 2),
    "max_drawdown_pct": round(max_dd, 2)
    }

def main():
    prices = []
    with open('prices.csv') as f:
        next(f)
        for line in f:
            parts = line.strip().split(',')
            prices.append(float(parts[1]))

    middle, upper, lower = bollinger_bands(prices, 20)
    signals = generate_signals(prices, upper, lower)
    results = backtest(prices, signals)

    print("=== Bollinger Bands Backtest Results ===")
    for key, value in results.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()