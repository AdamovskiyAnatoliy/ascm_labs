import numpy as np


def mean_squared_error(y_real, y_pred):
    return np.mean((y_real - y_pred)**2)

class PolynomialFeatures:
    def __init__(self, degree=2, include_bias=True):
        self.degree = degree
        self.include_bias = include_bias
    
    def transform(self, X):
        if self.include_bias:
            X = np.column_stack((np.ones(X.shape[0]), X))
        num_row, num_col = X.shape
        Xpoly = X.copy()
        for col1 in range(1, num_col):
            for col2 in range(col1, num_col):
                Xpoly = np.column_stack((Xpoly, X[:, col1] * X[:, col2]))
        return Xpoly
    
class StandardScaler:
    def fit(self, X):
        self.mean = X.mean(axis=0)
        self.std = X.std(axis=0)
    
    def transform(self, X):
        return (X - self.mean) / self.std
    
    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
    
class LinearRegression():
    def __init__(self, learning_rate=0.0008, max_iter=10000, C=100):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
    
    def fit(self, X, y):
        self.coef_ = 0.01 * np.random.normal(size=(X.shape[1], 1))
        self.intercept_ = 0.01 * np.random.normal()
        for i in range(self.max_iter):
            y_pred = self.predict(X)
            dx = - np.mean(X.T @ (y - y_pred), axis=1)[:,np.newaxis]
            db = - np.mean(y - y_pred)
            self.coef_ = self.coef_ - self.learning_rate * dx
            self.intercept_ = self.intercept_ - self.learning_rate * db
            
    def predict(self, X):
        return X @ self.coef_ + self.intercept_
    
    def score(self, X, y):
        y_pred = self.predict(X)
        return mean_squared_error(y, y_pred)