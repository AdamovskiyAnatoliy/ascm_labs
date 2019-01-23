import numpy as np


class TransportProblem:
    def __init__(self, stocks, needs, A):
        self.A = A.copy()
        self.stocks = stocks.copy()
        self.needs = needs.copy()
        
    def solve(self, max_iter=100):
        transportation_plan = np.zeros_like(self.A)
        A_copy = self.A.copy()
        for i in range(max_iter):
            min_row, min_col = np.unravel_index(np.argmin(A_copy, axis=None), A_copy.shape)
            cargo_volume = min(self.stocks[min_row], self.needs[min_col])
            
            transportation_plan[min_row, min_col] = cargo_volume
            self.stocks[min_row] -= cargo_volume 
            self.needs[min_col] -= cargo_volume
            
            if self.stocks[min_row] == 0:
                A_copy[min_row] = 10**10
            if self.needs[min_col] == 0:
                A_copy[:, min_col] = 10**10
            
            if np.array_equal(A_copy, 0):
                break
        return transportation_plan, np.sum(self.A * transportation_plan)