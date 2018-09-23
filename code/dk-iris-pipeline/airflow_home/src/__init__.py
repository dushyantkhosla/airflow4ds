import os
PROJECT_DIRECTORY = "/".join(os.getcwd().split('/')[:-1])

from .obtain import get_raw_iris
from .scrub import get_clean_iris, compress_numeric_columns
from .explore import class_imbalance, variance_by_group, anova_results, anova
