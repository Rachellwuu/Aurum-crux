import yfinance as yf
import matplotlib.pyplot as plt

ticker = yf.Ticker("AAPL")
df = ticker.history(period="5y")

df["MA50"] = df["Close"].rolling(window=50).mean()
df["MA200"] = df["Close"].rolling(window=200).mean()

plt.figure(figsize=(12,6))
plt.plot(df.index, df["Close"], label="AAPL Close", linewidth=1)
plt.plot(df["MA50"], label="50-Day MA", linewidth=1.5)
plt.plot(df["MA200"], label="200-Day MA", linewidth=1.5)
plt.title("AAPL Stock Price with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.tight_layout()
plt.show()

