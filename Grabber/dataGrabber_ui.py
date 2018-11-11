# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dataGrabber.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(499, 640)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pointDetectorsInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.pointDetectorsInput.setGeometry(QtCore.QRect(30, 60, 431, 131))
        self.pointDetectorsInput.setObjectName("pointDetectorsInput")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(40, 530, 80, 16))
        self.startButton.setObjectName("startButton")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(370, 530, 80, 16))
        self.stopButton.setObjectName("stopButton")
        self.pointDetectorsInputLabel = QtWidgets.QLabel(self.centralwidget)
        self.pointDetectorsInputLabel.setGeometry(QtCore.QRect(30, 30, 221, 21))
        self.pointDetectorsInputLabel.setObjectName("pointDetectorsInputLabel")
        self.availablePointDetButton = QtWidgets.QPushButton(self.centralwidget)
        self.availablePointDetButton.setGeometry(QtCore.QRect(250, 30, 201, 20))
        self.availablePointDetButton.setObjectName("availablePointDetButton")
        self.roiSpecificationLabel = QtWidgets.QLabel(self.centralwidget)
        self.roiSpecificationLabel.setGeometry(QtCore.QRect(30, 230, 221, 16))
        self.roiSpecificationLabel.setObjectName("roiSpecificationLabel")
        self.availableROIs = QtWidgets.QPushButton(self.centralwidget)
        self.availableROIs.setGeometry(QtCore.QRect(250, 230, 201, 20))
        self.availableROIs.setObjectName("availableROIs")
        self.roiInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.roiInput.setGeometry(QtCore.QRect(30, 260, 431, 121))
        self.roiInput.setObjectName("roiInput")
        self.beamlineLabel = QtWidgets.QLabel(self.centralwidget)
        self.beamlineLabel.setGeometry(QtCore.QRect(30, 400, 181, 16))
        self.beamlineLabel.setObjectName("beamlineLabel")
        self.refDetectorLabel = QtWidgets.QLabel(self.centralwidget)
        self.refDetectorLabel.setGeometry(QtCore.QRect(30, 440, 201, 16))
        self.refDetectorLabel.setObjectName("refDetectorLabel")
        self.refDetTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.refDetTextEdit.setGeometry(QtCore.QRect(240, 435, 221, 31))
        self.refDetTextEdit.setObjectName("refDetTextEdit")
        self.beamlineTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.beamlineTextEdit.setGeometry(QtCore.QRect(240, 400, 221, 31))
        self.beamlineTextEdit.setObjectName("beamlineTextEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 560, 441, 61))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.updateButton = QtWidgets.QPushButton(self.centralwidget)
        self.updateButton.setGeometry(QtCore.QRect(40, 493, 82, 20))
        self.updateButton.setObjectName("updateButton")
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(140, 490, 321, 31))
        self.statusLabel.setText("")
        self.statusLabel.setObjectName("statusLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pointDetectorsInput, self.roiInput)
        MainWindow.setTabOrder(self.roiInput, self.beamlineTextEdit)
        MainWindow.setTabOrder(self.beamlineTextEdit, self.refDetTextEdit)
        MainWindow.setTabOrder(self.refDetTextEdit, self.updateButton)
        MainWindow.setTabOrder(self.updateButton, self.startButton)
        MainWindow.setTabOrder(self.startButton, self.stopButton)
        MainWindow.setTabOrder(self.stopButton, self.availableROIs)
        MainWindow.setTabOrder(self.availableROIs, self.availablePointDetButton)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "dataGrabber"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.pointDetectorsInputLabel.setText(_translate("MainWindow", "Specify Point Detectors"))
        self.availablePointDetButton.setText(_translate("MainWindow", "Show Available Point Detectors"))
        self.roiSpecificationLabel.setText(_translate("MainWindow", "Specify ROIs"))
        self.availableROIs.setText(_translate("MainWindow", "Show Available ROIs"))
        self.beamlineLabel.setText(_translate("MainWindow", "Specify beamline:"))
        self.refDetectorLabel.setText(_translate("MainWindow", "Specify reference detector:"))
        self.label.setText(_translate("MainWindow", "Created by Matthew Ware, Jordan O\'Neal, Kathryn Ledbetter, \n"
" and Takahiro Sato.\n"
" See readme for License information"))
        self.updateButton.setText(_translate("MainWindow", "Update"))

