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
from method_runge_kutti import method_runge_kutti
import matplotlib.pyplot as plt

from scipy.integrate import odeint

y0 = 1/2
f = lambda u, x: -(x+u)/x
t = np.linspace(1,3,1000)

y = odeint(f,y0,t)


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.f = lambda u, x: -(x+u)/x
        self.initUI()

    def initUI(self):
        reg_num = QtCore.QRegExp("[0-9]{1,8}")
        validator_num = QtGui.QRegExpValidator(reg_num)
        reg = QtCore.QRegExp("^[-]?[0-9]{1,5}(\.[0-9]{1,3})?")
        validator = QtGui.QRegExpValidator(reg)
        
        self.lbl_breakdown = QLabel(self)
        self.lbl_breakdown.move(10, 12)
        self.lbl_breakdown.setFont(QFont("Arial", 11))
        self.lbl_breakdown.setText("Введіть кількіть розбиттів: ")
        
        self.num_breakdown = QLineEdit(self)
        self.num_breakdown.move(210, 10)
        self.num_breakdown.resize(80, 20)
        self.num_breakdown.setValidator(validator_num)
        
        self.lbl_a = QLabel(self)
        self.lbl_a.move(10, 40)
        self.lbl_a.setFont(QFont("Arial", 11))
        self.lbl_a.setText("Введіть нижню границю: ")
        
        self.a = QLineEdit(self)
        self.a.move(210, 38)
        self.a.resize(80, 20)
        self.a.setValidator(validator)
        
        self.lbl_b = QLabel(self)
        self.lbl_b.move(10, 68)
        self.lbl_b.setFont(QFont("Arial", 11))
        self.lbl_b.setText("Введіть верхню границю: ")
        
        self.b = QLineEdit(self)
        self.b.move(210, 66)
        self.b.resize(80, 20)
        self.b.setValidator(validator)


        self.lbl_u0 = QLabel(self)
        self.lbl_u0.move(10, 96)
        self.lbl_u0.setFont(QFont("Arial", 11))
        self.lbl_u0.setText("Введіть початкову умову: ")
        
        self.u0 = QLineEdit(self)
        self.u0.move(210, 94)
        self.u0.resize(80, 20)
        self.u0.setValidator(validator)

        but = QPushButton("Диференціювати", self)
        but.resize(120, 30)
        but.move(310, 88)
        but.clicked.connect(self.solve)
        
        func = QLabel(self)
        func.move(310, 6)
        func.setFont(QFont("Arial", 11))
        func.setText("f(x, u) = -(x+u)/x")
        
        real_res = QLabel(self)
        real_res.move(310, 26)
        real_res.setFont(QFont("Arial", 11))
        real_res.setText("Розвязок при границях [1, 3] та u(a) = 1/2: \n"+str(y[-1]))
        
        self.setGeometry(100, 100, 600, 150)
        self.setWindowTitle('Метод квадратного кореня')        
        self.show()
    
    def solve(self):
        num_breakdown = int(self.num_breakdown.text())
        a = float(self.a.text())
        b = float(self.b.text())
        u0 = float(self.u0.text())
        if self.b_less_a():
            QMessageBox.warning(self, "Message", 
                                "Нижня границя не може бути більше верхньої")
        else:
            x, y = method_runge_kutti(a, b, u0, num_breakdown)
            plt.plot(x, y)
            plt.show()
            QMessageBox.information(self, "Message", "Диференціал = "+str(y[-1]))
    
    def b_less_a(self):
        return float(self.a.text()) > float(self.b.text())
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())