# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scanner.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Scanner(object):
    def setupUi(self, Scanner):
        Scanner.setObjectName("Scanner")
        Scanner.resize(454, 357)
        self.centralwidget = QtWidgets.QWidget(Scanner)
        self.centralwidget.setObjectName("centralwidget")
        self.lbl_motor_name = QtWidgets.QLabel(self.centralwidget)
        self.lbl_motor_name.setGeometry(QtCore.QRect(40, 30, 121, 16))
        self.lbl_motor_name.setObjectName("lbl_motor_name")
        self.tbox_motor_name = QtWidgets.QLineEdit(self.centralwidget)
        self.tbox_motor_name.setGeometry(QtCore.QRect(40, 60, 371, 25))
        self.tbox_motor_name.setObjectName("tbox_motor_name")
        self.lbl_start_pos = QtWidgets.QLabel(self.centralwidget)
        self.lbl_start_pos.setGeometry(QtCore.QRect(40, 105, 121, 16))
        self.lbl_start_pos.setObjectName("lbl_start_pos")
        self.tbox_start_pos = QtWidgets.QLineEdit(self.centralwidget)
        self.tbox_start_pos.setGeometry(QtCore.QRect(160, 100, 71, 25))
        self.tbox_start_pos.setObjectName("tbox_start_pos")
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(50, 260, 80, 25))
        self.btn_start.setObjectName("btn_start")
        self.btn_stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_stop.setGeometry(QtCore.QRect(310, 260, 80, 25))
        self.btn_stop.setObjectName("btn_stop")
        self.lbl_num_steps = QtWidgets.QLabel(self.centralwidget)
        self.lbl_num_steps.setGeometry(QtCore.QRect(40, 185, 121, 16))
        self.lbl_num_steps.setObjectName("lbl_num_steps")
        self.lbl_num_loops = QtWidgets.QLabel(self.centralwidget)
        self.lbl_num_loops.setGeometry(QtCore.QRect(40, 225, 121, 16))
        self.lbl_num_loops.setObjectName("lbl_num_loops")
        self.spinBox_num_steps = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_num_steps.setGeometry(QtCore.QRect(160, 180, 71, 25))
        self.spinBox_num_steps.setObjectName("spinBox_num_steps")
        self.spinBox_num_loops = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_num_loops.setGeometry(QtCore.QRect(160, 220, 71, 25))
        self.spinBox_num_loops.setObjectName("spinBox_num_loops")
        self.lbl_end_pos = QtWidgets.QLabel(self.centralwidget)
        self.lbl_end_pos.setGeometry(QtCore.QRect(40, 145, 121, 16))
        self.lbl_end_pos.setObjectName("lbl_end_pos")
        self.tbox_end_pos = QtWidgets.QLineEdit(self.centralwidget)
        self.tbox_end_pos.setGeometry(QtCore.QRect(160, 140, 71, 25))
        self.tbox_end_pos.setObjectName("tbox_end_pos")
        self.lbl_names = QtWidgets.QLabel(self.centralwidget)
        self.lbl_names.setGeometry(QtCore.QRect(40, 290, 541, 41))
        self.lbl_names.setObjectName("lbl_names")
        Scanner.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Scanner)
        self.statusbar.setObjectName("statusbar")
        Scanner.setStatusBar(self.statusbar)

        self.retranslateUi(Scanner)
        QtCore.QMetaObject.connectSlotsByName(Scanner)

    def retranslateUi(self, Scanner):
        _translate = QtCore.QCoreApplication.translate
        Scanner.setWindowTitle(_translate("Scanner", "Scanner"))
        self.lbl_motor_name.setText(_translate("Scanner", "Motor name:"))
        self.lbl_start_pos.setText(_translate("Scanner", "Start position"))
        self.btn_start.setText(_translate("Scanner", "start"))
        self.btn_stop.setText(_translate("Scanner", "stop"))
        self.lbl_num_steps.setText(_translate("Scanner", "Number of steps"))
        self.lbl_num_loops.setText(_translate("Scanner", "Number of loops"))
        self.lbl_end_pos.setText(_translate("Scanner", "End position"))
        self.lbl_names.setText(_translate("Scanner", "Created by Matt Ware, Jordan O\'Neal, Kathryn Ledbetter, \n"
"and Takahiro Sato.  See readme for License info."))

