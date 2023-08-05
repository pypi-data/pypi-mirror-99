from soominsomean.lr import LinearRegression as LR
from sklearn import datasets
from sklearn.linear_model import LinearRegression
import numpy as np


def test_lr():
    boston = datasets.load_boston()
    X = boston.data
    y = boston.target

    reg = LinearRegression(fit_intercept=False)  # create an instance of LR
    reg.fit(X, y)  # estimate the parameters return value could
    prediction = reg.predict(X)

    lr_reg = LR().fit(X, y)
    lr_prediction = lr_reg.predict(X)

    np.testing.assert_almost_equal(prediction, lr_prediction)
