import sys
import numpy as np
from interface import MainWindow, SecondWindow
from PyQt5.QtWidgets import QApplication
from sqrt_method import sqrt_method


app = QApplication(sys.argv)

def test_positive_result():
    A = np.array([[9, 3, 4],
                  [3, 2, 1],
                  [4, 1, 2]])
    b = np.array([3, 1 , -1])
    x = sqrt_method(A, b)
    assert np.array_equal(np.round(x, 5), np.round(np.linalg.solve(A, b), 5))

def test_true_symmetric():
    A = np.array([[5, 4, 3],
                  [4, 5, 9],
                  [3, 9, 3]])
    assert SecondWindow(3).is_symmetric(A)

def test_false_symmetric():
    A = np.array([[5, 4, 3],
                  [1, 5, 9],
                  [3, 9, 3]])
    assert not SecondWindow(3).is_symmetric(A)

def test_true_positive():
    A = np.array([[ 6, -1,  0,  2],
                  [-1,  5,  2,  3],
                  [ 0,  2,  3, -1],
                  [ 2,  3, -1, 10]])
    assert SecondWindow(4).is_positive(A) 


def test_false_positive():
    A = np.array([[5, 4, 3],
                  [1, 5, 9],
                  [3, 9, 3]])
    assert not SecondWindow(3).is_positive(A)


test_positive_result()
print(test_positive_result.__name__, "past")

test_true_symmetric()
print(test_true_symmetric.__name__, "past")

test_false_symmetric()
print(test_false_symmetric.__name__, "past")

test_true_positive()
print(test_true_positive.__name__, "past")

test_false_positive()
print(test_false_positive.__name__, "past")