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
    coins = input("Enter cryptocurrencies separated by commas (e.g., bitcoin,ethereum,dogecoin): ")
    currency = input("Enter currency (default is USD): ") or "usd"
    
    crypto_list = [coin.strip() for coin in coins.split(",")]
    get_crypto_prices(crypto_list, currency)
