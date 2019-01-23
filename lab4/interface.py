import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore, QtGui
import numpy as np
from rosenbrock import method_rosenbrock
import matplotlib.pyplot as plt


from scipy.optimize import minimize

f = lambda x: (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2
x0 = np.array([-1, 3])
f_minimize = minimize(f, x0)
x_min = f_minimize.x
y_min = f_minimize.fun


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.f = lambda x: (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2
        self.initUI()

    def initUI(self):
        #reg_num = QtCore.QRegExp("[0-9]{1,8}")
        #validator_num = QtGui.QRegExpValidator(reg_num)
        reg = QtCore.QRegExp("^[-]?[0-9]{1,5}(\.[0-9]{1,3})?")
        validator = QtGui.QRegExpValidator(reg)
        
        
        
        self.lbl_breakdown = QLabel(self)
        self.lbl_breakdown.move(10, 12)
        self.lbl_breakdown.setFont(QFont("Arial", 11))
        self.lbl_breakdown.setText("Введіть швидкість навчання: ")
        
        self.num_breakdown = QLineEdit(self)
        self.num_breakdown.move(210, 10)
        self.num_breakdown.resize(80, 20)
        self.num_breakdown.setValidator(validator)
        
        self.lbl_a = QLabel(self)
        self.lbl_a.move(10, 40)
        self.lbl_a.setFont(QFont("Arial", 11))
        self.lbl_a.setText("Введіть x: ")
        
        self.a = QLineEdit(self)
        self.a.move(210, 38)
        self.a.resize(80, 20)
        self.a.setValidator(validator)
        
        self.lbl_b = QLabel(self)
        self.lbl_b.move(10, 68)
        self.lbl_b.setFont(QFont("Arial", 11))
        self.lbl_b.setText("Введіть y: ")
        
        self.b = QLineEdit(self)
        self.b.move(210, 66)
        self.b.resize(80, 20)
        self.b.setValidator(validator)

        but = QPushButton("Знайти мінімум", self)
        but.resize(120, 30)
        but.move(310, 88)
        but.clicked.connect(self.solve)
        
        func = QLabel(self)
        func.move(310, 6)
        func.setFont(QFont("Arial", 11))
        func.setText("f(x, y) = (1 - x)^2 + 100*(y - x^2)^2")
        
        real_res = QLabel(self)
        real_res.move(310, 26)
        real_res.setFont(QFont("Arial", 11))
        real_res.setText("Оптимальний X: {} Значення в оптимальній точці: {}\n".format(
                np.round(x_min, 4), np.round(y_min, 4)
                ))
        
        self.setGeometry(100, 100, 800, 150)
        self.setWindowTitle('Метод розенброка')        
        self.show()
    
    def solve(self):
        try:
            learning_rate = float(self.num_breakdown.text())
            a = float(self.a.text())
            b = float(self.b.text())

            xi, yi, ei = method_rosenbrock(func=self.f, x0=np.array([a, b]), learning_rate=learning_rate**np.ones(2))

            QMessageBox.information(self, "Message", "Оптимальний X: {} Значення в оптимальній точці: {}\n".format(
                                    np.round(xi[-1], 4), np.round(yi[-1], 4) ))
        
            xi = np.array(xi)
            yi = np.array(yi)
            ei = np.array(ei)
            x = np.linspace(xi[:,0].min(), xi[:,0].max(), 100)
            y = np.linspace(xi[:,1].min(), xi[:,1].max(), 100)
            X, Y = np.meshgrid(x, y)
            Z = self.f([X, Y])
            fig, ax = plt.subplots(figsize=(8,6))
            CS = ax.contour(X, Y, Z)
            ax.clabel(CS)
            ax.set_title('Simplest default with labels')
            ax.scatter([1], [1], c='r', marker='x', s=100)
            ax.grid()
            ax.plot(xi[:,0], xi[:,1], 'o-', c='y')
            plt.show()
        except:
            QMessageBox.information(self, "Message", "Не усі поля заповнені")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
    
    
    
