# config/settings.py

# SANDBOX, set Testnet=True in classes/BinanceAccount.py
API_KEY = 'BxcrMjigLm5GPLzwIZ4iEqYnixT10WTLF9Aw6ywvfeRNw9yazgEYqmptMzWcYNjs'
API_SECRET = '8TULX3xpc1yfQDa9GGwfSVnKJnC3Y12V27FIIH40cC1Cx9898Mm2G79BjFvJEhLZ'

#LIVE
# API_KEY = 'o5uoFFQaV1zxZ7OoiarqAoGpvPmhJ1avi8TuF81erkfeQEUW9CCb2F7szn2sQpQP'
# API_SECRET = 'wPFHeaofCqA9MCMwXO3IJQoXxOz1LubQCnQc2CRdeoFEhlAtYtazvWHOezip13my'

# List of symbols to monitor (you can add or remove symbols as needed)
SYMBOLS = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT',
    'SOLUSDT', 'DOTUSDT', 'LTCUSDT', 'SHIBUSDT', 'AVAXUSDT',
    'UNIUSDT', 'LINKUSDT', 'ATOMUSDT', 'TRXUSDT', 'ETCUSDT', 'XLMUSDT',
    'NEARUSDT', 'ALGOUSDT', 'FTMUSDT', 'FILUSDT', 'APEUSDT', 'SANDUSDT',
    'EGLDUSDT', 'HBARUSDT', 'XTZUSDT', 'THETAUSDT', 'AAVEUSDT', 'AXSUSDT',
    'EOSUSDT', 'MANAUSDT', 'FLOWUSDT', 'GRTUSDT', 'CHZUSDT',
    'CAKEUSDT', 'XECUSDT', 'NEOUSDT', 'RUNEUSDT', 'ARUSDT',
    'KSMUSDT', 'ZECUSDT', 'ENJUSDT', 'LRCUSDT', '1INCHUSDT', 'BATUSDT',
    'YFIUSDT', 'DYDXUSDT'
]

# Trading parameters
TRADE_AMOUNT = 100  # Amount in USDT to trade per symbol
PROFIT_TARGET = 0.02  # 2% profit target
STOP_LOSS = 0.04      # 4% stop loss
TRADE_TIMEOUT = 30    # 30 minutes timeout
