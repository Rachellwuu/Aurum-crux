import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)

ticker = yf.Ticker("AAPL")
df = ticker.history(period="5y")

df["MA50"] = df["Close"].rolling(window=50).mean()
df["MA200"] = df["Close"].rolling(window=200).mean()
df["Return"] = df["Close"].pct_change()
df["Raw_signal"] = (df["MA50"] > df["MA200"]).astype(int)
df["Signal"] = df["Raw_signal"].shift(1)
df["Strategy_Return"] = df["Return"] * df["Signal"]
print(df[["Close", "MA50", "MA200", "Return", "Raw_signal", "Signal"]].tail(10))
print((1+ df["Return"]).cumprod())
print((1+ df["Strategy_Return"]).cumprod())

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

