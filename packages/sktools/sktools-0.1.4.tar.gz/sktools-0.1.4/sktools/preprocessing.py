__author__ = ["david26694", "cmougan"]

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.multiclass import check_classification_targets
import scipy


class CyclicFeaturizer(BaseEstimator, TransformerMixin):
    """Cyclic featurizer

    Given some numeric columns, applies sine and cosine transformations to
    obtain cyclic features. This is specially suited to month of the year,
    day of the week, day of the month, hour of the day, etc, where the plain
    numeric representation doesn't work very well.

    Parameters
    ----------
    cols : list
        columns to be encoded using sine and cosine transformations. Should be numeric columns
    period_mapping : dict
        keys should be names of cols and values should be tuples indicating minimum and maximum values

    Example
    -------
    >>> from sktools import CyclicFeaturizer
    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         "posted_at": pd.date_range(
    >>>             start="1/1/2018", periods=365 * 3, freq="d"
    >>>         ),
    >>>         "created_at": pd.date_range(
    >>>             start="1/1/2018", periods=365 * 3, freq="h"
    >>>         )
    >>>     }
    >>> )
    >>> df["month_posted"] = df.posted_at.dt.month
    >>> df["hour_created"] = df.created_at.dt.hour
    >>> transformed_df = CyclicFeaturizer(
    >>>     cols=["month_posted", "hour_created"]
    >>> ).fit_transform(df)

    """

    def __init__(self, cols, period_mapping=None):
        self.cols = cols
        self.period_mapping = period_mapping

    def fit(self, X):

        # If the mapping is given, no need to run it
        if self.period_mapping is not None:
            if set(self.cols) != set(self.period_mapping.keys()):
                raise ValueError("Keys of period_mapping are not the same as cols")
            return self
        else:
            # Learn values to determine periods
            self.period_mapping = {}
            for col in self.cols:
                min_col = X[col].min()
                max_col = X[col].max()
                self.period_mapping[col] = (min_col, max_col)

        return self

    def transform(self, X):

        X = X.copy()

        for col in self.cols:
            min_col, max_col = self.period_mapping[col]
            # 24 hours -> 23 - 0 + 1
            # 365 days -> 365 - 1 + 1
            period = max_col - min_col + 1
            X[f"{col}_sin"] = np.sin(2 * (X[col] - min_col) * np.pi / period)
            X[f"{col}_cos"] = np.cos(2 * (X[col] - min_col) * np.pi / period)

        return X


class GradientBoostingFeatureGenerator(BaseEstimator, TransformerMixin):
    """
    Feature generator from a gradient boosting.

    Gradient boosting decision trees are a powerful and very convenient way to implement non-linear and tuple transformations.
    We treat each individual tree as a categorical feature that takes as value the index of the leaf an instance ends up falling in
    and then perform one hot encoding for these features.

     Parameters
    ----------
    stack_to_X: bool, default = True
        Generates leaves features using the fitted self.gbm and saves them in R.
        If `stack_to_X is True` then `.transform` returns the original features with 'R' appended as columns.
        If `stack_to_X is False` then  `.transform` returns only the leaves features from 'R'

    add_probs: bool, default = False
        If `add_probs is True` then the created features are appended a probability [0,1].
        If `add_probs is False` features are binary



    Example
    -------
    >>> from sktools import GradientBoostingFeatureGenerator
    >>> from sklearn.datasets import make_classification
    >>> X, y = make_classification()
    >>> mf = GradientBoostingFeatureGenerator()
    >>> mf.fit(X, y)
    >>> mf.transform(X)

    References
    ----------

    .. [1] Practical Lessons from Predicting Clicks on Ads at Facebook, from
    https://research.fb.com/wp-content/uploads/2016/11/practical-lessons-from-predicting-clicks-on-ads-at-facebook.pdf

    .. [2] Feature Generation with Gradient Boosted Decision Trees, Towards Data Science, Carlos Mougan
    """

    def __init__(
        self,
        stack_to_X=True,
        add_probs=False,
        regression=False,
        **kwargs,
    ):

        # Deciding whether to append features or simply return generated features
        self.stack_to_X = stack_to_X
        self.add_probs = add_probs
        self.regression = regression

        if self.regression:
            # Key arguments for the gradient boosting regressor
            self.gbm = GradientBoostingRegressor(**kwargs)

        else:
            # Key arguments for the gradient boosting classifier
            self.gbm = GradientBoostingClassifier(**kwargs)

    def _get_leaves(self, X):
        X_leaves = self.gbm.apply(X)

        # Difference in return methods
        if self.regression:
            n_rows, n_cols = X_leaves.shape
        else:
            n_rows, n_cols, _ = X_leaves.shape

        X_leaves = X_leaves.reshape(n_rows, n_cols)

        return X_leaves

    def _predict_probs(self, X):
        if self.regression == True:
            # Key arguments for the gradient boosting regressor
            return self.gbm.predict(X)
        else:
            # Key arguments for the gradient boosting classifier
            return self.gbm.predict_proba(X)

    def _decode_leaves(self, X):
        return self.encoder.transform(X).todense()

    def fit(self, X, y):

        if self.regression == False:
            # Check that is a classification target
            check_classification_targets(y)

        self.gbm.fit(X, y)
        self.encoder = OneHotEncoder(categories="auto")
        X_leaves = self._get_leaves(X)
        self.encoder.fit(X_leaves)
        return self

    def transform(self, X):
        """
        R contains the matrix with the encoded leaves. The shape depends upon the parameters.
        P contains a two columns array with the probability.
        """
        R = self._decode_leaves(self._get_leaves(X))

        if self.add_probs:
            P = self._predict_probs(X)
            R = np.hstack((R, P))
            X_new = np.hstack((X, R)) if self.stack_to_X == True else R

        else:
            X_new = np.hstack((X, R)) if self.stack_to_X == True else R
        return X_new
