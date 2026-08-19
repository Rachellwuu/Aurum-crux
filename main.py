
import pandas as pd
import indicators as ind
import numpy as np
import backtest as bt
import metrics as met
import data as d
import strategy as strat
pd.set_option('display.max_columns', None)


df = d.fetch_data("SPY", "14y")
df = ind.add_indicators(df)
df = strat.generate_signals(df, ma_short=50, ma_long=200, vix_threshold=25)
years = (df.index[-1] - df.index[0]).days / 365.25
bt_df, trade_df = bt.run_simulation(df, initial_capital=10000)
summary = met.calculate_summary_metrics(bt_df, trade_df, years=years)
print(summary)

sweep_results = strat.run_parameter_sweep(df,ma_pairs=[(20, 50), (50, 200), (10, 30)], vix_thresholds=[20, 25, 30])
print(pd.DataFrame(sweep_results))


