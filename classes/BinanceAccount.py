# classes/BinanceAccount.py

from binance.client import Client
from config.settings import API_KEY, API_SECRET
import math

class BinanceAccount:
    def __init__(self):
        # Use testnet=True for Binance Testnet (for testing purposes)
        self.client = Client(API_KEY, API_SECRET, testnet=True)

    def get_balance(self, asset):
        balance = self.client.get_asset_balance(asset=asset)
        return float(balance['free']) if balance else 0.0

    def place_order(self, symbol, side, quantity):
        # Adjust quantity precision based on symbol's step size
        quantity = self.adjust_quantity(symbol, quantity)

        order = self.client.create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        return order

    def adjust_quantity(self, symbol, quantity):
        """
        Adjusts the quantity to match the symbol's step size and lot size.
        """
        try:
            info = self.client.get_symbol_info(symbol)
            step_size = float(next(
                filter(
                    lambda f: f['filterType'] == 'LOT_SIZE',
                    info['filters']
                )
            )['stepSize'])
            precision = int(round(-math.log(step_size, 10), 0))
            adjusted_quantity = round(quantity - (quantity % step_size), precision)
            return adjusted_quantity
        except Exception as e:
            print(f"Error adjusting quantity for {symbol}: {e}")
            return quantity

    def get_open_orders(self, symbol):
        return self.client.get_open_orders(symbol=symbol)

    def cancel_order(self, symbol, orderId):
        return self.client.cancel_order(symbol=symbol, orderId=orderId)
