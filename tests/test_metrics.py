import pandas as pd
import sys
sys.path.insert(0,'..')
from metrics import calculate_sharpe, calculate_cagr, calculate_max_drawdown, calculate_win_rate


def test_sharpe_positive():
    returns = pd.Series([0.01, 0.02, 0.015, 0.03, 0.025])
    result = calculate_sharpe(returns)
    assert result > 0

def test_max_drawdown_positive():
    returns = pd.Series([100, 105, 102, 110, 108])
    result = calculate_max_drawdown(returns)
    assert result <= 0