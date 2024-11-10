# classes/SpotTrade.py

from classes.BinanceAccount import BinanceAccount
from datetime import datetime, timedelta
import time

class SpotTrade:
    def __init__(self, symbol, amount, profit_target, stop_loss, timeout):
        self.symbol = symbol
        self.amount = amount
        self.profit_target = profit_target
        self.stop_loss = stop_loss
        self.timeout = timeout
        self.account = BinanceAccount()
        self.entry_price = None
        self.entry_time = None

    def get_reference_price(self):
        """
        Fetches the previous closing price of the symbol.
        """
        klines = self.account.client.get_klines(
            symbol=self.symbol,
            interval='15m',
            limit=2  # Get the last two klines to ensure previous close
        )
        if klines:
            previous_close = float(klines[-2][4])  # Closing price of the previous candle
            return previous_close
        else:
            print(f"Could not fetch klines for {self.symbol}.")
            return None

    def find_entry_signal(self):
        """
        Checks if the current price is 1% lower than the reference price.
        """
        reference_price = self.get_reference_price()
        if reference_price is None:
            return False  # Cannot proceed without reference price

        current_price = float(self.account.client.get_symbol_ticker(symbol=self.symbol)['price'])

        # Calculate percentage drop
        price_drop_percentage = ((reference_price - current_price) / reference_price) * 100

        if price_drop_percentage >= 1:
            print(f"Entry signal detected for {self.symbol}: Price dropped by {price_drop_percentage:.2f}%")
            return True
        else:
            print(f"No entry signal for {self.symbol}: Price dropped by {price_drop_percentage:.2f}%")
            return False

    def enter_trade(self):
        """
        Places a market buy order for the specified amount.
        """
        # Calculate the quantity to buy based on amount and current price
        current_price = float(self.account.client.get_symbol_ticker(symbol=self.symbol)['price'])
        quantity = self.amount / current_price

        try:
            order = self.account.place_order(
                symbol=self.symbol,
                side='BUY',
                quantity=quantity
            )
            self.entry_price = float(order['fills'][0]['price'])
            self.entry_time = datetime.now()
            print(f"Entered trade for {self.symbol} at {self.entry_price}")
        except Exception as e:
            print(f"Error entering trade for {self.symbol}: {e}")

    def monitor_trade(self):
        """
        Monitors the trade for profit target, stop loss, or timeout.
        """
        print(f"Monitoring trade for {self.symbol}...")
        while True:
            try:
                current_price = float(self.account.client.get_symbol_ticker(symbol=self.symbol)['price'])
                roi = (current_price - self.entry_price) / self.entry_price

                if roi >= self.profit_target:
                    self.close_trade("Profit target reached")
                    break

                elif roi <= -self.stop_loss:
                    self.close_trade("Stop loss triggered")
                    break

                elif datetime.now() - self.entry_time > timedelta(minutes=self.timeout):
                    self.close_trade("Timeout reached")
                    break

                time.sleep(5)  # Wait before checking again
            except Exception as e:
                print(f"Error monitoring trade for {self.symbol}: {e}")
                time.sleep(5)

    def close_trade(self, reason):
        """
        Closes the trade by placing a market sell order.
        """
        try:
            # Get the quantity to sell
            asset = self.symbol.replace('USDT', '')
            balance = self.account.get_balance(asset)
            if balance > 0:
                order = self.account.place_order(
                    symbol=self.symbol,
                    side='SELL',
                    quantity=balance
                )
                exit_price = float(order['fills'][0]['price'])
                print(f"{reason} for {self.symbol}. Exited trade at {exit_price}")
            else:
                print(f"No balance to sell for {self.symbol}.")
        except Exception as e:
            print(f"Error closing trade for {self.symbol}: {e}")
