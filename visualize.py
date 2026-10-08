import matplotlib.pyplot as plt
import pandas as pd
def plot_results(bt_df:pd.DataFrame, df:pd.DataFrame, initial_capital: float = 10000)-> None:
    buy_and_hold = (1+df["Return"]).cumprod() *initial_capital
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    ax1.plot(bt_df["Portfolio_Value"], label= "Strategy", linewidth =1.5)
    ax1.plot(buy_and_hold, label="Buy and Hold", linewidth=1.5)
    ax1.set_title("Equity Curve vs Buy & Hold")
    ax1.set_ylabel("Portfolio Value")
    ax1.legend()

    rolling_peak = bt_df["Portfolio_Value"].cummax()
    drawdown = (bt_df["Portfolio_Value"] - rolling_peak) / rolling_peak
    ax2.fill_between(bt_df.index, drawdown, color="red", alpha=0.3)

    ax2.set_title("Drawdown")
    ax2.set_ylabel("Drawdown %")
    ax2.set_xlabel("Date")
    plt.tight_layout()
    plt.savefig("equity_curve.png")
    plt.show()
  