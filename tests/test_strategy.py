import pandas as pd
import sys
sys.path.insert(0,'..')
from strategy import generate_signals

def test_signal_shifted():
    close_prices = pd.Series(range(1, 251, 1), dtype=float)
    df = pd.DataFrame({
        "Close": close_prices,
        "VIX": [15.0]*250,
        "Return": close_prices.pct_change()
    })
    
    result = generate_signals(df)
    assert result["Signal"].iloc[5]== result["Raw_signal"].iloc[4]
    assert result["Signal"].iloc[4]== result["Raw_signal"].iloc[3]

def test_signal_is_binary():
    close_prices = pd.Series(range(1, 251, 1), dtype=float)
    df = pd.DataFrame({
        "Close": close_prices,
        "VIX": [15.0]*250,
        "Return": close_prices.pct_change()
    })
    
    result = generate_signals(df)
    assert set(result["Signal"].dropna()).issubset({0, 1})