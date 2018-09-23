import os
import sys
# Allow Python to discover local modules
sys.path.append(os.getenv(key='AIRFLOW_HOME'))

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

from src import PROJECT_DIRECTORY
from src.scrub import get_clean_iris

def get_train_test_data():
    """
    """
    df = get_clean_iris()
    X = df.copy().drop(['iris_type'], axis=1)
    y = df.copy().loc[:, 'iris_type'].replace({'setosa': 0, 'versicolor': 1, 'virginica': 2})
    return train_test_split(X, y, test_size=0.30, random_state=112358)


def run_model_benchmark():
    """
    """
    X_tr, X_te, y_tr, y_te = get_train_test_data()
    lr_0 = LogisticRegression()
    lr_0.fit(X_tr, y_tr)
    y_pr = lr_0.predict(X_te)
    print(f"Benchmark Model Accuracy: {accuracy_score(y_te, y_pr)}")
