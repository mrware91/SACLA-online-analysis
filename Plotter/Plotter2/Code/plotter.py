# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotter.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import dialog_plot_var as dialog_plot_var_window
import dialog_filter as dialog_filter_window
import dialog_filter_onoff as dialog_filter_onoff_window
import os

os.environ['dropboxPath'] = '../../Dropbox'
import time

import numpy as np
import matplotlib.pyplot as plt
import threading

import sys
sys.path.append('/home/software/SACLA_tool/local/python3.5/lib/python3.5/site-packages')
sys.path.insert(0, os.environ['dropboxPath'] + '/Code/mattsTools')
from plotStyles import *

sys.path.insert(0, '../../dataSaverLoader/')
import socket
host_name = socket.gethostname()
if 'hpc' in host_name:
        import dummyDatabase as Database
else:        
        import Database

from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import random

# initialize plot settings
title_str = 'Junk data.  Update to grab data.'
xLims, yLims, zLims = [None,None], [None,None], [None,None]
nxTicks, nyTicks, nzTicks = 5, 5, 5
xLabel, yLabel, zLabel = '', '', ''
xUnits, yUnits, zUnits = '', '', ''

figOpts = { 'dpi':70 , 'xIn':2.9 , 'yIn':2 , 'xLims':xLims , 'yLims':yLims , 'nxTicks':nxTicks , 'nyTicks':nyTicks , 'xLabel':xLabel , 'yLabel':yLabel , 'xUnits':xUnits , 'yUnits':yUnits }

figOptsColor = { 'dpi':70 , 'xIn':2.9 , 'yIn':2 , 'xLims':xLims , 'yLims':yLims , 'zLims':zLims , 'nxTicks':nxTicks , 'nyTicks':nyTicks , 'nzTicks':nzTicks , 'xLabel':xLabel , 'yLabel':yLabel , 'zLabel':zLabel , 'xUnits':xUnits , 'yUnits':yUnits , 'zUnits':zUnits }

# initialize figure with junk data
x_temp = np.linspace(0,1,100)
y_temp = x_temp**2
linePlot(x_temp, y_temp, **figOpts)
plt.title(title_str)


#figOpts['xIn'], figOptsColor['xIn'] = 8.0, 8.0
#figOpts['yIn'], figOptsColor['yIn'] = 4.2, 4.2
#figOpts['dpi'], figOptsColor['dpi'] = 70, 70

###############################################################################################
# define useful functions
###############################################################################################

# check if string is float
def is_number(num):
        try:
                float(num)
                return True
        except ValueError:
                return False

# read floats from textbox
def tbox_num_get(tbox):
        num = tbox.text()
        if len(num) == 0:
                return None
        elif is_number(num):
                return float(tbox.text())
        else:
                print('not a number, defaulting to None')
                return None

# replace None with 0, returns int
def none_to_int_0(num):
        if num is None:
                return 0
        else:
                return int(num)

# make lims [None,None] if one is None
def checkLims(lims):
        if (lims[0] is None) or (lims[1] is None):
                return [None,None]
        else:
                return lims


# grab data
def grabData(range_type, range_values, beamline, directory, equip):
        try:        
                if range_type == 'events':
                        data = Database.loadData(range_values[0], range_values[1], directory)

                elif range_type == 'run':
                        print(beamline)
                        print(range_values)
                        data = Database.loadRunData(int(beamline), int(range_values), directory)

                elif range_type == 'live':
                        data = Database.loadLiveData(range_values, directory, equip)

                else:
                        data = Database.loadJunkData(0,0,0)

        except Exception as e:
                print(str(e))
                data = Database.loadJunkData(0,0,0)

        return data

###############################################################################################
# live plotter thread
###############################################################################################

class livePlotterThread(QtCore.QThread):
        def __init__(self, theUI):
                #threading.Thread.__init__(self)
                QtCore.QThread.__init__(self)
                
                self.UI   = theUI
                self.stop = False  
     
        def run(self):
                while self.stop is not True:
                        self.UI.update_plot_instance()
                        time.sleep(2)
                self.UI = None

        def requestStop(self):
                self.stop = True

        def __del__(self):
                self.wait()
                
###############################################################################################
# define ui
###############################################################################################

