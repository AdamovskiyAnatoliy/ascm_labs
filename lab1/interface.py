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
from sqrt_method import sqrt_method


class MainWindow(QWidget):

    def __init__(self, parent=None):
    
        super().__init__(parent)
        self.dim = "2"
        self.secondWin = None
        self.initUI()

    def initUI(self):
        
        self.lbl = QLabel(self)
        self.lbl.move(10, 12)
        self.lbl.setFont(QFont("Arial", 11))
        self.lbl.setText("Виберіть розмірність матриці коефіцієнтів: ")
        
        self.combo = QComboBox(self)
        for i in range(6):
            self.combo.addItem(str(i+2), i)
        self.combo.move(320, 10)
        self.combo.activated.connect(self.setDim)
        
        self.okbutton = QPushButton("OK", self)
        self.okbutton.move(160, 60)
        self.okbutton.clicked.connect(self.openWin)

        self.setGeometry(150, 150, 400, 100)
        self.setWindowTitle('Метод квадратного кореня')
        
        self.show()
            
    def setDim(self, index):
        self.dim = self.combo.itemText(index)
        
    def openWin(self):
        if self.secondWin is not None:
            self.secondWin = None
            self.secondWin = SecondWindow(self.dim)
            self.secondWin.show()
        else:
            self.secondWin = SecondWindow(self.dim)
            self.secondWin.show()
    
    
class SecondWindow(QMainWindow):
    
    def __init__(self, dim, parent=None):
        
        super().__init__(parent, QtCore.Qt.Window)
        self.matrix_entry = []
        self.x_str = []
        self.dim = int(dim)
        self.initUI()
        
    def initUI(self):
        
        reg = QtCore.QRegExp("^[-]?[0-9]{1,8}(\.[0-9]{1,6})?")
        validator = QtGui.QRegExpValidator(reg)
        
        for i in range(self.dim+1):
            self.matrix_entry.append([])
            self.x_str.append([])
            
            for j in range(self.dim):
                self.matrix_entry[i].append(QLineEdit(self))
                self.matrix_entry[i][j].resize(30, 20)
                
                if i == self.dim:
                    self.matrix_entry[i][j].move(120+70*(i-1), 12+30*j)
                else:
                    self.matrix_entry[i][j].move(10+70*i, 12+30*j)
                    self.x_str[i].append(QLabel("x"+str(i+1), self))
                    self.x_str[i][j].move(45+70*i, 10+30*j)
                    
                    equal_label = QLabel("=", self)
                    equal_label.move(85+70*(self.dim-1), 8+30*i)
                
                self.matrix_entry[i][j].setValidator(validator)
        
        but = QPushButton("Розв\'язати систему", self)
        but.resize(130, 30)
        but.move(225, 40+30*self.dim)
        but.clicked.connect(self.solve)
        
        self.setGeometry(150, 150, 600, 400)
        self.setWindowTitle('Метод квадратного кореня')
    
    def solve(self):
        
        b = False
        for i in range(self.dim+1):
            for j in range(self.dim):
                if not self.matrix_entry[i][j].text() in ('', '-'):
                    b = True
                    continue
                else:
                    QMessageBox.warning(self, "Message",
                                    "Всі поля мають бути заповнені")
                    b = False
                    break
            if b == False:
                break
        
        if b == True:
        
            A = np.zeros((self.dim, self.dim))
            b = np.zeros(self.dim)
    
            for i in range(self.dim+1):
                for j in range(self.dim):
                    if i == self.dim:
                        b[j] = float(self.matrix_entry[i][j].text())
                    else:
                        A[i][j] = float(self.matrix_entry[j][i].text())
    
            if not self.is_symmetric(A):
                QMessageBox.warning(self, "Message",
                                    "Матриця коефіцієнтів не симетрична")
            elif not self.is_positive(A):
                QMessageBox.warning(self, "Message",
                        "Матриця коефіцієнтів не є додатньо визначеною")
            else:
                x = sqrt_method(A, b)
                QMessageBox.information(self, "Message", "X = "+str(x))
    
    def is_symmetric(self, A):
        return np.array_equal(A, A.T)
    
    def is_positive(self, A):
        return np.all(np.linalg.eigvals(A) > 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())