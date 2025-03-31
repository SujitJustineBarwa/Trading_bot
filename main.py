from src.api_utils import get_account_balance, place_order, get_pepe_usdt_price
from src.bollinger_strategy import BollingerStrategy
from src.plot_utils import LivePlot

def main():
    strategy = BollingerStrategy(period=20)
    plotter = LivePlot()
    
    usdt_balance = get_account_balance()
    pepe_balance = 0.0
    in_position = False
    
    while True:
        price = get_pepe_usdt_price()
        
        strategy.update_price(price)
        
        sma, lower_band, upper_band = strategy.calculate_bands()
        
        if sma and lower_band and upper_band:
            if not in_position and price < lower_band and usdt_balance > 0:
                quantity_to_buy = usdt_balance / price
                place_order("PEPEUSDT", "BUY", quantity_to_buy)
                pepe_balance += quantity_to_buy
                usdt_balance -= usdt_balance
                in_position = True
            
            elif in_position and price > sma:
                usdt_balance += pepe_balance * price
                place_order("PEPEUSDT", "SELL", pepe_balance)
                pepe_balance -= pepe_balance
                in_position = False
        
            plotter.update_plot(strategy.price_history, sma=sma, lower_band=lower_band,
                                upper_band=upper_band)

if __name__ == "__main__":
    main()
