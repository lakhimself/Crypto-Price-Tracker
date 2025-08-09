
## 📊 Crypto Price Tracker – CLI & GUI App

A versatile cryptocurrency price monitoring tool that fetches real-time data from the [CoinGecko API](https://www.coingecko.com/en/api), available in two flavors:
- 🖥️ Console version for terminal enthusiasts
- 🖼️ GUI version with Tkinter for visual users

Track prices, market caps, trading volumes, and price changes with ease!

## 🌟 Features

- 📈 Real-time cryptocurrency price tracking
- 💰 Multiple currency support (USD, EUR, GBP, etc.)
- 🏦 Comprehensive data including:
  - Current price
  - Market capitalization
  - 24h trading volume
  - 24h price change
- 📚 History tracking (save/load previous data)
- 🎨 GUI version features:
  - Color-coded output
  - Interactive interface
  - Historical data saving
- ⚡ Console version offers:
  - Quick checks
  - Command-based interaction
  - Persistent history

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/lakhimself/crypto-price-tracker.git
cd crypto-price-tracker
```

### 2. Install Required Dependencies
```bash
pip install requests tkinter
```

## 🚀 Usage

### 🖼️ GUI Version (Recommended)
```bash
python Tkinter.py
```
Features:
- Intuitive interface
- Color-coded data presentation
- Automatic history saving

### 🖥️ Console Versions

**Interactive Console App:**
```bash
python app_main.py
```
Commands:
- Enter crypto names to check prices
- `history` - View checked coins
- `save` - Save current data
- `help` - Show commands
- `exit` - Quit

**Quick Check Version:**
```bash
python crypto_prices_console_app.py
```
For one-time price checks

## 📂 Project Structure
```
crypto-tracker/
│
├── Tkinter.py                    # GUI application
├── app_main.py                   # Full-featured console app
├── crypto_prices_console_app.py  # Simple console version
├── crypto_history.txt            # Console app data storage
└── history.txt                   # GUI app data storage
```

## 📊 Data Sample

**GUI Output:**
```
📅 2023-11-15 14:30:45

📈 BITCOIN Price Tracker
💰 Current Price: 36,542.20 USD
🏦 Market Cap: 713,245,678,901 USD
📊 24h Volume: 24,567,890,123 USD
📉 24h Change: +2.34%
```

**Console Output:**
```
📈 ETHEREUM Price Tracker
💰 Current Price: 1,985.42 USD
🏦 Market Cap: 238,456,789,012 USD
📊 24h Volume: 12,345,678,901 USD
📉 24h Change: -1.23%
```

## 🛠️ Dependencies
- Python 3.x
- `requests` library
- `tkinter` (for GUI version)

## 💡 Tips
- Start with popular coins (bitcoin, ethereum)
- Try different currencies (eur, gbp, jpy)
- Use TAB for autocomplete in console version
- Colors in GUI indicate:
  - Green: Price
  - Gold: Market Cap
  - Teal: Volume
  - Orange: Change

## 🆘 Troubleshooting

| Issue                      | Solution                          |
|----------------------------|-----------------------------------|
| API not responding         | Check internet connection         |
| Coin not found             | Verify correct spelling           |
| History file missing       | App will create it automatically  |
| GUI display issues         | Ensure tkinter is installed       |
| ModuleNotFoundError        | Run `pip install requests tkinter`|
