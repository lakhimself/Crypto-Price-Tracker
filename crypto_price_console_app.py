import requests

def get_crypto_price(crypto, currency="usd"):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": crypto.lower(),
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

    if crypto.lower() not in data:
        print("❌ Cryptocurrency not found.")
        return

    coin_data = data[crypto.lower()]
    currency = currency.lower()

    price = coin_data.get(currency)
    market_cap = coin_data.get(f"{currency}_market_cap")
    change_24h = coin_data.get(f"{currency}_24h_change")
    volume_24h = coin_data.get(f"{currency}_24h_vol")

    print(f"\n📈 {crypto.upper()} Price Tracker")
    print(f"💰 Current Price: {price:,.2f} {currency.upper()}")
    print(f"🏦 Market Cap: {market_cap:,.2f} {currency.upper()}")
    print(f"📊 24h Volume: {volume_24h:,.2f} {currency.upper()}")
    print(f"📉 24h Change: {change_24h:.2f}%")

if __name__ == "__main__":
    while True:
        crypto = input("Enter cryptocurrency name (or 'exit' to quit): ").strip()
        if crypto.lower() == "exit":
            print("👋 Goodbye!")
            break
        
        currency = input("Enter currency (default is USD): ").strip() or "usd"
        get_crypto_price(crypto, currency)
        print()  # blank line for readability
