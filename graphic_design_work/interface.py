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
import pandas as pd
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from poly_reg import (
        mean_squared_error, 
        PolynomialFeatures, 
        StandardScaler, 
        LinearRegression
    )
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error

class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.degree = 2
        self.name_method = 'Набір цін на житло в Бостоні'
        self.initUI()

    def initUI(self):
        self.lbl_degree = QLabel(self)
        self.lbl_degree.move(10, 12)
        self.lbl_degree.setFont(QFont("Arial", 11))
        self.lbl_degree.setText("Оберіть степінь полінома: ")
        
        self.combo1 = QComboBox(self)
        for i in range(6):
            self.combo1.addItem(str(i+1), i)
        self.combo1.move(210, 10)
        self.combo1.setCurrentIndex(1)
        self.combo1.activated.connect(self.set_degree)
    
        self.lbl_method = QLabel(self)
        self.lbl_method.move(10, 40)
        self.lbl_method.setFont(QFont("Arial", 11))
        self.lbl_method.setText("Оберіть вхідні данні:")
        
        self.combo2 = QComboBox(self)
        for inx, val in enumerate(['Файл csv', 'Набір цін на житло в Бостоні']):
            self.combo2.addItem(val, inx)
        self.combo2.move(210, 38)
        self.combo2.setCurrentIndex(1)
        self.combo2.activated.connect(self.set_name_method)

        self.lbl_csv = QLabel(self)
        self.lbl_csv.move(10, 68)
        self.lbl_csv.setFont(QFont("Arial", 11))
        self.lbl_csv.setText("Введіть назву csv файла: ")
        self.lbl_csv.setVisible(False)
        
        self.csv = QLineEdit(self)
        self.csv.move(210, 66)
        self.csv.resize(120, 20)
        self.csv.setVisible(False)

        but = QPushButton("Побудувати поліноміальну регресію", self)
        but.resize(240, 30)
        but.move(10, 92)
        but.clicked.connect(self.solve)
        
        self.setGeometry(100, 100, 500, 150)
        self.setWindowTitle('Поліноміальна регресія')        
        self.show()
    
    def set_degree(self, index):
        self.degree = self.combo1.itemText(index)
    
    def set_name_method(self, index):
        self.name_method = self.combo2.itemText(index)
        if self.name_method ==  'Файл csv':
            self.lbl_csv.setVisible(True)
            self.csv.setVisible(True)
        else:
            self.lbl_csv.setVisible(False)
            self.csv.setVisible(False)
    
    def solve(self):
        if self.name_method == 'Файл csv':
            file_name = self.csv.text()
            try:
                data = pd.read_csv(file_name)
                X = data.drop('y', axis=1)
                y = data['y']
                res = self.fit(X, y)
                QMessageBox.information(self, 'Повідомлення', res)
            except FileNotFoundError:
                QMessageBox.information(
                        self, 
                        "Повідомлення", 
                        "У даній деректорії нема файла з назвою '{}'".format(file_name)
                )
        else:
            boston = load_boston()
            X = boston.data
            y = boston.target
            res = self.fit(X, y)
            QMessageBox.information(self, 'Повідомлення', res)
            
    def fit(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
        
        poly = PolynomialFeatures(int(self.degree))
        poly.fit(X_train)
        X_train_poly = poly.transform(X_train)
        X_test_poly = poly.transform(X_test)
        
        scalar = StandardScaler()
        scalar.fit(X_train_poly)
        
        
        X_train_poly_scalar = scalar.transform(X_train_poly)
        X_test_poly_scalar = scalar.transform(X_test_poly)
        
        lr = LinearRegression()
        lr.fit(X_train_poly_scalar, y_train)
        np.savetxt('res.txt', lr.coef_)
        train_pred = lr.predict(X_train_poly_scalar)
        test_pred = lr.predict(X_test_poly_scalar)
        train_score = mean_squared_error(y_train, train_pred)
        test_score = mean_squared_error(y_test, test_pred)
        return '''
        Похибка на тренувальних даних: {}
        Похибка на тестових даних: {}'''.format(train_score, test_score)
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
    