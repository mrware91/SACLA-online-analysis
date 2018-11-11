import os

os.environ['dropboxPath'] = '../Dropbox'
import time

import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, os.environ['dropboxPath'] + '/Code/mattsTools')
from plotStyles import *


from PyQt5 import QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import random

# define function that updates figure options
def set_figOpts():
	figOpts = { 'xLims':xLims , 'yLims':yLims , 'nxTicks':nxTicks , 'nyTicks':nyTicks , 'xLabel':xLabel , 'yLabel':yLabel , 'newFigure':newFigure }

	figOptsColor = { 'xLims':xLims , 'yLims':yLims , 'zLims':zLims , 'nxTicks':nxTicks , 'nyTicks':nyTicks , 'nzTicks':nzTicks , 'xLabel':xLabel , 'yLabel':yLabel , 'zLabel':zLabel , 'newFigure':newFigure }

	return(figOpts,figOptsColor)

# initialize plot settings
title = 'test title'
xLims, yLims, zLims = [None,None], [None,None], [None,None]
nxTicks, nyTicks, nzTicks = 5, 5, 5
xLabel, yLabel, zLabel = '$x$', '$y$', '$z$'
newFigure = True

figOpts, figOptsColor = set_figOpts()

# initialize figure with junk data
x = np.linspace(0,1,10)
y = x**2
linePlot(x, y, **figOpts)
plt.title(title)
newFigure = False

class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

	# Variables
	#self.X = ....

        # a figure instance to plot on
        self.figure = plt.gcf()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(plt.gcf())

        # just some button connected to `plot` method
        self.btn_plot = QtWidgets.QPushButton('Plot')
        self.btn_capture = QtWidgets.QPushButton('Capture')

	# textboxes
	self.tbox_capture = QtWidgets.QLineEdit(self)
	self.tbox_run = QtWidgets.QLineEdit(self)
	#self.tbox_evt_min = QtWidgets.QLineEdit(self)
	#self.tbox_evt_max = QtWidgets.QLineEdit(self)
	#self.tbox_x_min = QtWidgets.QLineEdit(self)
	#self.tbox_x_max = QtWidgets.QLineEdit(self)
	#self.tbox_x_var_name = QtWidgets.QLineEdit(self)
	#self.tbox_y_min = QtWidgets.QLineEdit(self)
	#self.tbox_y_max = QtWidgets.QLineEdit(self)
	#self.tbox_y_var_name = QtWidgets.QLineEdit(self)
	#self.tbox_z_min = QtWidgets.QLineEdit(self)
	#self.tbox_z_max = QtWidgets.QLineEdit(self)
	#self.tbox_z_var_name = QtWidgets.QLineEdit(self)
	
	# connect buttons
        self.btn_plot.clicked.connect(self.plot)
        self.btn_capture.clicked.connect(self.capture)
        self.btn_capture.clicked.connect(self.capture)
	
        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.btn_plot)
        layout.addWidget(self.btn_capture)
	layout.addWidget(self.tbox_capture)
	layout.addWidget(self.tbox_run)
	#layout.addWidget(self.tbox_evt_min)
	#layout.addWidget(self.tbox_evt_max)
	#layout.addWidget(self.tbox_x_min)
	#layout.addWidget(self.tbox_x_max)
	#layout.addWidget(self.tbox_x_var_name)
	#layout.addWidget(self.tbox_y_min)
	#layout.addWidget(self.tbox_y_max)
	#layout.addWidget(self.tbox_y_var_name)
	#layout.addWidget(self.tbox_z_min)
	#layout.addWidget(self.tbox_z_max)
	#layout.addWidget(self.tbox_z_var_name)
        self.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''

	# store textbox inputs
	run        = self.tbox_run.text()
	#evt_min    = self.tbox_evt_min.text()
	#evt_max    = self.tbox_evt_max.text()
	#xLims[0]   = self.tbox_x_min.text()
	#xLims[1]   = self.tbox_x_max.text()
	#x_var_name = self.tbox_x_var_name.text()
	#yLims[0]   = self.tbox_y_min.text()
	#yLims[1]   = self.tbox_y_max.text()
	#y_var_name = self.tbox_y_var_name.text()
	#zLims[0]   = self.tbox_z_min.text()
	#zLims[1]   = self.tbox_z_max.text()
	#z_var_name = self.tbox_z_var_name.text()
	
	# set new figure options
	figOpts, figOptsColor = set_figOpts()

        # random data
        data = [random.random() for i in range(10)]
	data = np.array(data)

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()
        resetLineCycler()

        # plot data
        linePlot(x*2, data, **figOpts)
	plt.title(str(run))

        # refresh canvas
        self.canvas.draw()

    def capture(self):
	'''save the plot'''
	# create file names
	temp1 = xLabel
	temp2 = yLabel
	temp3 = time.time() % 10**6
	temp3 = str(int(temp3))

	plot_name = '../Logs/pictures/'
	plot_name += 'x-' + temp1 + '_y-' + temp2 + '_time-' + temp3
	
	plot_name_fig = plot_name + '.eps'
	plot_name_scrshot = plot_name + '.png'

	# save figure as eps using mattsTools, use PyQt5 to grab screenshot of GUI
	savefig( plot_name_fig )
	self.grab().save(plot_name_scrshot,'PNG')
	
	# notify of capture
	self.tbox_capture.setText('captured! - filename: ' + plot_name)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
