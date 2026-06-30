import math

def backtest(prices, signals, initial_capital=1000, middle=None, cost_per_trade=0.001, capital_per_trade=1.0):
    capital = initial_capital
    position = 0
    buy_price = 0
    trades = []
    peak = initial_capital
    max_dd = 0
    portfolio_values = []

    for i in range(len(signals) - 1):

        if signals[i] == 1 and position == 0:
            allocated = capital * capital_per_trade
            buy_price = prices[i + 1]
            position_units = allocated / buy_price
            cash = capital - allocated
            position = 1

        elif signals[i] == -1 and position == 1:
            sell_price = prices[i + 1]
            position_value = position_units * sell_price
            trade_return = (sell_price - buy_price) / buy_price * 100
            trades.append({"buy": buy_price, "sell": sell_price, "return_pct": trade_return})
            capital = cash + position_value * (1 - cost_per_trade)

            # drawdown calculation
            if capital > peak:
                peak = capital
            dd = (capital - peak) / peak * 100
            if dd < max_dd:
                max_dd = dd
            position = 0

        elif position == 1 and middle is not None and middle[i] is not None:
            if prices[i] > middle[i]:
                sell_price = prices[i + 1]
                position_value = position_units * sell_price
                trade_return = (sell_price - buy_price) / buy_price * 100
                trades.append({"buy": buy_price, "sell": sell_price, "return_pct": trade_return})
                capital = cash + position_value * (1 - cost_per_trade)
                if capital > peak:
                    peak = capital
                dd = (capital - peak) / peak * 100
                if dd < max_dd:
                    max_dd = dd
                position = 0

        # portfolio tracking
        if position == 1:
            portfolio_values.append(cash + position_units * prices[i])
        else:
            portfolio_values.append(capital)

    final_capital = capital
    total_return_pct = (final_capital / initial_capital - 1) * 100

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
        "max_drawdown_pct": round(abs(max_dd), 2),
        "portfolio_values": portfolio_values
    }

def sharpe_ratio(portfolio_values, risk_free_rate=0.05):
    daily_returns = []

    for i in range(1, len(portfolio_values)):
        ret = (portfolio_values[i] - portfolio_values[i-1]) / portfolio_values[i-1]
        daily_returns.append(ret)

    if len(daily_returns) == 0:
        return 0.0

    mean_return = sum(daily_returns) / len(daily_returns)
    variance = sum((r - mean_return) ** 2 for r in daily_returns) / len(daily_returns)
    std_return = variance ** 0.5

    if std_return == 0:
        return 0.0

    daily_rf = risk_free_rate / 252
    daily_sharpe = (mean_return - daily_rf) / std_return
    annualised = daily_sharpe * math.sqrt(252)

    return round(annualised, 2)
