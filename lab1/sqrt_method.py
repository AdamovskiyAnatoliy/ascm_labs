import numpy as np


def sqrt_method(A, b):
    n, m = A.shape
    U = np.zeros((n, m), dtype=float) 
    for i in range(n):
        U[i, i] = np.sqrt(A[i, i] - np.sum(U[:i, i]**2))
        for j in range(i+1,m):
            U[i, j] = (A[i, j] - np.sum(U[:i, i] * U[:i, j])) / U[i, i]
    y = triangle_solve(U.T, b, 'low')
    x = triangle_solve(U, y, 'upp')
    return x 
    
def triangle_solve(A, b, triangle_type):
    n, m = A.shape
    y = np.zeros((n,), dtype=float)
    if triangle_type == 'low':
        for i in range(n):
            y[i] = (b[i] - np.sum(A[i, :i] * y[:i])) / A[i, i]
    elif triangle_type == 'upp':
        for i in range(n-1, -1, -1):
            y[i] = (b[i] - np.sum(A[i, i:] * y[i:])) / A[i, i]      
    return y