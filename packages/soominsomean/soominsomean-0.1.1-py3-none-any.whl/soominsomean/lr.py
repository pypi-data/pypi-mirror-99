from sklearn.base import BaseEstimator, RegressorMixin
import numpy as np

# superclass
# inheriting


class LinearRegression(BaseEstimator, RegressorMixin):  # inheriting BaseEstimator and RegressorMixin class

    def fit(self, X: np.ndarray, y: np.array):
        # (X'X)^(-1)X'y
        self.parameters = np.linalg.inv(X.T @ X) @ X.T @ y  # state
        # this is useful because then you can apply other methods on this instance
        return self

    def predict(self, X: np.ndarray) -> np.array:
        predicted_y = X @ self.parameters

        return predicted_y

    # write the function
    # write the unit test and make the results similar to the scikit learn's
    # from scikit learn import the fake data and try out
