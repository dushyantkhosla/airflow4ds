import os
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

path_ = "/".join(os.getenv(key='AIRFLOW_HOME').split('/')[:-1])
path_

def get_raw_iris():
    """
    If file exists in data/raw/, recover from backup
    If it doesn't, import it again
    """
    if os.path.exists(f"{path_}/data/raw/iris.csv"):
        print("Loading raw data from backup")
        return pd.read_csv(f"{path_}/data/raw/iris.csv")
    else:
        print("Downloading data")
        df_iris = \
        (pd.concat([
            pd.DataFrame(load_iris().get('data'), columns=load_iris().get('feature_names')),
            pd.DataFrame(load_iris().get('target'), columns=['iris_type'])
        ], axis=1)
         .assign(iris_type = lambda fr: fr['iris_type'].replace({k:v for k, v in enumerate(load_iris().get('target_names'))}))
        )
        print("Persisting data...")
        df_iris.to_csv(f"{path_}/data/raw/iris.csv", index=False)

    return df_iris

if __name__ == "__main__":
    import sys
    sys.path.append(os.getcwd())
    _ = get_raw_iris()
