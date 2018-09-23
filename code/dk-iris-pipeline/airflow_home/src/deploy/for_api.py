import pandas as pd
import numpy as np
from ..scrub import get_clean_iris

def generate_random_iris():
    """
    """
    df = get_clean_iris()

    generate_random_iris = lambda i: (df.select_dtypes(include=np.number).quantile(0.75) + np.random.randn(4)).abs()
    df_newData = pd.concat([generate_random_iris(x) for x in range(20)], axis=1).T.round(2)

    df_newData.rename(columns={
        'petallength': 'pl',
        'petalwidth': 'pw',
        'sepallength': 'sl',
        'sepalwidth': 'sw'
    }, inplace=True)

    return df_newData
