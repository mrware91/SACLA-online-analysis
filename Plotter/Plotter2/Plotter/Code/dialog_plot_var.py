# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_plot_var.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import plotter
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.insert(0, '../../dataSaverLoader/')
import socket
host_name = socket.gethostname()
if 'hpc' in host_name:
        import dummyDatabase as Database
else:        
        import Database


class Ui_dialog_plot_var(QtWidgets.QMainWindow):
    def setupUi(self, dialog_plot_var, mainWindow):
        self.mainWindow = mainWindow

	# designer generated code
        dialog_plot_var.setObjectName("dialog_plot_var")
        dialog_plot_var.resize(632, 313)
        self.centralwidget = QtWidgets.QWidget(dialog_plot_var)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 611, 245))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_datastream_var = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_datastream_var.setObjectName("lbl_datastream_var")
        self.verticalLayout.addWidget(self.lbl_datastream_var)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_x = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_x.setObjectName("lbl_x")
        self.gridLayout.addWidget(self.lbl_x, 0, 0, 1, 1)
        self.lbl_y = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_y.setObjectName("lbl_y")
        self.gridLayout.addWidget(self.lbl_y, 1, 0, 1, 1)
        self.tbox_x_stream = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_x_stream.setObjectName("tbox_x_stream")
        self.gridLayout.addWidget(self.tbox_x_stream, 0, 1, 1, 1)
        self.tbox_y_stream = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_y_stream.setObjectName("tbox_y_stream")
        self.gridLayout.addWidget(self.tbox_y_stream, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.lbl_help = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_help.setObjectName("lbl_help")
        self.verticalLayout.addWidget(self.lbl_help)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_reference = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_reference.setObjectName("lbl_reference")
        self.verticalLayout_2.addWidget(self.lbl_reference)
        #self.btn_add_x = QtWidgets.QPushButton(self.verticalLayoutWidget)
        #self.btn_add_x.setObjectName("btn_add_x")
        #self.verticalLayout_2.addWidget(self.btn_add_x)
        #self.btn_add_y = QtWidgets.QPushButton(self.verticalLayoutWidget)
        #self.btn_add_y.setObjectName("btn_add_y")
        #self.verticalLayout_2.addWidget(self.btn_add_y)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.tbox_datastream_reference = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.tbox_datastream_reference.setMinimumSize(QtCore.QSize(0, 100))
        self.tbox_datastream_reference.setObjectName("tbox_datastream_reference")
        self.horizontalLayout.addWidget(self.tbox_datastream_reference)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.btn_update = QtWidgets.QPushButton(self.centralwidget)
        self.btn_update.setGeometry(QtCore.QRect(530, 264, 80, 16))
        self.btn_update.setObjectName("btn_update")
        dialog_plot_var.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(dialog_plot_var)
        self.statusbar.setObjectName("statusbar")
        dialog_plot_var.setStatusBar(self.statusbar)

        self.retranslateUi(dialog_plot_var)
        QtCore.QMetaObject.connectSlotsByName(dialog_plot_var)
        
        # populate reference
        self.tbox_datastream_reference.setReadOnly(True)
        data = plotter.grabData(self.mainWindow.range_type, self.mainWindow.range_values, self.mainWindow.beamline, self.mainWindow.directory, self.mainWindow.equip)
        ref_str = ''
        for key in data:
                ref_str += "self.data['%s'] \n" %key

        self.tbox_datastream_reference.setText(ref_str)
        
        # linking signals to slots
        self.btn_update.clicked.connect(self.update)
        
###############################################################################################
# ui class functions
###############################################################################################

    def update(self):
        ''' update plot with new datastream variables '''
        
        # update plot
        self.mainWindow.refresh_plot = False
        self.mainWindow.update_plot()
        self.mainWindow.update_labels()


        # designer generated function
    def retranslateUi(self, dialog_plot_var):
        _translate = QtCore.QCoreApplication.translate
        dialog_plot_var.setWindowTitle(_translate("dialog_plot_var", "dialog_plot_var"))
        self.lbl_datastream_var.setText(_translate("dialog_plot_var", "Datastream variables"))
        self.lbl_x.setText(_translate("dialog_plot_var", "x"))
        self.lbl_y.setText(_translate("dialog_plot_var", "y"))
        self.lbl_help.setText(_translate("dialog_plot_var", "Use reference below to populate x and y fields with python code."))
        self.lbl_reference.setText(_translate("dialog_plot_var", "reference"))
        #self.btn_add_x.setText(_translate("dialog_plot_var", "add to x"))
        #self.btn_add_y.setText(_translate("dialog_plot_var", "add to y"))
        self.btn_update.setText(_translate("dialog_plot_var", "update"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Plot = QtWidgets.QMainWindow()
    ui = Ui_dialog_plot_var()
    ui.setupUi(Plot)
    Plot.show()
    sys.exit(app.exec_())

