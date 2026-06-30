from indicators import bollinger_bands, generate_signals, combined_signals, sma_crossover_signals, ema_crossover_signals
from engine import backtest, sharpe_ratio
from generate_prices import generate_prices

def main():
    prices = generate_prices()

    middle, upper, lower = bollinger_bands(prices, 20)
    bb_sigs = generate_signals(prices, upper, lower)
    sma_sigs = sma_crossover_signals(prices)
    ema_sigs = ema_crossover_signals(prices)

    strategies = [
        {"name": "SMA Crossover", "signals": sma_sigs, "middle": None},
        {"name": "EMA Crossover", "signals": ema_sigs, "middle": None},
        {"name": "Bollinger Bands", "signals": bb_sigs, "middle": middle},
        {"name": "BB + SMA", "signals": combined_signals(bb_sigs, sma_sigs), "middle": middle},
        {"name": "BB + EMA", "signals": combined_signals(bb_sigs, ema_sigs), "middle": middle},
        {"name": "SMA + EMA", "signals": combined_signals(sma_sigs, ema_sigs), "middle": None},
        {"name": "All Three", "signals": combined_signals(bb_sigs, sma_sigs, ema_sigs), "middle": middle},
    ]

    test_prices = prices[700:]

    print(f"{'Strategy':<20} {'Return%':<10} {'Trades':<8} {'Sharpe':<8} {'WinRate':<8}")

    for strat in strategies:
        test_sigs = strat["signals"][700:]
        test_res = backtest(test_prices, test_sigs, middle=strat["middle"][700:] if strat["middle"] else None)

        test_sharpe = sharpe_ratio(test_res["portfolio_values"])

        print(f"{strat['name']:<20} {test_res['total_return_pct']:<10.2f} {test_res['num_trades']:<8} {test_sharpe:<8.2f} {test_res['win_rate']:<8.2f}")

    bh_test = (test_prices[-1] / test_prices[0] - 1) * 100
    print(f"{'Buy & Hold':<20} {bh_test:<10.2f}")

if __name__ == "__main__":
    main()

    seeds = [1, 7, 13, 21, 99, 123, 456, 789, 999, 1111]
    results_by_seed = {seed: {} for seed in seeds}

    for seed in seeds:
        prices = generate_prices(seed=seed)
        middle, upper, lower = bollinger_bands(prices, 20)
        bb_sigs = generate_signals(prices, upper, lower)
        sma_sigs = sma_crossover_signals(prices)
        ema_sigs = ema_crossover_signals(prices)

        strategies = [
            ("SMA Crossover", sma_sigs, None),
            ("EMA Crossover", ema_sigs, None),
            ("Bollinger Bands", bb_sigs, middle),
            ("BB + SMA", combined_signals(bb_sigs, sma_sigs), middle),
            ("BB + EMA", combined_signals(bb_sigs, ema_sigs), middle),
            ("SMA + EMA", combined_signals(sma_sigs, ema_sigs), None),
            ("All Three", combined_signals(bb_sigs, sma_sigs, ema_sigs), middle),
        ]

        test_prices = prices[700:]
        for name, sigs, mid in strategies:
            res = backtest(test_prices, sigs[700:], middle=mid[700:] if mid else None)
            results_by_seed[seed][name] = res["total_return_pct"]

    print("\n=== Multi-Seed Average (Test Period) ===")
    print(f"{'Strategy':<20} {'Avg Ret%':<10}")
    names = [s[0] for s in strategies]
    for name in names:
        returns = [results_by_seed[s][name] for s in seeds]
        avg = sum(returns) / len(returns)
        print(f"{name:<20} {avg:<10.2f}")
