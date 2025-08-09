import tkinter as tk
from tkinter import ttk
import requests
import datetime

def format_value(value, decimals=2):
    if value is None:
        return "N/A"
    return f"{value:,.{decimals}f}"

def get_crypto_prices(coins, currency="usd"):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join([coin.lower() for coin in coins]),
        "vs_currencies": currency.lower(),
        "include_market_cap": "true",
        "include_24hr_change": "true",
        "include_24hr_vol": "true"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Error fetching data: {e}"

    data = response.json()
    result = {}

    for coin in coins:
        coin_key = coin.lower()
        if coin_key not in data:
            result[coin] = None
            continue
        coin_data = data[coin_key]
        result[coin] = {
            "price": coin_data.get(currency.lower()),
            "market_cap": coin_data.get(f"{currency.lower()}_market_cap"),
            "volume_24h": coin_data.get(f"{currency.lower()}_24h_vol"),
            "change_24h": coin_data.get(f"{currency.lower()}_24h_change")
        }

    return result

def save_history(text):
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(text)
        f.write("\n" + "-"*50 + "\n\n")

def show_prices():
    coins_input = coins_entry.get()
    currency = currency_entry.get() or "usd"
    coins = [coin.strip() for coin in coins_input.split(",") if coin.strip()]

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)

    if not coins:
        output_text.insert(tk.END, "⚠️ Please enter at least one cryptocurrency.\n", "error")
        output_text.config(state=tk.DISABLED)
        return

    prices = get_crypto_prices(coins, currency)

    if isinstance(prices, str):  # error message returned
        output_text.insert(tk.END, prices + "\n", "error")
        output_text.config(state=tk.DISABLED)
        return

    output_str = f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    for coin in coins:
        data = prices.get(coin)
        if data is None:
            output_text.insert(tk.END, f"❌ {coin} not found.\n\n", "error")
            continue

        # Insert with tags for color
        output_text.insert(tk.END, f"📈 {coin.upper()} Price Tracker\n", "heading")
        output_text.insert(tk.END, f"💰 Current Price: {format_value(data['price'])} {currency.upper()}\n", "price")
        output_text.insert(tk.END, f"🏦 Market Cap: {format_value(data['market_cap'])} {currency.upper()}\n", "market_cap")
        output_text.insert(tk.END, f"📊 24h Volume: {format_value(data['volume_24h'])} {currency.upper()}\n", "volume")
        output_text.insert(tk.END, f"📉 24h Change: {format_value(data['change_24h'])}%\n\n", "change")

    output_text.config(state=tk.DISABLED)
    save_history(output_text.get("1.0", tk.END))

# --- Tkinter GUI setup ---

root = tk.Tk()
root.title("Crypto Price Tracker")
root.geometry("600x450")
root.resizable(False, False)

# Color scheme
bg_color = "#1e1e2f"
fg_color = "#dcdcdc"
input_bg = "#2c2c44"
button_bg = "#4a90e2"
button_fg = "#ffffff"
error_color = "#ff4c4c"
price_color = "#7fff00"
market_cap_color = "#ffd700"
volume_color = "#00ced1"
change_color = "#ff8c00"
heading_color = "#00bfff"

root.configure(bg=bg_color)

style = ttk.Style()
style.theme_use('clam')

style.configure("TFrame", background=bg_color)
style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
style.configure("TEntry", fieldbackground=input_bg, foreground=fg_color, font=("Segoe UI", 10))
style.configure("TButton", background=button_bg, foreground=button_fg, font=("Segoe UI", 11, "bold"))

# Main frame
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Input frame
input_frame = ttk.Frame(main_frame)
input_frame.pack(fill=tk.X, pady=5)

ttk.Label(input_frame, text="Cryptocurrency names (comma separated):").pack(anchor=tk.W)
coins_entry = ttk.Entry(input_frame, width=50)
coins_entry.pack(fill=tk.X, pady=2)
coins_entry.insert(0, "bitcoin, ethereum, dogecoin")

ttk.Label(input_frame, text="Currency (default USD):").pack(anchor=tk.W, pady=(10, 2))
currency_entry = ttk.Entry(input_frame, width=10)
currency_entry.pack(fill=tk.X, pady=2)
currency_entry.insert(0, "usd")

# Button frame
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10)

get_button = ttk.Button(button_frame, text="Get Prices", command=show_prices)
get_button.pack()

# Button hover effect
def on_enter(e):
    get_button.config(background="#6aa0f8")
def on_leave(e):
    get_button.config(background=button_bg)

get_button.bind("<Enter>", on_enter)
get_button.bind("<Leave>", on_leave)

# Output frame with scrollbar
output_frame = ttk.Frame(main_frame)
output_frame.pack(fill=tk.BOTH, expand=True)

output_text = tk.Text(
    output_frame, height=15, wrap=tk.WORD, state=tk.DISABLED,
    font=("Consolas", 11), bg="#252535", fg=fg_color, insertbackground=fg_color,
    relief=tk.FLAT, borderwidth=5
)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text.configure(yscrollcommand=scrollbar.set)

# Text tags for colors
output_text.tag_config("error", foreground=error_color, font=("Consolas", 11, "bold"))
output_text.tag_config("price", foreground=price_color)
output_text.tag_config("market_cap", foreground=market_cap_color)
output_text.tag_config("volume", foreground=volume_color)
output_text.tag_config("change", foreground=change_color)
output_text.tag_config("heading", foreground=heading_color, font=("Consolas", 12, "bold"))

root.mainloop()