class Ui_Plot(object):
    def setupUi(self, Plot):
        Plot.setObjectName("Plot")
        Plot.resize(602, 832)
        # a figure instance to plot on
        self.figure = plt.gcf()

        # this is the Canvas Widget that displays the `figure`
        self.canvas = FigureCanvas(plt.gcf())

	# designer generated code
        self.centralwidget = QtWidgets.QWidget(Plot)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 330, 581, 321))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_run_event = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_run_event.setObjectName("lbl_run_event")
        self.gridLayout.addWidget(self.lbl_run_event, 0, 0, 1, 1)
        self.lbl_axis_units = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_axis_units.setObjectName("lbl_axis_units")
        self.gridLayout.addWidget(self.lbl_axis_units, 0, 15, 1, 1)
        self.tbox_c_axis_units = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_c_axis_units.setObjectName("tbox_c_axis_units")
        self.gridLayout.addWidget(self.tbox_c_axis_units, 4, 15, 1, 1)
        self.line_38 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_38.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_38.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_38.setObjectName("line_38")
        self.gridLayout.addWidget(self.line_38, 3, 14, 1, 1)
        self.tbox_min_event = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_min_event.setObjectName("tbox_min_event")
        self.gridLayout.addWidget(self.tbox_min_event, 2, 1, 1, 1)
        self.line_18 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_18.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_18.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_18.setObjectName("line_18")
        self.gridLayout.addWidget(self.line_18, 4, 8, 1, 1)
        self.lbl_min_event = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_min_event.setObjectName("lbl_min_event")
        self.gridLayout.addWidget(self.lbl_min_event, 2, 0, 1, 1)
        self.lbl_run = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_run.setObjectName("lbl_run")
        self.gridLayout.addWidget(self.lbl_run, 1, 0, 1, 1)
        self.line_9 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.gridLayout.addWidget(self.line_9, 1, 7, 1, 1)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 4, 1, 1)
        self.lbl_c = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_c.setObjectName("lbl_c")
        self.gridLayout.addWidget(self.lbl_c, 4, 5, 1, 1)
        self.lbl_y = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_y.setObjectName("lbl_y")
        self.gridLayout.addWidget(self.lbl_y, 3, 5, 1, 1)
        self.line_20 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_20.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_20.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_20.setObjectName("line_20")
        self.gridLayout.addWidget(self.line_20, 0, 12, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 2, 4, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout.addWidget(self.line_5, 3, 4, 1, 1)
        self.line_21 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_21.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_21.setObjectName("line_21")
        self.gridLayout.addWidget(self.line_21, 1, 9, 1, 1)
        self.line_6 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout.addWidget(self.line_6, 4, 4, 1, 1)
        self.line_28 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_28.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_28.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_28.setObjectName("line_28")
        self.gridLayout.addWidget(self.line_28, 4, 12, 1, 1)
        self.line_19 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_19.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_19.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_19.setObjectName("line_19")
        self.gridLayout.addWidget(self.line_19, 0, 10, 1, 1)
        self.line_13 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_13.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        self.gridLayout.addWidget(self.line_13, 4, 6, 1, 1)
        self.lbl_x = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_x.setObjectName("lbl_x")
        self.gridLayout.addWidget(self.lbl_x, 2, 5, 1, 1)
        self.line_8 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.gridLayout.addWidget(self.line_8, 1, 6, 1, 1)
        self.line_7 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridLayout.addWidget(self.line_7, 1, 5, 1, 1)
        self.line_11 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_11.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.gridLayout.addWidget(self.line_11, 2, 6, 1, 1)
        self.line_14 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_14.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        self.gridLayout.addWidget(self.line_14, 0, 8, 1, 1)
        self.line_10 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_10.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.gridLayout.addWidget(self.line_10, 0, 6, 1, 1)
        self.lbl_min = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_min.setObjectName("lbl_min")
        self.gridLayout.addWidget(self.lbl_min, 0, 7, 1, 1)
        self.line_12 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_12.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.gridLayout.addWidget(self.line_12, 3, 6, 1, 1)
        self.line_15 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_15.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.gridLayout.addWidget(self.line_15, 1, 8, 1, 1)
        self.lbl_max = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_max.setObjectName("lbl_max")
        self.gridLayout.addWidget(self.lbl_max, 0, 9, 1, 1)
        self.line_17 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_17.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_17.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_17.setObjectName("line_17")
        self.gridLayout.addWidget(self.line_17, 3, 8, 1, 1)
        self.lbl_axis_labels = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_axis_labels.setObjectName("lbl_axis_labels")
        self.gridLayout.addWidget(self.lbl_axis_labels, 0, 13, 1, 1)
        self.line_23 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_23.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_23.setObjectName("line_23")
        self.gridLayout.addWidget(self.line_23, 1, 13, 1, 1)
        self.line_22 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_22.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_22.setObjectName("line_22")
        self.gridLayout.addWidget(self.line_22, 1, 11, 1, 1)
        self.lbl_num_ticks = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_num_ticks.setObjectName("lbl_num_ticks")
        self.gridLayout.addWidget(self.lbl_num_ticks, 0, 11, 1, 1)
        self.line_24 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_24.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_24.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_24.setObjectName("line_24")
        self.gridLayout.addWidget(self.line_24, 1, 10, 1, 1)
        self.line_26 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_26.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_26.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_26.setObjectName("line_26")
        self.gridLayout.addWidget(self.line_26, 3, 10, 1, 1)
        self.line_25 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_25.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_25.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_25.setObjectName("line_25")
        self.gridLayout.addWidget(self.line_25, 2, 10, 1, 1)
        self.line_27 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_27.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_27.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_27.setObjectName("line_27")
        self.gridLayout.addWidget(self.line_27, 4, 10, 1, 1)
        self.line_31 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_31.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_31.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_31.setObjectName("line_31")
        self.gridLayout.addWidget(self.line_31, 1, 12, 1, 1)
        self.line_29 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_29.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_29.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_29.setObjectName("line_29")
        self.gridLayout.addWidget(self.line_29, 3, 12, 1, 1)
        self.line_30 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_30.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_30.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_30.setObjectName("line_30")
        self.gridLayout.addWidget(self.line_30, 2, 12, 1, 1)
        self.spinBox_x_num_ticks = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_x_num_ticks.setObjectName("spinBox_x_num_ticks")
        self.spinBox_x_num_ticks.setMinimum(1)
        self.gridLayout.addWidget(self.spinBox_x_num_ticks, 2, 11, 1, 1)
        self.spinBox_z_num_ticks = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_z_num_ticks.setObjectName("spinBox_z_num_ticks")
        self.spinBox_z_num_ticks.setMinimum(1)
        self.gridLayout.addWidget(self.spinBox_z_num_ticks, 4, 11, 1, 1)
        self.spinBox_y_num_ticks = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_y_num_ticks.setObjectName("spinBox_y_num_ticks")
        self.spinBox_y_num_ticks.setMinimum(1)
        self.gridLayout.addWidget(self.spinBox_y_num_ticks, 3, 11, 1, 1)
        self.tbox_x_max = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_x_max.setObjectName("tbox_x_max")
        self.gridLayout.addWidget(self.tbox_x_max, 2, 9, 1, 1)
        self.tbox_x_min = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_x_min.setObjectName("tbox_x_min")
        self.gridLayout.addWidget(self.tbox_x_min, 2, 7, 1, 1)
        self.tbox_y_min = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_y_min.setObjectName("tbox_y_min")
        self.gridLayout.addWidget(self.tbox_y_min, 3, 7, 1, 1)
        self.tbox_c_min = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_c_min.setObjectName("tbox_c_min")
        self.gridLayout.addWidget(self.tbox_c_min, 4, 7, 1, 1)
        self.tbox_x_axis_labels = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_x_axis_labels.setObjectName("tbox_x_axis_labels")
        self.gridLayout.addWidget(self.tbox_x_axis_labels, 2, 13, 1, 1)
        self.lbl_live = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_live.setObjectName("lbl_live")
        self.gridLayout.addWidget(self.lbl_live, 4, 0, 1, 1)
        self.tbox_c_max = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_c_max.setObjectName("tbox_c_max")
        self.gridLayout.addWidget(self.tbox_c_max, 4, 9, 1, 1)
        self.tbox_y_max = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_y_max.setObjectName("tbox_y_max")
        self.gridLayout.addWidget(self.tbox_y_max, 3, 9, 1, 1)
        self.tbox_y_axis_labels = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_y_axis_labels.setObjectName("tbox_y_axis_labels")
        self.gridLayout.addWidget(self.tbox_y_axis_labels, 3, 13, 1, 1)
        self.tbox_c_axis_labels = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_c_axis_labels.setObjectName("tbox_c_axis_labels")
        self.gridLayout.addWidget(self.tbox_c_axis_labels, 4, 13, 1, 1)
        self.tbox_max_event = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_max_event.setObjectName("tbox_max_event")
        self.gridLayout.addWidget(self.tbox_max_event, 3, 1, 1, 1)
        self.lbl_max_event = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_max_event.setObjectName("lbl_max_event")
        self.gridLayout.addWidget(self.lbl_max_event, 3, 0, 1, 1)
        self.line_39 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_39.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_39.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_39.setObjectName("line_39")
        self.gridLayout.addWidget(self.line_39, 2, 14, 1, 1)
        self.line_41 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_41.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_41.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_41.setObjectName("line_41")
        self.gridLayout.addWidget(self.line_41, 0, 14, 1, 1)
        self.comboBox_run_event = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_run_event.setObjectName("comboBox_run_event")
        self.comboBox_run_event.addItem("")
        self.comboBox_run_event.addItem("")
        self.comboBox_run_event.addItem("")
        self.gridLayout.addWidget(self.comboBox_run_event, 0, 1, 1, 1)
        self.line_16 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_16.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")
        self.gridLayout.addWidget(self.line_16, 2, 8, 1, 1)
        self.line_42 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_42.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_42.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_42.setObjectName("line_42")
        self.gridLayout.addWidget(self.line_42, 4, 14, 1, 1)
        self.tbox_y_axis_units = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_y_axis_units.setObjectName("tbox_y_axis_units")
        self.gridLayout.addWidget(self.tbox_y_axis_units, 3, 15, 1, 1)
        self.line_43 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_43.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_43.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_43.setObjectName("line_43")
        self.gridLayout.addWidget(self.line_43, 1, 15, 1, 1)
        self.tbox_x_axis_units = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_x_axis_units.setObjectName("tbox_x_axis_units")
        self.gridLayout.addWidget(self.tbox_x_axis_units, 2, 15, 1, 1)
        self.line_40 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_40.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_40.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_40.setObjectName("line_40")
        self.gridLayout.addWidget(self.line_40, 1, 14, 1, 1)
        self.tbox_num_shots_live = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_num_shots_live.setObjectName("tbox_num_shots_live")
        self.gridLayout.addWidget(self.tbox_num_shots_live, 4, 1, 1, 1)
        self.tbox_run = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.tbox_run.setObjectName("tbox_run")
        self.gridLayout.addWidget(self.tbox_run, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line_2 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.radioBtn_histogram = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioBtn_histogram.setObjectName("radioBtn_histogram")
        self.gridLayout_3.addWidget(self.radioBtn_histogram, 2, 0, 1, 1)
        self.radioBtn_color = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioBtn_color.setObjectName("radioBtn_color")
        self.gridLayout_3.addWidget(self.radioBtn_color, 3, 0, 1, 1)
        self.radioBtn_scatter = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioBtn_scatter.setObjectName("radioBtn_scatter")
        self.gridLayout_3.addWidget(self.radioBtn_scatter, 1, 0, 1, 1)
        self.checkBox_subtraction = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_subtraction.setObjectName("checkBox_subtraction")
        self.gridLayout_3.addWidget(self.checkBox_subtraction, 2, 2, 1, 1)
        self.lbl_plot_type = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_plot_type.setObjectName("lbl_plot_type")
        self.gridLayout_3.addWidget(self.lbl_plot_type, 0, 0, 1, 1)
        self.btn_set_filter_onoff = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_set_filter_onoff.setObjectName("btn_set_filter_onoff")
        self.gridLayout_3.addWidget(self.btn_set_filter_onoff, 3, 2, 1, 1)
        self.btn_set_filters = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_set_filters.setObjectName("btn_set_filters")
        self.gridLayout_3.addWidget(self.btn_set_filters, 1, 2, 1, 1)
        self.line_34 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_34.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_34.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_34.setObjectName("line_34")
        self.gridLayout_3.addWidget(self.line_34, 3, 1, 1, 1)
        self.line_35 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_35.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_35.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_35.setObjectName("line_35")
        self.gridLayout_3.addWidget(self.line_35, 2, 1, 1, 1)
        self.line_32 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_32.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_32.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_32.setObjectName("line_32")
        self.gridLayout_3.addWidget(self.line_32, 1, 1, 1, 1)
        self.btn_set_plot_var = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_set_plot_var.setObjectName("btn_set_plot_var")
        self.gridLayout_3.addWidget(self.btn_set_plot_var, 0, 2, 1, 1)
        self.line_33 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_33.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_33.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_33.setObjectName("line_33")
        self.gridLayout_3.addWidget(self.line_33, 0, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_3)
        self.line_36 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_36.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_36.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_36.setObjectName("line_36")
        self.horizontalLayout_2.addWidget(self.line_36)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_current_plot_var = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_current_plot_var.setObjectName("lbl_current_plot_var")
        self.verticalLayout_2.addWidget(self.lbl_current_plot_var)
        self.lbl_current_filters = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_current_filters.setObjectName("lbl_current_filters")
        self.verticalLayout_2.addWidget(self.lbl_current_filters)
        self.lbl_current_filter_onoff = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_current_filter_onoff.setObjectName("lbl_current_filter_onoff")
        self.verticalLayout_2.addWidget(self.lbl_current_filter_onoff)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line_3 = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.btn_run = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_run.setObjectName("btn_run")
        self.verticalLayout.addWidget(self.btn_run)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_capture = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_capture.setObjectName("btn_capture")
        self.horizontalLayout.addWidget(self.btn_capture)
        self.lbl_captured_filename = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_captured_filename.setObjectName("lbl_captured_filename")
        self.horizontalLayout.addWidget(self.lbl_captured_filename)
        self.verticalLayout.addLayout(self.horizontalLayout)

        # add widgets
        self.lbl_beamline = QtWidgets.QLabel(self.centralwidget)
        self.lbl_beamline.setGeometry(QtCore.QRect(10, 660, 120, 20))
        self.lbl_beamline.setObjectName("lbl_beamline")

        self.tbox_beamline = QtWidgets.QLineEdit(self.centralwidget)
        self.tbox_beamline.setGeometry(QtCore.QRect(130, 660, 20, 20))
        self.tbox_beamline.setObjectName("tbox_beamline")

        self.lbl_database_directory = QtWidgets.QLabel(self.centralwidget)
        self.lbl_database_directory.setGeometry(QtCore.QRect(160, 660, 70, 20))
        self.lbl_database_directory.setObjectName("lbl_database_directory")

        self.tbox_database_directory = QtWidgets.QLineEdit(self.centralwidget)
        self.tbox_database_directory.setGeometry(QtCore.QRect(220, 660, 371, 20))
        self.tbox_database_directory.setObjectName("tbox_database_directory")

        self.lbl_equip = QtWidgets.QLabel(self.centralwidget)
        self.lbl_equip.setGeometry(QtCore.QRect(10, 685, 50, 20))
        self.lbl_equip.setObjectName("lbl_equip")

        self.tbox_equip = QtWidgets.QLineEdit(self.centralwidget)
        self.tbox_equip.setGeometry(QtCore.QRect(60, 685, 271, 20))
        self.tbox_equip.setObjectName("tbox_equip")

        self.btn_stop_live = QtWidgets.QPushButton(self.centralwidget)
        self.btn_stop_live.setGeometry(QtCore.QRect(10, 710, 291, 20))
        self.btn_stop_live.setObjectName("btn_stop_live")

        self.btn_default = QtWidgets.QPushButton(self.centralwidget)
        self.btn_default.setGeometry(QtCore.QRect(340, 685, 150, 20))
        self.btn_default.setObjectName("btn_default")

        self.lbl_error = QtWidgets.QLabel(self.centralwidget)
        self.lbl_error.setGeometry(QtCore.QRect(320, 710, 100, 20))
        self.lbl_error.setObjectName("lbl_error")

        self.lbl_names = QtWidgets.QLabel(self.centralwidget)
        self.lbl_names.setGeometry(QtCore.QRect(10, 745, 581, 50))
        self.lbl_names.setObjectName("lbl_names")

        #self.lbl_error = QtWidgets.QLabel(self.centralwidget)
        #self.lbl_error.setGeometry(QtCore.QRect(10, 665, 50, 20))
        #self.lbl_error.setObjectName("lbl_equip")
        
###############################################################################################
# initialize window
###############################################################################################

        # initialize values
        self.liveThread = None
        self.tbox_beamline.setText('3')
        self.tbox_database_directory.setText('/home/mrware/ANAPC/online/dataSaverLoader/smallData')
        self.tbox_equip.setText('xfel_bl_3_tc_bm_2_pd/charge')
        self.is_live = False
        self.refresh_plot = True
        self.need_default_title = False

        self.beamline = int( self.tbox_beamline.text() )
        self.directory = self.tbox_database_directory.text()
        self.equip = self.tbox_equip.text()
        self.range_type = 'live'
        self.range_values = 1
        self.filter_mask = None
        self.filter_off_mask = None
        self.no_x = False
        self.plot_x = x_temp
        self.plot_y = y_temp
        self.filt_x = None
        self.filt_y = None
        self.filt_off_x = None
        self.filt_off_y = None
        self.error_code = ''
        self.data = grabData('run', 1, self.beamline, self.directory, self.equip)
        self.radioBtn_histogram.setChecked(True)
        self.spinBox_x_num_ticks.setValue(5)
        self.spinBox_y_num_ticks.setValue(5)
        self.spinBox_z_num_ticks.setValue(5)
        self.tbox_x_axis_labels.setText('$x$')
        self.tbox_y_axis_labels.setText('$y$')
        self.btn_stop_live.hide()
        self.tbox_num_shots_live.setText('1000')

        # initialize plot settings
        self.title_str = 'Junk data.  Update to grab data.'
        self.xLims, self.yLims, self.zLims = [None,None], [None,None], [None,None]
        self.nxTicks, self.nyTicks, self.nzTicks = 5, 5, 5

	# layout of plot
        self.canvas.setObjectName("canvas")
        self.replace_with_plot = QtWidgets.QWidget(self.centralwidget)
        self.replace_with_plot.setGeometry(QtCore.QRect(10, 10, 581, 289))
        self.replace_with_plot.setObjectName("replace_with_plot")
        self.replace_with_plotLayout = QtWidgets.QVBoxLayout(self.replace_with_plot)
        self.replace_with_plotLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.replace_with_plotLayout.setContentsMargins(0, 0, 0, 0)
        self.replace_with_plotLayout.setObjectName("replace_with_plotLayout")
        self.replace_with_plotLayout.addWidget(self.canvas)

	# more designer generated code
        Plot.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Plot)
        self.statusbar.setObjectName("statusbar")
        Plot.setStatusBar(self.statusbar)

        self.retranslateUi(Plot)
        QtCore.QMetaObject.connectSlotsByName(Plot)

        # setup dialog windows
        self.dialog_plot_var = dialog_plot_var_window.Ui_dialog_plot_var()
        self.dialog_plot_var_window_Plot = QtWidgets.QMainWindow()
        self.dialog_plot_var.setupUi(self.dialog_plot_var_window_Plot, self)

        self.dialog_filter = dialog_filter_window.Ui_dialog_filter()
        self.dialog_filter_window_Plot = QtWidgets.QMainWindow()
        self.dialog_filter.setupUi(self.dialog_filter_window_Plot, self)

        self.dialog_filter_onoff = dialog_filter_onoff_window.Ui_dialog_filter_onoff()
        self.dialog_filter_onoff_window_Plot = QtWidgets.QMainWindow()
        self.dialog_filter_onoff.setupUi(self.dialog_filter_onoff_window_Plot, self)

        # linking signals to slots
        self.btn_run.clicked.connect(self.run_plot)
        self.btn_capture.clicked.connect(self.capture)
        self.btn_set_plot_var.clicked.connect(self.open_dialog_plot_var)
        self.btn_set_filters.clicked.connect(self.open_dialog_filter)
        self.btn_set_filter_onoff.clicked.connect(self.open_dialog_filter_onoff)
        self.btn_stop_live.clicked.connect(self.requestStop)
        self.radioBtn_scatter.clicked.connect(self.update_labels)
        self.radioBtn_histogram.clicked.connect(self.update_labels)
        self.radioBtn_color.clicked.connect(self.update_labels)
        self.btn_default.clicked.connect(self.set_default)

###############################################################################################
# ui class functions
###############################################################################################

    def x_tag_numbers(self):
                try:
                        self.plot_x = self.plot_y.index.values
                        print('default to tag numbers')
                        if self.radioBtn_scatter.isChecked():
                                self.dialog_plot_var.tbox_x_stream.setText('tag numbers')
                except AttributeError:
                        self.plot_x = np.arange(self.plot_y.size)
                        print('default to arange')
                        self.dialog_plot_var.tbox_x_stream.setText('arange')

    def requestStop(self):
        self.btn_stop_live.hide()
        self.is_live = False

    def filt_data(self):
        ''' filter data '''
        # also check for nans
        try:
                nan_filter_mask = np.isnan( np.array(self.plot_x) ) | np.isnan( np.array(self.plot_y) )
        except:
                nan_filter_mask = np.zeros_like(self.plot_x).astype(bool)
                print('nan filter failed')        

        self.filt_x = np.array(self.plot_x[ self.filter_mask & (~nan_filter_mask) ])
        self.filt_y = np.array(self.plot_y[ self.filter_mask & (~nan_filter_mask) ])

        
        if self.checkBox_subtraction.isChecked():
                self.filt_off_x = self.plot_x[ self.filter_off_mask & (~nan_filter_mask) ]
                self.filt_off_y = self.plot_y[ self.filter_off_mask & (~nan_filter_mask) ]

        # plotting functions
    def plot_scatter(self):
        ''' update scatter plot '''
        if self.filt_x.max() - self.filt_x.min() < 1e-10:
            self.filt_x = np.arange( self.filt_y.size ) 


        if figOpts['xLims'][0] is None:
            figOpts['xLims'][0] = self.filt_x.min()

        if figOpts['xLims'][1] is None:
            figOpts['xLims'][1] = self.filt_x.max()

        if figOpts['yLims'][0] is None:
            figOpts['yLims'][0] = self.filt_y.min()

        if figOpts['yLims'][1] is None:
            figOpts['yLims'][1] = self.filt_y.max()
        
        scatterPlot(self.filt_x, self.filt_y, **figOpts)


    def plot_histogram(self):
        ''' update histogram plot '''

        
        if figOpts['xLims'][0] is None:
            figOpts['xLims'][0] = self.filt_x.min()

        if figOpts['xLims'][1] is None:
            figOpts['xLims'][1] = self.filt_x.max()

        #if figOpts['yLims'][0] is None:
        #    figOpts['yLims'][0] = self.filt_y.min()

        #if figOpts['yLims'][1] is None:
        #    figOpts['yLims'][1] = self.filt_y.max()




        if self.no_x:
                if np.any(self.xLims) == None:
                        data, bins_x = np.histogram(self.filt_y, self.nxTicks)
                else:
                        data, bins_x = np.histogram(self.filt_y, self.nxTicks, tuple(self.xLims))
        
                if self.checkBox_subtraction.isChecked():
                        data_off = np.histogram(self.filt_y, bins_x)
                        
                        data = data - data_off

                dx = bins_x[1] - bins_x[0]
                bins_x = bins_x[:-1] + dx/2
        else:
                if np.any(self.xLims) == None:
                        self.xLims[0] = self.filt_x.min()
                        self.xLims[1] = self.filt_x.max()

                dx = (self.xLims[1]-self.xLims[0])/self.nxTicks
                bins_x = np.linspace( self.xLims[0] ,self.xLims[1] + dx, self.nxTicks+1 )

                inds = np.digitize(self.filt_x, bins_x)-1
                data = np.zeros_like(bins_x)
                count = np.zeros_like(bins_x)

                for ind, yf in zip(inds , self.filt_y):
                        data[ind] += yf 
                        count[ind] += 1

                data = data / count
                data[ np.isnan(data) ] = 0.

                if self.checkBox_subtraction.isChecked():

                        inds_off = np.digitize(self.filt_off_x, bins_x)-1
                        data_off = np.zeros_like(bins_x)
                        count_off = np.zeros_like(bins_x)

                        for ind, yf in zip(inds_off , self.filt_off_y):
                                data_off[ind] += yf 
                                count_off[ind] += 1

                        data_off = data_off / count_off
                        data_off[ np.isnan(data_off) ] = 0.
                        
                        data = data - data_off

        linePlot(bins_x, data, **figOpts)


    def plot_color(self):
        ''' update color plot '''
        if (np.any(self.xLims) == None) and (np.any(self.yLims) == None):
                data, bins_x, bins_y = np.histogram2d( self.filt_x, self.filt_y, [self.nxTicks, self.nyTicks] )

        elif np.any(self.xLims) == None:
                print('y lims')
                xLims_temp = [ np.min(self.filt_x), np.max(self.filt_x) ]
                print(xLims_temp)
                print(self.yLims)
                data, bins_x, bins_y = np.histogram2d( self.filt_x, self.filt_y, [self.nxTicks, self.nyTicks], [xLims_temp, self.yLims] )
                
        elif np.any(self.yLims) == None:
                print('x lims')
                yLims_temp = [ np.min(self.filt_y), np.max(self.filt_y) ]
                print(yLims_temp)
                print(self.xLims)
                data, bins_x, bins_y = np.histogram2d( self.filt_x, self.filt_y, [self.nxTicks, self.nyTicks], [self.xLims, yLims_temp] )
                
        else:
                print('x and y lims')
                data, bins_x, bins_y = np.histogram2d( self.filt_x, self.filt_y, [self.nxTicks, self.nyTicks], [self.xLims, self.yLims] )
                print(data.shape)
        
        if self.checkBox_subtraction.isChecked():
                data_off = np.histogram2d( self.filt_x, self.filt_y, bins_x, bins_y)
                
                data = data - data_off

        dx = bins_x[1] - bins_x[0]
        xc = bins_x[:-1] + dx/2.

        dy = bins_y[1] - bins_y[0]
        yc = bins_y[:-1] + dy/2.

        colorPlot(xc,yc, data.T, **figOptsColor)


        # get data range
    def getRange(self):
        ''' get data range '''
        if self.range_type == 'run':
                range_values = none_to_int_0( tbox_num_get(self.tbox_run) )
                title_str = 'run %d' %range_values

        elif self.range_type == 'events':
                range_values = [0,0]
                range_values[0] = none_to_int_0( tbox_num_get(self.tbox_min_event) ) 
                range_values[1] = none_to_int_0( tbox_num_get(self.tbox_max_event) )
                title_str = 'events %d to %d' %(range_values[0],range_values[1]) 

        elif self.range_type == 'live':
                range_values = none_to_int_0( tbox_num_get(self.tbox_num_shots_live) )
                title_str = 'live, %d events' %range_values

        return range_values, title_str


    def refresh_reference(self):
        ''' update datastream reference in dialog boxes '''

        data = grabData(self.range_type, self.range_values, self.beamline, self.directory, self.equip)
        ref_str = ''
        for key in data.keys():
                ref_str += "self.data['%s'] \n" %key

        self.dialog_plot_var.tbox_datastream_reference.setText(ref_str)
        self.dialog_filter.tbox_datastream_reference.setText(ref_str)
        self.dialog_filter_onoff.tbox_datastream_reference.setText(ref_str)


        # open dialog functions
    def open_dialog_plot_var(self):
        ''' open dialog box to define plot variables '''
        self.refresh_reference()
        self.dialog_plot_var_window_Plot.show()


    def open_dialog_filter(self):
        ''' open dialog box to define filter '''
        self.refresh_reference()
        self.dialog_filter_window_Plot.show()

        
    def open_dialog_filter_onoff(self):
        ''' open dialog box to define filter '''
        self.refresh_reference()
        self.dialog_filter_onoff_window_Plot.show()

    def update_labels(self):
        ''' update axis labels '''

        if self.radioBtn_scatter.isChecked():
                if self.no_x:
                        self.tbox_x_axis_labels.setText('tag numbers')
                else:
                        self.tbox_x_axis_labels.setText(self.dialog_plot_var.tbox_x_stream.text())
                self.tbox_y_axis_labels.setText(self.dialog_plot_var.tbox_y_stream.text())
        elif self.radioBtn_histogram.isChecked():
                if self.no_x:
                        self.tbox_x_axis_labels.setText(self.dialog_plot_var.tbox_y_stream.text())
                        self.tbox_y_axis_labels.setText('shots/bin')

                else:
                        self.tbox_x_axis_labels.setText(self.dialog_plot_var.tbox_x_stream.text())
                        self.tbox_y_axis_labels.setText( 'average %s in bin' %self.dialog_plot_var.tbox_y_stream.text() )
        elif self.radioBtn_color.isChecked():
                if self.no_x:
                        self.tbox_x_axis_labels.setText('tag numbers')

                else:
                        self.tbox_x_axis_labels.setText(self.dialog_plot_var.tbox_x_stream.text())
                self.tbox_y_axis_labels.setText(self.dialog_plot_var.tbox_y_stream.text())
                self.tbox_c_axis_labels.setText('shots/bin')

    def set_default(self):
        ''' set all fields to defaults '''

        self.tbox_x_min.setText('')
        self.tbox_y_min.setText('')
        self.tbox_c_min.setText('')
        self.tbox_x_max.setText('')
        self.tbox_y_max.setText('')
        self.tbox_c_max.setText('')
        self.spinBox_x_num_ticks.setValue(5)
        self.spinBox_y_num_ticks.setValue(5)
        self.spinBox_z_num_ticks.setValue(5)

        self.tbox_x_axis_labels.setText('$x$')
        self.tbox_y_axis_labels.setText('$y$')
        self.tbox_c_axis_labels.setText('')
        self.tbox_x_axis_units.setText('')
        self.tbox_y_axis_units.setText('')
        self.tbox_c_axis_units.setText('')

        self.tbox_beamline.setText('3')
        self.tbox_database_directory.setText('/home/mrware/ANAPC/online/dataSaverLoader/smallData')
        self.tbox_equip.setText('xfel_bl_3_tc_bm_2_pd/charge')
        
###############################################################################################
# update data
###############################################################################################
        
    def update_data(self):
        ''' update the data selection and filter data '''

        # update data
        try:
                print(eval(self.dialog_plot_var.tbox_y_stream.text()))
                self.plot_y = eval(self.dialog_plot_var.tbox_y_stream.text()).astype(float)

        except:
                print('error, code in textbox y datastream variable must evaluate to a float')
                self.lbl_error.setText('error, y datastream variable must evaluate to float, replacing with default')
                self.plot_y = y_temp

        try:
                self.plot_x = eval(self.dialog_plot_var.tbox_x_stream.text()).astype(float)
                self.need_default_title = False
                self.no_x = False                
        
        except:
                print('eval failed, defaulting to tag numbers')
                self.need_default_title = False

                try:
                        if np.allclose(self.plot_y, y_temp, 0.01):
                                self.plot_x = x_temp
                                self.dialog_plot_var.tbox_x_stream.setText('default')
                                self.need_default_title = True
                        
                        else:
                                self.x_tag_numbers()
                                self.no_x = True

                except:
                        self.x_tag_numbers()
                        self.no_x = True
        
        # update filters
        try:
                self.filter_mask = eval(self.dialog_filter.tbox_filter.text())
                self.filter_mask.size
        
        except:
                print('filter not boolean mask')
                self.lbl_error.setText('filter not boolean mask')
                self.filter_mask = np.ones_like(self.plot_y)

        if self.filter_mask is None:
                self.filter_mask = np.ones_like(self.plot_y)
        
        elif self.filter_mask.size != self.plot_y.size:
                print('filter inconsistent size')
                self.lbl_error.setText('filter inconsistent size, default to no filter')
                self.filter_mask = np.ones_like(self.plot_y)

        self.filter_mask = np.array(self.filter_mask).astype(bool)

        # update off filter
        try:
                self.filter_off_mask = eval(self.dialog_filter_onoff.tbox_filter_onoff.text())
        
        except:
                print('off filter not boolean mask')
                self.lbl_error.setText('off filter not boolean mask')
                self.filter_off_mask = np.ones_like(self.plot_y)

        if self.filter_off_mask is None:
                self.filter_off_mask = np.ones_like(self.plot_y)
        
        elif self.filter_off_mask.size != self.plot_y.size:
                print('off filter inconsistent size')
                self.lbl_error.setText('off filter inconsistent size, default to no filter')
                self.filter_off_mask = np.ones_like(self.plot_y)

        self.filter_off_mask = np.array(self.filter_off_mask).astype(bool)

###############################################################################################
# update plot
###############################################################################################
        
    def run_plot(self):
        ''' plot new '''
        self.refresh_plot = True
        self.update_plot()
        

    def update_plot(self):
        ''' wrapper for update plot function '''

        # update event info
        self.title_str = ''
        self.range_type = self.comboBox_run_event.currentText()
        self.range_values, self.title_str = self.getRange()
        
        if (self.range_type == 'live') and (self.refresh_plot):
                self.btn_stop_live.show()
                self.is_live = True
                while self.is_live:
                        self.title_str = ''
                        self.range_values, self.title_str = self.getRange()

                        self.update_plot_instance()
                        QtCore.QCoreApplication.processEvents()
                        time.sleep(1)

        else:
                self.requestStop()
                self.update_plot_instance()

###############################################################################################
# load data and figure options
###############################################################################################


    def update_plot_instance(self):
        ''' update plot with event info, figOpts, and random data '''
        
        self.lbl_error.setText('no errors')
        self.refresh_reference()
        
        self.data = grabData(self.range_type, self.range_values, self.beamline, self.directory, self.equip)
        self.update_data()

        # update labels
        self.lbl_current_plot_var.setText( 'current plot_y = ' + self.dialog_plot_var.tbox_y_stream.text() )
        self.lbl_current_filters.setText( 'current ons filter = ' + self.dialog_filter.tbox_filter.text() )
        self.lbl_current_filter_onoff.setText( 'current offs filter = ' + self.dialog_filter_onoff.tbox_filter_onoff.text() )
        self.beamline = int( self.tbox_beamline.text() )
        self.directory = self.tbox_database_directory.text()
        self.equip = self.tbox_equip.text()

        # update figure options
        self.xLims = checkLims( [tbox_num_get(self.tbox_x_min), tbox_num_get(self.tbox_x_max)] )
        self.yLims = checkLims( [tbox_num_get(self.tbox_y_min), tbox_num_get(self.tbox_y_max)] )
        self.zLims = checkLims( [tbox_num_get(self.tbox_c_min), tbox_num_get(self.tbox_c_max)] )


        self.nxTicks = none_to_int_0( self.spinBox_x_num_ticks.value() )
        self.nyTicks = none_to_int_0( self.spinBox_y_num_ticks.value() )
        self.nzTicks = none_to_int_0( self.spinBox_z_num_ticks.value() )

        figOpts['xLims'] = self.xLims
        figOpts['yLims'] = self.yLims
        figOpts['nxTicks'] = self.nxTicks
        figOpts['nyTicks'] = self.nyTicks

        if self.nxTicks > 11: figOpts['nxTicks'] = 11
        if self.nyTicks > 11: figOpts['nyTicks'] = 11
        if self.nxTicks > 11: figOptsColor['nxTicks'] = 11
        if self.nyTicks > 11: figOptsColor['nyTicks'] = 11
        if self.nzTicks > 11: figOptsColor['nzTicks'] = 11

        figOpts['xLabel'] = self.tbox_x_axis_labels.text()
        figOpts['yLabel'] = self.tbox_y_axis_labels.text()
        figOpts['xUnits'] = self.tbox_x_axis_units.text()
        figOpts['yUnits'] = self.tbox_y_axis_units.text()

        figOptsColor['xLims'] = self.xLims
        figOptsColor['yLims'] = self.yLims
        figOptsColor['zLims'] = self.zLims
        figOptsColor['xLabel'] = self.tbox_x_axis_labels.text()
        figOptsColor['yLabel'] = self.tbox_y_axis_labels.text()
        figOptsColor['zLabel'] = self.tbox_c_axis_labels.text()
        figOptsColor['xUnits'] = self.tbox_x_axis_units.text()
        figOptsColor['yUnits'] = self.tbox_y_axis_units.text()
        figOptsColor['zUnits'] = self.tbox_c_axis_units.text()

        # clear plot and draw
        if self.refresh_plot:
                plt.close()
                plt.clf()
                self.canvas.close()
                time.sleep(0.1)

        # refreshes plot        
        if self.plot_y is None:
                print('no data to plot')

        else:
        
                if self.plot_x.size != self.plot_y.size:
                        print('x and y sizes inconsistent, defaulting to no x for histogram and tag numbers for scatter')
                        self.x_tag_numbers()
                        self.no_x = True

                # filter data
                self.filt_data()
                
                try:
                        if self.refresh_plot:
                                if self.radioBtn_scatter.isChecked():
                                        self.plot_scatter()

                                elif self.radioBtn_histogram.isChecked():
                                        self.plot_histogram()

                                elif self.radioBtn_color.isChecked():
                                        self.plot_color()
                                        self.title_str += ', '

                except Exception as e:
                        print('failed to plot with error: '+str(e))
                        self.lbl_error.setText('failed to plot')

        # update canvas with new plot
        if self.refresh_plot:        
                self.title_str += plt.gca().get_title()

                if self.need_default_title:
                        plt.title('Junk data.  Add datastream.')
                else:
                        plt.title(self.title_str)
                self.figure = plt.gcf()
                self.canvas = FigureCanvas(plt.gcf())
                self.canvas.setObjectName("canvas")

                self.replace_with_plotLayout.addWidget(self.canvas)

                self.canvas.figure = plt.gcf()
                self.canvas.draw()
                self.canvas.show()
                time.sleep(0.1)



###############################################################################################
# capture data
###############################################################################################

    def capture(self):
        '''save the plot'''
        # update event info
        self.range_type = self.comboBox_run_event.currentText()
        self.range_values, self.title_str = self.getRange()

        # create file names
        if self.range_type == 'events':
                tags = 'events-%d-%d' %(self.range_values[0],self.range_values[1])
        else:
                tags = self.range_type + '-' + str(self.range_values)
        
        grab_time = time.time() % 10**6
        grab_time = int(grab_time)
        plot_name = '../Logs/pictures/'
        if self.radioBtn_color.isChecked():
                plot_name += 'color__%s_time-%d' %(tags, grab_time)
        elif self.radioBtn_histogram.isChecked():
                plot_name += 'hist_%s_time-%d' %(tags, grab_time)

        plot_name_fig = plot_name + '.eps'
        plot_name_scrshot = plot_name + '.png'

        # save figure as eps using mattsTools, use PyQt5 to grab screenshot of GUI
        savefig( plot_name_fig )
        Plot.grab().save(plot_name_scrshot,'PNG')

        # notify of capture
        self.lbl_captured_filename.setText('captured! - filename: ' + plot_name)
        




        # designer generated function
    def retranslateUi(self, Plot):
        _translate = QtCore.QCoreApplication.translate
        Plot.setWindowTitle(_translate("Plot", "Plotter"))
        self.lbl_run_event.setText(_translate("Plot", "range type"))
        self.lbl_axis_units.setText(_translate("Plot", "axis units"))
        self.lbl_min_event.setText(_translate("Plot", "min event"))
        self.lbl_run.setText(_translate("Plot", "run"))
        self.lbl_c.setText(_translate("Plot", "c"))
        self.lbl_y.setText(_translate("Plot", "y"))
        self.lbl_x.setText(_translate("Plot", "x"))
        self.lbl_min.setText(_translate("Plot", "min"))
        self.lbl_max.setText(_translate("Plot", "max"))
        self.lbl_axis_labels.setText(_translate("Plot", "axis labels"))
        self.lbl_num_ticks.setText(_translate("Plot", "# ticks"))
        self.lbl_live.setText(_translate("Plot", "num shots live"))
        self.lbl_max_event.setText(_translate("Plot", "max event"))
        self.comboBox_run_event.setItemText(1, _translate("Plot", "run"))
        self.comboBox_run_event.setItemText(2, _translate("Plot", "events"))
        self.comboBox_run_event.setItemText(0, _translate("Plot", "live"))
        self.radioBtn_histogram.setText(_translate("Plot", "histogram"))
        self.radioBtn_color.setText(_translate("Plot", "color"))
        self.radioBtn_scatter.setText(_translate("Plot", "scatter"))
        self.checkBox_subtraction.setText(_translate("Plot", "subtract offs?"))
        self.lbl_plot_type.setText(_translate("Plot", "Plot type:"))
        self.btn_set_filter_onoff.setText(_translate("Plot", "set offs filter"))
        self.btn_set_filters.setText(_translate("Plot", "set ons filter"))
        self.btn_set_plot_var.setText(_translate("Plot", "set plot variables"))
        self.lbl_current_plot_var.setText(_translate("Plot", "current plot variables"))
        self.lbl_current_filters.setText(_translate("Plot", "current ons filter"))
        self.lbl_current_filter_onoff.setText(_translate("Plot", "current offs filter"))
        self.btn_run.setText(_translate("Plot", "run"))
        self.btn_capture.setText(_translate("Plot", "capture"))
        self.lbl_captured_filename.setText(_translate("Plot", "captured filename"))
        self.lbl_names.setText(_translate("Plot", "Created by Matt Ware, Jordan O'Neal, Kathryn Ledbetter, and Takahiro Sato\nSee readme for License info."))

        # add new widgets
        self.lbl_beamline.setText(_translate("Plot", "beamline number"))
        self.lbl_database_directory.setText(_translate("Plot", "directory"))
        self.lbl_equip.setText(_translate("Plot", "equip"))
        self.btn_stop_live.setText(_translate("Plot", "stop live"))
        self.btn_default.setText(_translate("Plot", "default plot style"))
        self.lbl_error.setText(_translate("Plot", "no errors"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Plot = QtWidgets.QMainWindow()
    ui = Ui_Plot()
    ui.setupUi(Plot)
    Plot.show()
    sys.exit(app.exec_())

