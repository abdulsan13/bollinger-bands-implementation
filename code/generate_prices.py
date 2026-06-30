import math
import random

def random_t(df):
    x = random.gauss(0, 1)
    y = random.gammavariate(df / 2, 2)
    return x / math.sqrt(y / df)

def generate_prices(start_price=100, days=1000, seed=42):
    random.seed(seed)
    prices = []
    price = start_price
    drift = 0.08 / 252
    current_vol = 0.015

    for i in range(days):
        prices.append(price)

        if random.random() < 0.05:
            current_vol = random.expovariate(1 / 0.008)

        t_shock = random_t(4) * current_vol

        jump = 0
        if random.random() < 0.01:
            jump = random.choice([-0.07, 0.07])

        change = drift + t_shock + jump
        price = price * (1 + change)
    return prices

prices = generate_prices()

with open("prices.csv", "w") as f:
    f.write("date,price\n")
    for i, p in enumerate(prices):
        f.write(f"2024-{i+1:03d},{p:.2f}\n")

print(f"Generated {len(prices)} prices, range {min(prices):.2f} - {max(prices):.2f}")