import numpy as np
import pandas as pd
def calculate_sharpe(returns: pd.Series, risk_free_rate: float= 0.0):
    std= returns.std()
    if std == 0:
        return 0
    return (returns.mean()- risk_free_rate)/ std * np.sqrt(252)

def calculate_cagr(returns: pd.Series, years: float):
    return (returns.add(1).prod())**(1/years) - 1