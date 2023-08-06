import numpy as np
import pandas as pd

def counts_by_col(data):
    counts=data.isnull().sum()
    return counts

def drop_r(data):
    data = data.dropna(axis = 0)
    return pd.DataFrame(data)

