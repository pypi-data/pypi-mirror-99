# Module: RecFeatureSelect
# Author: Daniel Ryan Furman <dryanfurman@gmail.com>
# License: MIT
# Last modified : 3.10.2021

import numpy as np
import pandas as pd

# Unit tests for the feature selection algorithm.
# Set up data for the function

covariance_org = pd.read_csv('data/feature-correlations-test.csv')
feature_importance = pd.read_csv('data/feature-importance-test.csv')
threshold = 0.85
raw_data = pd.read_csv('data/raw-data-test.csv')

print(covariance_org.columns)
print(feature_importance.columns)

def test_inputs():
    # First assert that the inputs have the same features (and order)
    assert np.all(covariance_org.columns == feature_importance.columns)
    assert list(covariance_org) == list(feature_importance)

from RecFeatureSelect._main import RecFeatureSelect

def test_function():
    # Second, assert that all final correlations are lower than the threshold
    RecFeatureSelect(covariance_org, feature_importance, threshold, raw_data)
    cov = pd.read_csv('data/cov.csv', index_col = "Unnamed: 0")
    cov = cov.to_numpy()
    np.fill_diagonal(cov, 0)
    # did the algorithm remove correlated pairs above the threshold? :
    assert np.all(cov <= threshold)
