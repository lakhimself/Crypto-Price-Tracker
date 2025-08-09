import requests

def format_value(val, is_percent=False):
    if val is None:
        return "N/A"
    return f"{val:.2f}%" if is_percent else f"{val:,.2f}"

def get_crypto_prices(cryptos, currency="usd"):
    ids = ",".join([coin.lower() for coin in cryptos])
    
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ids,
        "vs_currencies": currency.lower(),
        "include_market_cap": "true",
        "include_24hr_change": "true",
        "include_24hr_vol": "true"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"❌ Failed to retrieve data. Status code: {response.status_code}")
        return {}

    data = response.json()

    result = {}

    for coin in cryptos:
        coin_key = coin.lower()
        if coin_key not in data:
            print(f"❌ {coin} not found.")
            continue

        coin_data = data[coin_key]

        price = coin_data.get(currency.lower())
        market_cap = coin_data.get(f"{currency.lower()}_market_cap")
        change_24h = coin_data.get(f"{currency.lower()}_24h_change")
        volume_24h = coin_data.get(f"{currency.lower()}_24h_vol")

        print(f"\n📈 {coin.upper()} Price Tracker")
        print(f"💰 Current Price: {format_value(price)} {currency.upper()}")
        print(f"🏦 Market Cap: {format_value(market_cap)} {currency.upper()}")
        print(f"📊 24h Volume: {format_value(volume_24h)} {currency.upper()}")
        print(f"📉 24h Change: {format_value(change_24h, is_percent=True)}")

        if price is not None:
            result[coin] = {
                "price": price,
                "market_cap": market_cap,
                "volume_24h": volume_24h,
                "change_24h": change_24h
            }

    return result

def load_history(filename="crypto_history.txt"):
    history = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 5:
                    print(f"Warning: Malformed line in history: {line}")
                    continue
                coin, price_str, market_cap_str, volume_str, change_str = parts
                try:
                    history[coin] = {
                        "price": float(price_str),
                        "market_cap": float(market_cap_str),
                        "volume_24h": float(volume_str),
                        "change_24h": float(change_str)
                    }
                except ValueError:
                    print(f"Warning: Could not parse numbers for {coin} in history.")
    except FileNotFoundError:
        print("No previous history found.")
    return history

def save_history(history, filename="crypto_history.txt"):
    with open(filename, "w") as f:
        for coin, data in sorted(history.items()):
            line = f"{coin},{data['price']},{data['market_cap']},{data['volume_24h']},{data['change_24h']}\n"
            f.write(line)
    print(f"History saved to {filename}")

if __name__ == "__main__":
    history = load_history()
    if history:
        print("Loaded history:")
        for coin, data in history.items():
            print(f" - {coin}: Price={format_value(data['price'])}, Market Cap={format_value(data['market_cap'])}, Volume={format_value(data['volume_24h'])}, 24h Change={format_value(data['change_24h'], is_percent=True)}")

    currency = input("Enter currency (default is USD): ").strip().lower() or "usd"

    while True:
        user_input = input("\nEnter command or cryptocurrencies (e.g., bitcoin,ethereum), or 'help' for options:\n").strip().lower()

        if user_input == "exit":
            print("Goodbye!")
            break

        elif user_input == "help":
            print("\nCommands:")
            print(" - Enter cryptocurrencies separated by commas to get prices")
            print(" - history: Show all coins checked with last known prices")
            print(" - save: Save checked coins and prices to a file")
            print(" - help: Show this message")
            print(" - exit: Exit the app")

        elif user_input == "history":
            if history:
                print("Coins checked so far:")
                for coin, data in sorted(history.items()):
                    print(f" - {coin}: Price={format_value(data['price'])}, Market Cap={format_value(data['market_cap'])}, Volume={format_value(data['volume_24h'])}, 24h Change={format_value(data['change_24h'], is_percent=True)}")
            else:
                print("No coins checked yet.")

        elif user_input == "save":
            if history:
                save_history(history)
            else:
                print("No coins to save yet.")

        else:
            coins = [coin.strip() for coin in user_input.split(",") if coin.strip()]
            if not coins:
                print("Please enter valid coin names or a command.")
                continue

            prices = get_crypto_prices(coins, currency)
            for coin, data in prices.items():
                history[coin] = data
