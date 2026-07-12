import pandas as pd
def run_simulation(df: pd.DataFrame, initial_capital: float = 10000)-> pd.DataFrame:
    df["Portfolio_Value"] = initial_capital
    df["Shares"] = 0
    cash = initial_capital
    shares = 0
    portfolio_values = []
    trades = []
    for index, row in df.iterrows():
        if row["Entry"]:
            shares = cash / row["Close"]
            cash = 0
            trades.append(("BUY", row["Close"], shares, index,shares * row["Close"]))
        elif row["Exit"]:
            cash = shares * row["Close"]
            
            trades.append(("SELL", row["Close"], shares, index,cash))
            shares = 0
        if shares > 0:
            portfolio_values.append(shares * row["Close"])
        else:
            portfolio_values.append(cash)
    df["Portfolio_Value"] = portfolio_values
    trade_df= pd.DataFrame(trades, columns=["Action", "Price", "Shares", "Date", "Portfolio_Value"])
    return df, trade_df


            

