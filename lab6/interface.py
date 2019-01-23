import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore, QtGui
from min_element_method import TransportProblem
import numpy as np


class MainWindow(QWidget):
    
    def __init__(self, parent=None):
        
        super().__init__(parent)
        self.number_of_customers = "3"
        self.number_of_vendors = "3"
        self.secondWin = None
        self.initUI()

    def initUI(self):
        
        self.lbl_1 = QLabel(self)
        self.lbl_1.move(10, 12)
        self.lbl_1.setFont(QFont("Arial", 11))
        self.lbl_1.setText("Оберіть кількість споживачів: ")
        
        self.combo_1 = QComboBox(self)
        for i in range(9):
            self.combo_1.addItem(str(i+2), i)
        self.combo_1.move(320, 10)
        self.combo_1.setCurrentIndex(1)
        self.combo_1.activated.connect(self.set_number_of_customers)
        
        self.lbl_2 = QLabel(self)
        self.lbl_2.move(10, 40)
        self.lbl_2.setFont(QFont("Arial", 11))
        self.lbl_2.setText("Оберіть кількість постачальників: ")
        
        self.combo_2 = QComboBox(self)
        for i in range(9):
            self.combo_2.addItem(str(i+2), i)
        self.combo_2.move(320, 40)
        self.combo_2.setCurrentIndex(1)
        self.combo_2.activated.connect(self.set_number_of_vendors)
        
        self.okbutton = QPushButton("OK", self)
        self.okbutton.move(160, 90)
        self.okbutton.clicked.connect(self.openWin)

        self.setGeometry(150, 150, 400, 140)
        self.setWindowTitle('Транспортна задача')
        self.setWindowIcon(QIcon('icon.jpg'))

        self.show()
            
    def set_number_of_customers(self, index):
        self.number_of_customers = self.combo_1.itemText(index)
        
    def set_number_of_vendors(self, index):
        self.number_of_vendors = self.combo_2.itemText(index)
        
    def openWin(self):
        if self.secondWin is not None:
            self.secondWin = None
        self.secondWin = SecondWindow(self.number_of_customers,
                                      self.number_of_vendors)
        self.secondWin.show()
    
class SecondWindow(QWidget):
    
    def __init__(self, number_of_customers,
                 number_of_vendors, parent=None):
        
        super().__init__(parent)
        self.matrix_entry = []
        self.b = []
        self.a = []
        self.m = int(number_of_customers)
        self.n = int(number_of_vendors)
        self.initUI()
        
    def initUI(self):
        
        reg = QtCore.QRegExp("^[0-9]{1,8}(\.[0-9]{1,5})?")
        validator = QtGui.QRegExpValidator(reg)
        
        self.C_str = QLabel(self)
        self.C_str.move((85+50*(self.m))//2, 12)
        self.C_str.setFont(QFont("Arial", 9))
        self.C_str.setText('Матриця тарифів')
        
        for i in range(self.m):
            self.matrix_entry.append([])
            for j in range(self.n):
                self.matrix_entry[i].append(QLineEdit(self))
                self.matrix_entry[i][j].resize(45, 20)
                self.matrix_entry[i][j].move(100+50*i, 35+30*j)
                self.matrix_entry[i][j].setValidator(validator)
                
        self.b_str = QLabel(self)
        self.b_str.move(75+50*(i+2), 12)
        self.b_str.setFont(QFont("Arial", 9))
        self.b_str.setText("Запаси")
                
        for j in range(self.n):
            self.b.append(QLineEdit(self))
            self.b[j].resize(45, 20)
            self.b[j].move(75+50*(i+2), 35+30*j)
            self.b[j].setValidator(validator)
            
        self.a_str = QLabel(self)
        self.a_str.move(25, 84+30*j)
        self.a_str.setFont(QFont("Arial", 9))
        self.a_str.setText("Потреби")
        
        for i in range(self.m):
            self.a.append(QLineEdit(self))
            self.a[i].move(100+50*i, 80+30*j)
            self.a[i].resize(45, 20)
            self.a[i].setValidator(validator)
        
        but = QPushButton("Знайти опорний план\n та вартість перевезення", self)
        but.resize(170, 40)
        but.move((80+70*(self.m+1))//2, 50+30*(j+3))
        but.setFont(QFont("Arial", 10))
        but.clicked.connect(self.solve)
    
        clear_line_button = QPushButton("Очистити всі поля", self)
        clear_line_button.resize(130, 40)
        clear_line_button.move((70*(self.m+1)-200)//2,
                               50+30*(j+3))
        clear_line_button.setFont(QFont("Arial", 10))
        clear_line_button.clicked.connect(self.clear_line)
        
        self.setGeometry(150, 150, 70+60*(i+3), 35+30*(j+5))
        self.setWindowTitle('Транспортна задача')
        self.show()
        
    def clear_line(self):
        for i in range(self.m):
            for j in range(self.n):
                self.matrix_entry[i][j].clear()
                
        for i in range(self.n):
            self.b[i].clear()
            
        for i in range(self.m):
            self.a[i].clear()
            
    def isEmpty(self):
        empty = False
        for i in np.reshape(self.matrix_entry, self.m*self.n):
            if i.text() == "":
                empty = True
                break
        if empty:
            return empty
        
        for i in self.b:
            if i.text() == "":
                empty = True
                break
        if empty:
            return empty
        
        for i in self.a:
            if i.text() == "":
                empty = True
                break
            
        return empty
    
    def solve(self):
        if self.isEmpty():
            QMessageBox.warning(self, "Message",
                                "Всі поля мають бути заповнені")
        else:
                
            C = np.zeros((self.n, self.m))
            for i in range(self.n):
                for j in range(self.m):
                    C[i][j] = float(self.matrix_entry[j][i].text())
                    
            stocks = np.zeros(self.n)
            for i in range(self.n):
                stocks[i] = float(self.b[i].text())
            
            needs = np.zeros(self.m)
            for i in range(self.m):
                needs[i] = float(self.a[i].text())
                
            tp = TransportProblem(A=C, needs=needs, stocks=stocks)
            plan, func = tp.solve()
            
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText('Опорний план:\n{}\nВартість перевезення:\n{}'.format(plan, func))    
            msg.setWindowTitle("Результат")
            msg.setFont(QFont("Arial", 10))
            msg.exec_()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
