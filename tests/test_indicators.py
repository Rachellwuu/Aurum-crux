import pandas as pd
import sys
sys.path.insert(0,'..')
from indicators import calculate_ma, calculate_rsi

def test_calculate_ma():
    series = pd.Series([1, 2, 3, 4, 5])
    result = calculate_ma(series, window=3)
    assert pd.isna(result.iloc[0])
    assert pd.isna(result.iloc[1])
    assert result.iloc[2] == 2.0
    assert result.iloc[3] == 3.0
    assert result.iloc[4] == 4.0

def test_calculate_ma_window_greater_than_series_length():
    series = pd.Series([1, 2, 3])
    result = calculate_ma(series, window=5)
    assert pd.isna(result.iloc[0])
    assert pd.isna(result.iloc[1])
    assert pd.isna(result.iloc[2])

def test_calculate_rsi():
    series = pd.Series([100,102, 101, 103, 105, 104, 106, 108, 107, 109, 100, 102, 101, 101])
    result = calculate_rsi(series, window=14)
    result = result.dropna() 
    assert (result>= 0).all()
    assert (result<= 100).all()
