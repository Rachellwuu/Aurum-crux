import numpy as np
import pandas as pd
def calculate_sharpe(returns: pd.Series, risk_free_rate: float= 0.0):
    std= returns.std()
    if std == 0:
        return 0
    return (returns.mean()- risk_free_rate)/ std * np.sqrt(252)

def calculate_cagr(returns: pd.Series, years: float):
    return (returns.add(1).prod())**(1/years) - 1

def calculate_max_drawdown(returns: pd.Series):
    rolling_peak = returns.cummax()
    drawdown = (returns - rolling_peak) / rolling_peak
    return drawdown.min()

def calculate_win_rate(trades_df: pd.DataFrame):
    buys = trades_df[trades_df["Action"] == "BUY"]["Price"].reset_index(drop=True)
    sells = trades_df[trades_df["Action"] == "SELL"]["Price"].reset_index(drop=True)
    min_len = min(len(buys), len(sells))
    wins = (sells[:min_len] > buys[:min_len]).sum()
    total = min_len
    return wins / total if total > 0 else 0

def calculate_summary_metrics(returns: pd.Series, trade_df: pd.DataFrame, years: float):
    sharpe = calculate_sharpe(returns)
    cagr = calculate_cagr(returns, years)
    max_drawdown = calculate_max_drawdown(trade_df["Portfolio_Value"])
    win_rate = calculate_win_rate(trade_df)
    return {"Sharpe Ratio": sharpe,"CAGR": cagr,"Max Drawdown": max_drawdown,"Win Rate": win_rate}



