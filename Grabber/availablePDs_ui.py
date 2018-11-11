# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'availablePDs.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(433, 316)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEditSearch = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEditSearch.setGeometry(QtCore.QRect(130, 20, 271, 31))
        self.plainTextEditSearch.setObjectName("plainTextEditSearch")
        self.pushButtonSearch = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSearch.setGeometry(QtCore.QRect(30, 20, 91, 31))
        self.pushButtonSearch.setObjectName("pushButtonSearch")
        self.plainTextEditPDList = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEditPDList.setGeometry(QtCore.QRect(30, 60, 371, 221))
        self.plainTextEditPDList.setReadOnly(True)
        self.plainTextEditPDList.setObjectName("plainTextEditPDList")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButtonSearch, self.plainTextEditSearch)
        MainWindow.setTabOrder(self.plainTextEditSearch, self.plainTextEditPDList)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Available Point Detectors"))
        self.pushButtonSearch.setText(_translate("MainWindow", "Search"))

