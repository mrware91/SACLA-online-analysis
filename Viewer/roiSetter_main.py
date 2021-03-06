from PyQt5 import QtCore, QtGui, QtWidgets

import roi_set_ui
import roiSetter_ui
import availableDetectors_ui
from cameraViewer import *

import os

os.environ['dropboxPath'] = '../Dropbox'
import time

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import threading

import sys
sys.path.append('/home/software/SACLA_tool/local/python3.5/lib/python3.5/site-packages')
sys.path.insert(0, os.environ['dropboxPath'] + '/Code/mattsTools')
from plotStyles import *
from picklez import *

sys.path.insert(0, '../dataSaverLoader/')
import socket
host_name = socket.gethostname()
if 'hpc' in host_name:
        from dummyDatabase import *
else:        
        from Database import *


###########################################################################################
# Useful python commands
###########################################################################################
def merge_dictionaries( *args ):
    z = {}
    for arg in args:
        z.update( arg )
    return z




###########################################################################################
# Integrated UIs
###########################################################################################

class integratedUIs(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ui = None
        self.uiObject = None
        self.app = None
        self.running = False
        self.firstPlot = True
        self.canvas=None
        self.figure=None
        self.plotLayout=None

        # Set user variables in viewer
        self.beamline = 3
        self.referenceDetector = 'xfel_bl_3_tc_bm_1_pd/charge'

        # Set integration type
        self.integrateType = 'live'
        self.nlive = 100
        self.runNumber = getNewestRun( self.beamline )
        self.detector = 'MPCCD-8-2-002-1'
        self.rois = {}


    def run(self):
        self.ui,self.uiObject, self.app = self.load_ui( roiSetter_ui, start=True, show=True )
        self.ui.set_ui , self.ui.set_uiO , dummy =  self.load_ui( roi_set_ui, start=False, show=True )
        self.ui.det_ui , self.ui.det_uiO , dummy =  self.load_ui( availableDetectors_ui, start=False, show=True )

        # Set value defaults for  main ui screen
        self.ui.radioBtn_live.setChecked(True)
        self.ui.tbox_detector.setText( self.detector )
        self.ui.tbox_run.setText( str(self.runNumber) )
        self.ui.tbox_num_shots_live.setText( str(self.nlive) )
        self.ui.plainTextEditBeamline.setPlainText( str(self.beamline) )
        self.ui.plainTextEditReferenceDet.setPlainText( self.referenceDetector )

        # Set button operations for main ui screen
        self.ui.radioBtn_live.toggled.connect(  self.liveCheck )
        self.ui.radioBtn_run.toggled.connect(  self.runCheck )
        self.ui.pushButtonUpdate.clicked.connect( self.updateAll )
        self.ui.btn_run_plot.clicked.connect( self.plot )
        self.ui.btn_stop_plot.clicked.connect( self.requestStop )

        # Set value defaults for available detectors screen
        self.updateDetectors()

        # Set value defaults for set rois screen
        self.loadROI()
        self.printROIs()

        # Set button operations for Set ROIs screen
        self.ui.set_ui.btn_add_roi.clicked.connect( self.updateROI )
        self.ui.set_ui.btn_remove_roi.clicked.connect( self.removeROI )

        
        

        sys.exit(self.app.exec_())

    def requestStop(self):
        self.running = False

    def makeColorPlot(self,image):
        x = np.arange( image.shape[0] )
        y = np.arange( image.shape[1] )
        colorPlot( x , y , image.T)

    def plot(self):
        self.updateAll()
        
        if self.integrateType=='live':
            self.running = True
            while self.running:
                if not self.firstPlot:
                    plt.close()
                    plt.clf() 
                image = liveIntegratedCamera( self.detector , self.nlive , self.beamline , equip = self.referenceDetector )
                self.makeColorPlot(image)
                if self.firstPlot:
                    self.capturePlotInWidget( self.ui.plot )
                    self.firstPlot=False
                else:
                    #self.updatePlot()
                    self.canvas.close()
                    time.sleep(0.1)
                    self.capturePlotInWidget( self.ui.plot )
                    time.sleep(0.1)
                self.add_rois()
                time.sleep(0.1)
                self.canvas.draw()
                self.canvas.show()
                QtCore.QCoreApplication.processEvents()
                time.sleep(1)

        else:
            if not self.firstPlot:
                plt.close()
                plt.clf()
            image = runIntegratedCamera( self.detector , self.runNumber , self.beamline , equip = self.referenceDetector )
            self.makeColorPlot(image)
            if self.firstPlot:
                self.capturePlotInWidget( self.ui.plot )
                self.firstPlot=False
            else:
                #self.updatePlot()
                self.canvas.close()
                self.capturePlotInWidget( self.ui.plot )
            self.add_rois()

    def add_rois(self):
        for roi in self.rois.keys():
            if self.detector == self.rois[roi]['Detector']:
                print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
                self.add_an_roi( roi )

    def add_an_roi(self, roiName):
        print(self.rois[roiName])
        X1 = self.rois[roiName]['X1']
        X2 = self.rois[roiName]['X2']
        Y1 = self.rois[roiName]['Y1']
        Y2 = self.rois[roiName]['Y2']

        DX = X2-X1
        DY = Y2-Y1

        p=patch.Rectangle( (X1,Y1) , width = DX , height= DY , fill=False , linewidth = 2, color='r')
        ax = plt.gca()
        ax.add_patch(p)


    def capturePlotInWidget( self , widget ):
        # a figure instance to plot on
        self.figure = plt.gcf()

        # this is the Canvas Widget that displays the `figure`
        self.canvas = FigureCanvas(plt.gcf())
        self.canvas.setObjectName("canvas")

        # now use a layout to put the canvas into the existing widget
        if self.plotLayout is None:
            self.plotLayout = QtWidgets.QVBoxLayout( widget )
            self.plotLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            self.plotLayout.setContentsMargins(0, 0, 0, 0)
            self.plotLayout.setObjectName("Plot")
        self.plotLayout.addWidget(self.canvas)

    def updatePlot(self):
        self.figure = plt.gcf()
        self.canvas.figure = plt.gcf()
        self.canvas.draw()

    def loadROI(self):
        self.rois = load_obj('roiDefinitions')

    def removeROI(self):
        roiName = self.ui.set_ui.tbox_name.text().strip()
        newDict = {}
        for key in self.rois.keys():
            if key == roiName:
                continue
            else:
                newDict[key] = self.rois[key]
        self.rois = newDict
        self.printROIs()
        save_obj( self.rois , 'roiDefinitions' )


    def updateROI(self):
        roiName = self.ui.set_ui.tbox_name.text().strip()
        x1 = self.ui.set_ui.tbox_x1.text().strip()
        x2 = self.ui.set_ui.tbox_x2.text().strip()
        y1 = self.ui.set_ui.tbox_y1.text().strip()
        y2 = self.ui.set_ui.tbox_y2.text().strip()

        if (len(x1)==0)|(len(x2)==0)|(len(y1)==0)|(len(y2)==0)|(len(roiName)==0):
            return

        try:
            anROI = { roiName : { 'Detector':self.detector , 'Description':'An image', 'X1':int(x1), 'X2':int(x2), 'Y1':int(y1), 'Y2':int(y2) } }
            self.rois = merge_dictionaries( anROI , self.rois )
            self.printROIs()
            save_obj( self.rois , 'roiDefinitions' )
        except Exception as e:
            print(str(e))


    def printROIs(self):
        roiNames =self.rois.keys()
        roiLines=''
        for idx, name in enumerate(roiNames):
            roiLines+='%s, %s, %d, %d, %d, %d'%(name,self.rois[name]['Detector'],self.rois[name]['X1'],self.rois[name]['X2'],self.rois[name]['Y1'],self.rois[name]['Y2'])
            if idx < len(roiNames)-1:
               roiLines+='\n'

        self.ui.set_ui.tbox_current_roi.setText( roiLines )


    def updateAll(self):
        self.beamline = int(self.ui.plainTextEditBeamline.toPlainText().strip())
        self.referenceDetector = (self.ui.plainTextEditReferenceDet.toPlainText().strip())
        self.runNumber = int(self.ui.tbox_run.text().strip())
        self.nlive = int(self.ui.tbox_num_shots_live.text().strip())
        self.detector = (self.ui.tbox_detector.text().strip())
        self.updateDetectors()

    def updateDetectors(self):
        #detList = getCurrentDetectorList( self.beamline )
        detList = olpy.read_detidlist()
        printedDets = self.linePrintList( detList )
        self.ui.det_ui.plainTextEditDetectors.setPlainText(printedDets)
        
            
    def liveCheck(self):
        self.ui.radioBtn_run.setChecked(False)
        self.integrateType = 'live'
            
    def runCheck(self):
        self.ui.radioBtn_live.setChecked(False)
        self.integrateType = 'run'


    def load_ui(self, uiMWClass, start=False, show=False):
        if start:
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = None
        uiObject= QtWidgets.QMainWindow()
        ui =  uiMWClass.Ui_MainWindow()
        ui.setupUi( uiObject )
        if show:
            uiObject.show()

        while uiObject is None:
            time.sleep(0.1)
        while ui is None:
            time.sleep(0.1)

        

        return ui, uiObject, app

    def linePrintList(self,alist):
        astring=''
        for idx, det in enumerate(alist):
            if idx == 0:
                astring += det
            else:
                astring += '\n'+det
        return astring

  
 

###########################################################################################
# UI main
###########################################################################################

if __name__ == "__main__":
    master = integratedUIs()
    master.start()



