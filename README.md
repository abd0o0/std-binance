Overview
Std-Binance is a Python standard-library-inspired wrapper I built for the Binance API, providing a clean, modular interface for cryptocurrency trading operations. It standardizes common tasks like fetching market data, placing orders (spot/futures), managing wallets, and executing strategies, while handling authentication, rate limits, and error recovery. This project demonstrates my skills in API abstraction, async programming, and financial data processing—ideal for building scalable trading bots or analytics tools.
Disclaimer: Requires a Binance account and API keys. For educational use only; trading involves risks and is not financial advice. Respect Binance's terms and rate limits.
Features

Standardized API Calls: Simplified methods for spot/futures trading, e.g., client.get_ticker('BTCUSDT') or client.place_market_order('ETHUSDT', 'BUY', quantity=0.1).
Async Support: Non-blocking operations using asyncio for high-frequency trading.
Wallet & Account Management: Query balances, transfer funds, and track positions.
Market Data Tools: Real-time klines (candles), order books, and historical data fetching.
Error Handling: Built-in retries, rate limiting, and HMAC-SHA256 signature generation.
Extensible: Easy to add custom endpoints or integrate with strategies (e.g., from your RSIstrategy repo).

Tech Stack

Language: Python 3.10+
Key Libraries:

requests or aiohttp for HTTP requests.
hmac and hashlib (standard lib) for API signing.
pandas for data parsing and analysis.
python-binance (optional base for validation).


Minimal dependencies; emphasizes standard library where possible.

Getting Started
Prerequisites

Python 3.10 or higher.
Binance API keys (spot/futures; create at binance.com).
Git for cloning.

Installation

Clone the repository:
bashgit clone https://github.com/abd0o0/std-binance.git
cd std-binance

Create a virtual environment and install dependencies:
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Set up environment variables (create .env in the root):
textBINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
BINANCE_TESTNET=True  # Use testnet for safety


Usage

CLI Example (Fetch Ticker Data):
bashpython binance_cli.py ticker --symbol BTCUSDT
Outputs current price, volume, etc., as JSON.
Programmatic Use (in a Python script):
pythonfrom std_binance.client import BinanceClient
import asyncio

# Initialize client (loads from .env)
client = BinanceClient(testnet=True)

# Sync example: Get account balance
balance = client.get_account()
print(balance['balances'])  # List of assets with free/locked amounts

# Async example: Place a market order
async def place_order():
    order = await client.place_market_order(
        symbol='ETHUSDT',
        side='BUY',
        quantity=0.01
    )
    print(order)  # Order details: ID, status, fills

asyncio.run(place_order())

Advanced: Fetch Historical Klies:
pythonfrom std_binance.client import BinanceClient

client = BinanceClient()
klines = client.get_klines('BTCUSDT', interval='1h', limit=100)
df = client.parse_klines(klines)  # Returns Pandas DataFrame
print(df.head())  # OHLCV data


Run python binance_cli.py --help for all commands. Examples in /examples folder; full API docs in /docs.
