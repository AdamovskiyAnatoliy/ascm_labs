import sys
import numpy as np
from interface import MainWindow
from PyQt5.QtWidgets import QApplication, QLineEdit
from method_runge_kutti import method_runge_kutti

app = QApplication(sys.argv)

def test_positive_result():
    a = 1
    b = 3
    u0 = 1
    x, y = method_runge_kutti(a, b, u0)
    assert np.round(y[-1], 5) == -1

def test_true_b_less_a():
    window = MainWindow()
    window.a = QLineEdit(window)
    window.b = QLineEdit(window)
    window.a.setText("5")
    window.b.setText("1")
    assert window.b_less_a() 
    
def test_false_b_less_a():
    window = MainWindow()
    window.a = QLineEdit(window)
    window.b = QLineEdit(window)
    window.a.setText("1")
    window.b.setText("5")
    assert not window.b_less_a() 


test_positive_result()
print(test_positive_result.__name__, "past")


test_true_b_less_a()
print(test_true_b_less_a.__name__, "past")

test_false_b_less_a()
print(test_false_b_less_a.__name__, "past")