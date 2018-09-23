import os
import numpy as np
import pandas as pd

from src.scrub import get_clean_iris, compress_numeric_columns

# Define Tests

SHAPE = (150, 5)

COLS = [
    'sepallength', 
    'sepalwidth', 
    'petallength', 
    'petalwidth', 
    'iris_type'
]

TYPES = [
    np.dtype('float32'),
    np.dtype('float32'),
    np.dtype('float32'),
    np.dtype('float32'),
    np.dtype('O')
]

# Run Tests

def test_iris_scrub():
    """
    """
    df = get_clean_iris().apply(compress_numeric_columns)
    
    assert df.shape == SHAPE
    assert df.dtypes.tolist() == TYPES
    assert all(df.columns == COLS)