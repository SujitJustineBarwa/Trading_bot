import matplotlib.pyplot as plt

class LivePlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        
    def update_plot(self, price_history, sma=None, lower_band=None, upper_band=None, buy_price=None, sell_price=None):
        self.ax.clear()
        
        self.ax.plot(price_history, label="Actual Price", color="blue")
        
        if sma is not None:
            self.ax.plot([sma] * len(price_history), label="SMA", color="orange")
        
        if lower_band is not None and upper_band is not None:
            self.ax.plot([lower_band] * len(price_history), label="Lower Band", color="green")
            self.ax.plot([upper_band] * len(price_history), label="Upper Band", color="red")
        
        if buy_price is not None:
            self.ax.scatter(len(price_history) - 1, buy_price, color="green", label="Buy Price")
        
        if sell_price is not None:
            self.ax.scatter(len(price_history) - 1, sell_price, color="red", label="Sell Price")
        
        self.ax.legend()
        plt.pause(0.01)
