import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import indicators as ind
pd.set_option('display.max_columns', None)

ticker = yf.Ticker("AAPL")
vxticker = yf.Ticker("^VIX")
df = ticker.history(period="5y")
vix_df = vxticker.history(period="5y")
vix_df.rename(columns={"Close":"VIX"}, inplace=True)
df.index = df.index.tz_localize(None)
vix_df.index = vix_df.index.tz_localize(None)
df = df.join(vix_df["VIX"], how = 'left')
df["MA50"] = ind.calculate_ma(df["Close"], window=50)
df["MA200"] = ind.calculate_ma(df["Close"], window=200)
df["RSI"] = ind.calculate_rsi(df["Close"], window=14)
df["Return"] = df["Close"].pct_change()
df["Raw_signal"] = ((df["MA50"] > df["MA200"]) & (df["VIX"] <25)).astype(int)
df["Signal"] = df["Raw_signal"].shift(1)
df["Strategy_Return"] = df["Return"] * df["Signal"]
print(df[["Close", "MA50", "MA200", "Raw_signal","VIX"]].tail(10))


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

