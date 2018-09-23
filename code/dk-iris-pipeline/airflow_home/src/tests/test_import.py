import os
import numpy as np

from src.obtain import get_raw_iris

# Declare Expectations

SHAPE = (150, 5)

COLS = [
    'sepal length (cm)', 
    'sepal width (cm)', 
    'petal length (cm)',
    'petal width (cm)', 
    'iris_type'
]

TYPES = [
    np.dtype('float64'),
    np.dtype('float64'),
    np.dtype('float64'),
    np.dtype('float64'),
    np.dtype('O')
]

## Write Tests

def test_iris_import():
    """
    """
    df = get_raw_iris()
    
    assert df.shape == SHAPE
    assert df.dtypes.tolist() == TYPES
    assert all(df.columns == COLS)