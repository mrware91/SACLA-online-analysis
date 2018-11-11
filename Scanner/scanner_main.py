import sys
sys.path.insert(0, '../dataSaverLoader/')

import numpy as np
import matplotlib.pyplot as plt

import socket
host_name = socket.gethostname()
if 'hpc' in host_name:
        import dummyDatabase as Database
else:        
        import Database

from PyQt5 import QtCore, QtGui, QtWidgets

import scanner_ui



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = scanner_ui.Ui_Scanner()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

