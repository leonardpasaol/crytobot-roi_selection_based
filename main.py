# main.py

from classes.SpotTrade import SpotTrade
from classes.BinanceAccount import BinanceAccount
from config.settings import SYMBOLS, TRADE_AMOUNT, PROFIT_TARGET, STOP_LOSS, TRADE_TIMEOUT
from utils.helpers import calculate_atr
import time

def main():
    account = BinanceAccount()
    active_trades = []

    while True:
        symbol_roi = {}

        # Step 1: Find the best 3 symbols based on possible ROI
        for symbol in SYMBOLS:
            try:
                # Calculate ATR as a measure of potential ROI
                atr = calculate_atr(account.client, symbol)
                klines = account.client.get_klines(
                    symbol=symbol,
                    interval='1h',
                    limit=1
                )
                last_close = float(klines[0][4])  # Closing price of the last kline

                # Potential ROI estimation
                potential_roi = (atr / last_close) * 100  # Percentage
                symbol_roi[symbol] = potential_roi
                print(f"Calculated potential ROI for {symbol}: {potential_roi:.2f}%")
            except Exception as e:
                print(f"Error calculating ROI for {symbol}: {e}")
                continue

        # Sort symbols based on potential ROI in descending order
        sorted_symbols = sorted(symbol_roi.items(), key=lambda x: x[1], reverse=True)
        selected_symbols = [symbol for symbol, roi in sorted_symbols[:3]]

        print(f"Selected top 3 symbols based on potential ROI: {selected_symbols}")

        for symbol in selected_symbols:
            # Check if we already have an active trade for this symbol
            if any(trade.symbol == symbol for trade in active_trades):
                continue  # Skip if trade is already active

            trade = SpotTrade(
                symbol=symbol,
                amount=TRADE_AMOUNT,
                profit_target=PROFIT_TARGET,
                stop_loss=STOP_LOSS,
                timeout=TRADE_TIMEOUT
            )

            if trade.find_entry_signal():
                trade.enter_trade()
                active_trades.append(trade)
            else:
                print(f"No entry signal for {symbol}. Skipping trade.")

        # Monitor active trades
        for trade in active_trades[:]:
            if trade.entry_price is not None:
                trade.monitor_trade()
                active_trades.remove(trade)  # Remove trade after it's done

        # Sleep before repeating the process
        time.sleep(60)  # Wait for 1 minute before checking again

if __name__ == "__main__":
    main()
