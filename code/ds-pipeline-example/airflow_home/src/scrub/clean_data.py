import os
import sys
import pandas as pd

PROJECT_DIRECTORY = os.getenv(key='AIRFLOW_HOME')
sys.path.append(PROJECT_DIRECTORY)

from src import get_raw_iris

path_ = "/".join(PROJECT_DIRECTORY.split('/')[:-1])
path_

def compress_numeric_columns(COL):
    """
    If the passed COL is numeric,
    downcast it to the lowest size.
    Else,
    Return as-is.

    Parameters
    -----------
    COL: pandas.Series
        The Series to shrink

    Returns
    -------
    if numeric, a compressed series
    """
    if 'float' in str(COL.dtype):
        return pd.to_numeric(COL, downcast='float', errors='ignore')
    elif 'int' in str(COL.dtype):
        return pd.to_numeric(COL, downcast='int', errors='ignore')
    else:
        return COL

def get_clean_iris():
    """
    If file exists in data/processed/, recover it
    If it doesn't, import and clean it again
    Compress it if possible
    """
    if os.path.exists(f"{path_}/data/processed/iris.csv"):
        print("Retrieving clean data from backup...")
        df = pd.read_csv(f"{path_}/data/processed/iris.csv")
        return df
    else:
        df = get_raw_iris()
        df.columns = \
        map(lambda i: ''.join([x for x in i.lower() if x not in './()& ']).replace('cm', ''),
            df.columns)
        print("Persisting cleaned iris data...")
        df.to_csv(f"{path_}/data/processed/iris.csv")
        return df

if __name__ == "__main__":
    import sys
    sys.path.append(os.getcwd())

    from src.obtain import get_raw_iris
    _ = get_clean_iris()
