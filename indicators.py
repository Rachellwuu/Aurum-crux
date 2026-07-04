import pandas as pd
def calculate_ma(series: pd.Series, window: int) -> pd.Series:
    """returns the moving average of the 'Close' column in a specified window."""
    return series.rolling(window=window).mean()

def calculate_rsi(series:pd.Series, window:int =14)-> pd.Series:
    """returns the relative strength index of the 'Close' column in a specified window."""
    
    diff = series.diff()
    gain = diff.clip(lower=0)
    loss = diff.clip(upper=0).abs()
    rsi = 100 - (100 / (1 + gain.rolling(window=window).mean() / loss.rolling(window=window).mean()))
    return rsi
