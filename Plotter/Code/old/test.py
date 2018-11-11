# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_xy_var.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(624, 779)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 290, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 371, 277))
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
        self.tbox_x_stream = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.tbox_x_stream.setObjectName("tbox_x_stream")
        self.gridLayout.addWidget(self.tbox_x_stream, 0, 1, 1, 1)
        self.tbox_y_stream = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.tbox_y_stream.setObjectName("tbox_y_stream")
        self.gridLayout.addWidget(self.tbox_y_stream, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_reference = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_reference.setObjectName("lbl_reference")
        self.horizontalLayout.addWidget(self.lbl_reference)
        self.listView_datastream_reference = QtWidgets.QListView(self.verticalLayoutWidget)
        self.listView_datastream_reference.setObjectName("listView_datastream_reference")
        self.horizontalLayout.addWidget(self.listView_datastream_reference)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbl_datastream_var.setText(_translate("Dialog", "Datastream variables"))
        self.lbl_x.setText(_translate("Dialog", "x"))
        self.lbl_y.setText(_translate("Dialog", "y"))
        self.label.setText(_translate("Dialog", "TextLabel"))
        self.lbl_reference.setText(_translate("Dialog", "reference"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Plot = QtWidgets.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(Plot)
    Plot.show()
    sys.exit(app.exec_())

