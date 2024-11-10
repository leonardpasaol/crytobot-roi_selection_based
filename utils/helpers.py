# utils/helpers.py

import pandas as pd

def calculate_atr(client, symbol, interval='1h', limit=14):
    """
    Calculates the Average True Range (ATR) for a given symbol.
    """
    klines = client.get_klines(
        symbol=symbol,
        interval=interval,
        limit=limit + 1  # Need an extra data point for True Range calculation
    )
    data = pd.DataFrame(klines, columns=[
        'Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close time', 'Quote asset volume', 'Number of trades',
        'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'
    ])
    data['High'] = data['High'].astype(float)
    data['Low'] = data['Low'].astype(float)
    data['Close'] = data['Close'].astype(float)

    # Calculate True Range
    data['Previous Close'] = data['Close'].shift(1)
    data['High-Low'] = data['High'] - data['Low']
    data['High-PC'] = abs(data['High'] - data['Previous Close'])
    data['Low-PC'] = abs(data['Low'] - data['Previous Close'])
    data['True Range'] = data[['High-Low', 'High-PC', 'Low-PC']].max(axis=1)

    # Calculate ATR
    atr = data['True Range'].rolling(window=limit).mean().iloc[-1]
    return atr
