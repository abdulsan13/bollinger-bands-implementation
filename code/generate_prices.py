import random

def generate_prices(start_price=100, days=250, seed=42):
    random.seed(seed)
    prices = []
    price = start_price

    for i in range(days):
        prices.append(price)
        change = random.gauss(0, 1) * 0.015
        price = price * (1 + change)
    return prices

prices = generate_prices()

with open("prices.csv", "w") as f:
    f.write("date,price\n")
    for i, p in enumerate(prices):
        f.write(f"2024-{i+1:03d},{p:.2f}\n")

print(f"Generated {len(prices)} prices, range {min(prices):.2f} - {max(prices):.2f}")