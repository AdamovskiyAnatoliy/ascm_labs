import numpy as np

def method_left_rectangles(f, a, b, n=1000):
    xi = np.linspace(a, b, n)[:-1]
    yi = f(xi)
    h = xi[1] - xi[0]
    return np.sum(h * yi)
