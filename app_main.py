import requests

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
        return

    data = response.json()

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
        print(f"💰 Current Price: {price:,.2f} {currency.upper()}")
        print(f"🏦 Market Cap: {market_cap:,.2f} {currency.upper()}")
        print(f"📊 24h Volume: {volume_24h:,.2f} {currency.upper()}")
        print(f"📉 24h Change: {change_24h:.2f}%")

if __name__ == "__main__":
    history = []
    # Load history if exists
    try:
        with open("crypto_history.txt", "r") as f:
            history = [line.strip() for line in f.readlines() if line.strip()]
        if history:
            print(f"Loaded history from file: {', '.join(history)}")
    except FileNotFoundError:
        print("No previous history found.")

    currency = input("Enter currency (default is USD): ").strip().lower() or "usd"

    while True:
        user_input = input("\nEnter command or cryptocurrencies (e.g., bitcoin,ethereum), or 'help' for options:\n").strip().lower()

        if user_input == "exit":
            print("Goodbye!")
            break

        elif user_input == "help":
            print("\nCommands:")
            print(" - Enter cryptocurrencies separated by commas to get prices")
            print(" - history: Show all coins checked")
            print(" - save: Save checked coins to a file")
            print(" - help: Show this message")
            print(" - exit: Exit the app")

        elif user_input == "history":
            if history:
                print("Coins checked so far:", ", ".join(sorted(set(history))))
            else:
                print("No coins checked yet.")

        elif user_input == "save":
            if history:
                with open("crypto_history.txt", "w") as f:
                    for coin in sorted(set(history)):
                        f.write(coin + "\n")
                print("History saved to crypto_history.txt")
            else:
                print("No coins to save yet.")

        else:
            coins = [coin.strip() for coin in user_input.split(",") if coin.strip()]
            if not coins:
                print("Please enter valid coin names or a command.")
                continue

            get_crypto_prices(coins, currency)
            for coin in coins:
                if coin not in history:
                    history.append(coin)
