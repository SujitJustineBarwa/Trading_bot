import numpy as np
from collections import deque

class BollingerStrategy:
    def __init__(self, period=20):
        self.period = period
        self.price_history = deque(maxlen=period)

    def update_price(self, price):
        self.price_history.append(price)

    def calculate_bands(self):
        if len(self.price_history) < self.period:
            return None, None, None
        
        sma = np.mean(self.price_history)
        std_dev = np.std(self.price_history)
        lower_band = sma - 2 * std_dev
        upper_band = sma + 2 * std_dev
        
        return sma, lower_band, upper_band