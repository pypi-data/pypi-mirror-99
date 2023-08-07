# Module: RecFeatureSelect
# Author: Daniel Ryan Furman <dryanfurman@gmail.com>
# License: MIT
# Last modified : 3.10.2021

import pandas as pd
import numpy as np
from scipy.stats import spearmanr

def RecFeatureSelect(covariance, feature_importance, threshold, raw_data):

    '''A recursive function for feature selection based on a
    correlation threshold and the feature importance scores.

    This function selects de-correlated features for a modeling experiment by
    filtering the most similar pair at each call. The algorithm reaches the
    stopping case when all pairs of features are below the Spearman's statistic
    `threshold`. The feature importances are used as the ranking.

    covariance: Pandas object containing the covariance matrix, with
        correlations between modeling variables, by definition containing
        ones along the diagonal. Variable names should be above the
        entries and absent from the rows.

    feature_importance: Pandas object containing a model's feature importance
        scores in the first row, with the same order of variables as the
        covariance matrix. Variable names should be above the row. Feature
        importance is generally defined as techniques that assign a score to
        input features based on how useful they are at predicting a target
        variable. Importance scores can vary, and you should therefore
        at least take a look at the associated uncertainties.

    threshold: A correlation value for which features are filtered below,
        Thresholds between 0.5 - 0.7 are commonly used (e.g. Dormann et al.,
        2013, doi: 10.1111/j.1600-0587.2012.07348.x).

    raw_data: The raw feature dataframe that constructed the covariance matrix.

    Warnings:
    --------
    * The Pandas dataframes should have the same order of variables.
    * Make sure dependencies are installed: pandas, np, scipy.

    Example:
    --------
    * See https://nbviewer.jupyter.org/github/daniel-furman/ensemble-climate-
    projections/blob/main/Comparing_MLs.ipynb, Appendix 1'''

    # initial transformations
    feature_importance.rename(index={0: 'importance'}, inplace = True)
    covariancenp = pd.DataFrame.to_numpy(covariance)
    covariancenp = np.triu(covariancenp)
    covariance = pd.DataFrame(covariancenp, columns=list(covariance))
    for i in np.arange(0,len(covariance)):
        covariance.rename(index={i: list(covariance)[i]}, inplace=True)
    covariance = covariance.abs()
    covar = covariance.copy(deep=True)
    for i in np.arange(0, len(covar)):
        for p in np.arange(0, len(covar)):
            if covar.iloc[i, p] < threshold:
                covar.iloc[i, p] = np.NaN
        covar.iloc[i, i] = np.NaN
    covariance_bool = covar.isna()

    # stopping case
    if covariance_bool.all(axis=None):
        fin = list(covariance)
        print('\nFinal set of variables:\n', fin)
        print('\nCovariance matrix (with r < ', str(threshold), '):\n')
        print(covariance)
        # save the final correlation matrix to file
        covariance.to_csv('data/cov.csv')

    # one loop forward
    else:
        for i in np.arange(0, len(covariance)):
            for p in np.arange(0, len(covariance)):
                if covariance.iloc[i, p] < threshold:
                    covariance.iloc[i, p] = np.NaN
            covariance.iloc[i, i] = np.NaN
        maximum_corr = np.max(np.max(covariance))
        for i in np.arange(0, len(covariance)):
            for p in np.arange(0, len(covariance)):
                if covariance.iloc[i, p] == maximum_corr:
                    colname = list(covariance)[p]
                    rowname = list(covariance)[i]
        min_imp = np.min([feature_importance[colname],
                          feature_importance[rowname]])
        if feature_importance[colname].loc['importance'] == min_imp:
            raw_data.drop([colname], axis=1, inplace=True)
            feature_importance.drop([colname], axis=1, inplace=True)
            print('Compared', rowname, 'or', colname, '\n      -> Dropped',
                colname)
        else:
            raw_data.drop([rowname], axis=1, inplace=True)
            feature_importance.drop([rowname], axis=1, inplace=True)
            print('Compared', rowname, 'or', colname, '\n      -> Dropped',
                rowname)
        covariance = pd.DataFrame(spearmanr(raw_data).correlation,
                                  columns=list(feature_importance))
        # recursion called
        RecFeatureSelect(covariance, feature_importance,
                         threshold, raw_data)
