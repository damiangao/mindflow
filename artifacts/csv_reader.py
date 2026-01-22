import pandas as pd

def read_csv_safe(filepath, **kwargs):
    '''安全读取CSV文件'''
    return pd.read_csv(filepath, **kwargs)
