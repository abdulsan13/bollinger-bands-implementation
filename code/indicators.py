import math

def sma(data, window):
    result = []
    for i in range(len(data)):
        if i < window - 1:
            result.append(None)
        else:
            result.append(sum(data[i - window + 1 : i + 1]) / window)
    return result

def ema(data, alpha):
    result = []
    for i in range(len(data)):
        if i == 0:
            result.append(data[i])
        else:
            result.append(alpha * data[i] + (1 - alpha) * result[i-1])
    return result

def std_dev(data):
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std = math.sqrt(variance)
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

def combined_signals(*signal_lists, threshold=0.33):
    num_lists = len(signal_lists)
    combined = []
    for i in range(len(signal_lists[0])):
        avg = sum([lst[i] for lst in signal_lists]) / num_lists
        if avg > threshold:
            combined.append(1)
        elif avg < -threshold:
            combined.append(-1)
        else:
            combined.append(0)
    return combined

def sma_crossover_signals(prices, short_window=20, long_window=50):
    short_sma = sma(prices, short_window)
    long_sma = sma(prices, long_window)
    signals = []
    for i in range(len(prices)):
        if short_sma[i] is None or long_sma[i] is None:
            signals.append(0)
        elif i > 0 and short_sma[i-1] is not None and long_sma[i-1] is not None and short_sma[i-1] <= long_sma[i-1] and short_sma[i] > long_sma[i]:
            signals.append(1)
        elif i > 0 and short_sma[i-1] is not None and long_sma[i-1] is not None and short_sma[i-1] >= long_sma[i-1] and short_sma[i] < long_sma[i]:
            signals.append(-1)
        else:
            signals.append(0)
    return signals

def ema_crossover_signals(prices, short_window=20, long_window=50):
    short_alpha = 2 / (short_window + 1)
    long_alpha  = 2 / (long_window + 1)
    short_ema = ema(prices, short_alpha)
    long_ema  = ema(prices, long_alpha)
    signals = []
    for i in range(len(prices)):
        if short_ema[i] is None or long_ema[i] is None:
            signals.append(0)
        elif i > 0 and short_ema[i-1] is not None and long_ema[i-1] is not None and short_ema[i-1] <= long_ema[i-1] and short_ema[i] > long_ema[i]:
            signals.append(1)
        elif i > 0 and short_ema[i-1] is not None and long_ema[i-1] is not None and short_ema[i-1] >= long_ema[i-1] and short_ema[i] < long_ema[i]:
            signals.append(-1)
        else:
            signals.append(0)
    return signals
