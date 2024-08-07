# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/home_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HomeWindow(object):
    def setupUi(self, HomeWindow):
        HomeWindow.setObjectName("HomeWindow")
        HomeWindow.resize(495, 600)
        self.centralwidget = QtWidgets.QWidget(HomeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 550, 471, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(80, 20, 341, 111))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(420, 90, 47, 13))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.open_duty_btn = QtWidgets.QPushButton(self.centralwidget)
        self.open_duty_btn.setGeometry(QtCore.QRect(120, 180, 251, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.open_duty_btn.setFont(font)
        self.open_duty_btn.setObjectName("open_duty_btn")
        self.open_park_btn = QtWidgets.QPushButton(self.centralwidget)
        self.open_park_btn.setGeometry(QtCore.QRect(120, 280, 251, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.open_park_btn.setFont(font)
        self.open_park_btn.setObjectName("open_park_btn")
        self.open_cars_btn = QtWidgets.QPushButton(self.centralwidget)
        self.open_cars_btn.setGeometry(QtCore.QRect(120, 370, 251, 61))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.open_cars_btn.setFont(font)
        self.open_cars_btn.setObjectName("open_cars_btn")
        HomeWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(HomeWindow)
        QtCore.QMetaObject.connectSlotsByName(HomeWindow)

    def retranslateUi(self, HomeWindow):
        _translate = QtCore.QCoreApplication.translate
        HomeWindow.setWindowTitle(_translate("HomeWindow", "СКУД КТП"))
        self.label.setText(_translate("HomeWindow", "Оразбекұлы Ерлан 594 гр. (Кибербезопасность) 2022 год"))
        self.label_2.setText(_translate("HomeWindow", "СКУД КТП"))
        self.label_3.setText(_translate("HomeWindow", "ver 1.0"))
        self.open_duty_btn.setText(_translate("HomeWindow", "ДПЧ"))
        self.open_park_btn.setText(_translate("HomeWindow", "КТП"))
        self.open_cars_btn.setText(_translate("HomeWindow", "Список техники"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HomeWindow = QtWidgets.QMainWindow()
    ui = Ui_HomeWindow()
    ui.setupUi(HomeWindow)
    HomeWindow.show()
    sys.exit(app.exec_())
