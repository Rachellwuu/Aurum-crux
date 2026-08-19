import pandas as pd
import numpy as np
import indicators as ind
import backtest as bt
import metrics as met
def generate_signals(df: pd.DataFrame, ma_short: int = 50, ma_long: int = 200, vix_threshold: float = 25) -> pd.DataFrame:
    df["MA_short"] = ind.calculate_ma(df["Close"], ma_short)
    df["MA_long"] = ind.calculate_ma(df["Close"], ma_long)
    df["Raw_signal"] = ((df["MA_short"] > df["MA_long"]) & (df["VIX"] < vix_threshold)).astype(int)
    df["Signal"] = df["Raw_signal"].shift(1)

    df["Position"] = df["Signal"]
    df["Entry"]= df["Signal"].diff() == 1
    df["Exit"]= df["Signal"].diff() == -1
    df["Cost"] = np.zeros(len(df))
    df.loc[df["Entry"]|df["Exit"], "Cost"] = -0.001
    df["Strategy_Return"] = df["Return"] * df["Signal"] + df["Cost"]
    
    return df

def run_parameter_sweep(df,ma_pairs, vix_thresholds):
    results = []
    for(par1, par2) in ma_pairs:
        for vix_threshold in vix_thresholds:
            df = generate_signals(df.copy(), ma_short=par1, ma_long=par2, vix_threshold=vix_threshold)
            bt_df, trade_df = bt.run_simulation(df, initial_capital=10000)
            metrics = met.calculate_summary_metrics(bt_df, trade_df, years=(df.index[-1] - df.index[0]).days / 365.25)
            results.append({"MA1": par1, "MA2": par2, "VIX": vix_threshold, **metrics})
    return results