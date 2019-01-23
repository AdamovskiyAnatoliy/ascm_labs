import numpy as np
from scipy.optimize import minimize
from method import method_rosenbrock

def test_rosenbroc_func():        
    f = lambda x: (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2
    x0 = np.array([-1, 3])
    f_minimize = minimize(f, x0)
    x_min = f_minimize.x
    y_min = f_minimize.fun
    xi, yi, ei = method_rosenbrock(func=f, x0=x0)
    assert np.array_equal(np.round(x_min, 4), np.round(xi[-1], 4))

def test_rosenbroc_func100():        
    f = lambda x: (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2
    x0 = np.array([-100, 100])
    f_minimize = minimize(f, x0)
    x_min = f_minimize.x
    y_min = f_minimize.fun
    xi, yi, ei = method_rosenbrock(func=f, x0=x0)
    assert np.array_equal(np.round(x_min, 4), np.round(xi[-1], 4))

def test_square_func():        
    f = lambda x: (1 - x[0])**2 + (x[1] - 4)**2
    x0 = np.array([-1, 3])
    f_minimize = minimize(f, x0)
    x_min = f_minimize.x
    y_min = f_minimize.fun
    xi, yi, ei = method_rosenbrock(func=f, x0=x0)
    assert np.array_equal(np.round(x_min, 4), np.round(xi[-1], 4))

def test_square_func100():        
    f = lambda x: (1 - x[0])**2 + (x[1] - 4)**2
    x0 = np.array([-1, 3])
    f_minimize = minimize(f, x0)
    x_min = f_minimize.x
    y_min = f_minimize.fun
    xi, yi, ei = method_rosenbrock(func=f, x0=x0)
    assert np.array_equal(np.round(x_min, 4), np.round(xi[-1], 4))


test_rosenbroc_func()
print(test_rosenbroc_func.__name__, "past")
test_rosenbroc_func100()
print(test_rosenbroc_func100.__name__, "past")
test_square_func()
print(test_square_func.__name__, "past")
test_square_func100()
print(test_square_func100.__name__, "past")