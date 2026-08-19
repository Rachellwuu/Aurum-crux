import yfinance as yf
import pandas as pd
def fetch_data(tick:str, period_yr:str) -> pd.DataFrame:
        
    ticker = yf.Ticker(tick)
    vxticker = yf.Ticker("^VIX")
    df = ticker.history(period=period_yr)
    vix_df = vxticker.history(period=period_yr)
    vix_df.rename(columns={"Close":"VIX"}, inplace=True)
    df.index = df.index.tz_localize(None)
    vix_df.index = vix_df.index.tz_localize(None)
    df = df.join(vix_df["VIX"], how = 'left')
    df["Return"] = df["Close"].pct_change()
    return df