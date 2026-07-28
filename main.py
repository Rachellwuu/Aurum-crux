import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import indicators as ind
import numpy as np
import backtest as bt
import metrics as met
pd.set_option('display.max_columns', None)

test_ticker = "SPY"
test_year = "14y"
ticker = yf.Ticker(test_ticker)
vxticker = yf.Ticker("^VIX")
df = ticker.history(period=test_year)
vix_df = vxticker.history(period=test_year)
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

df["Position"] = df["Signal"]
df["Entry"]= df["Signal"].diff() == 1
df["Exit"]= df["Signal"].diff() == -1
df["Cost"] = np.zeros(len(df))
df.loc[df["Entry"]|df["Exit"], "Cost"] = -0.001
df["Strategy_Return"] = df["Return"] * df["Signal"] + df["Cost"]
bt_df, trade_df = bt.run_simulation(df, initial_capital=10000)
#print(bt_df[["Close", "Portfolio_Value"]].tail(10))
#print(trade_df[["Action", "Price", "Shares", "Date", "Portfolio_Value"]].tail(5))
#print(met.calculate_summary_metrics(bt_df["Strategy_Return"], trade_df, years=(df.index[-1] - df.index[0]).days / 365.25))
#print(df["Close"].head(10))
#print((1 + df["Return"]).cumprod().iloc[-1])
#print((1 + df["Strategy_Return"]).cumprod().iloc[-1])
def run_parameter_sweep(ma_pairs, vix_thresholds):
    results = []
    for(par1, par2) in ma_pairs:
        for vix_threshold in vix_thresholds:
            df["MA1"] = ind.calculate_ma(df["Close"], window = par1)
            df["MA2"] = ind.calculate_ma(df["Close"], window = par2)
            df["Raw_signal"]= ((df["MA1"] > df["MA2"]) & (df["VIX"] < vix_threshold)).astype(int)
            df["Signal"] = df["Raw_signal"].shift(1)
            df["Position"] = df["Signal"]
            df["Entry"] = df["Signal"].diff() == 1
            df["Exit"] = df["Signal"].diff() == -1
            df["Cost"] = np.zeros(len(df))
            df.loc[df["Entry"] | df["Exit"], "Cost"] = -0.001
            df["Strategy_Return"] = df["Return"] * df["Signal"] + df["Cost"]
            bt_df, trade_df = bt.run_simulation(df, initial_capital=10000)
            metrics = met.calculate_summary_metrics(bt_df, trade_df, years=(df.index[-1] - df.index[0]).days / 365.25)
            results.append({"MA1": par1, "MA2": par2, "VIX": vix_threshold, **metrics})
    return results
sweep_results = run_parameter_sweep(ma_pairs=[(20, 50), (50, 200), (10, 30)], vix_thresholds=[20, 25, 30])
print(pd.DataFrame(sweep_results))
plt.figure(figsize=(12,6))
plt.plot(df.index, df["Close"], label="Close", linewidth=1)
plt.plot(df["MA50"], label="50-Day MA", linewidth=1.5)
plt.plot(df["MA200"], label="200-Day MA", linewidth=1.5)
plt.title("Stock Price with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.tight_layout()
plt.show()

