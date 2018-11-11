from PyQt5 import QtCore, QtGui, QtWidgets

import dataGrabber_ui
import availablePDs_ui
import availableROIs_ui
import os

os.environ['dropboxPath'] = '../Dropbox'
import time

import numpy as np
import matplotlib.pyplot as plt
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
# Defaults detector parameters
###########################################################################################

refDet='xfel_bl_3_tc_bm_2_pd/charge'

pointDetectors = {'xfel_bl_3_tc_bm_2_pd/charge':{'Description':'Xray pulse energy','Nickname':'pulseEnergy','motorName':None},
'xfel_bl_3_st_2_pd_user_10_fitting_peak/voltage':{'Description':'Xray pulse energy detector voltage','Nickname':'pulseEnergyV','motorName':None},
'xfel_bl_3_lh1_shutter_1_open_valid/status':{'Description':'Optical shutter','Nickname':'opticalShutter','motorName':None},
'xfel_bl_3_shutter_1_open_valid/status':{'Description':'Xray shutter','Nickname':'xrayShutter','motorName':None},
'xfel_bl_3_st_1_motor_73/position':{'Description':'Time tool stage','Nickname':'ttStage','motorName':None},
'xfel_bl_3_st_2_motor_1/position':{'Description':'Optical stage','Nickname':'opticalStage','motorName':None},
'xfel_bl_3_st_2_motor_2/position':{'Description':'ND position','Nickname':'NDpos','motorName':None},
'xfel_bl_3_st_2_motor_5/position':{'Description':'Optical rotation','Nickname':'opticalRotation','motorName':None},
'xfel_bl_3_st_2_motor_6/position':{'Description':'Optical swivel','Nickname':'opticalSwivel','motorName':None},
'xfel_bl_3_st_2_motor_40/position':{'Description':'Sample X','Nickname':'sampleX','motorName':None},
'xfel_bl_3_st_2_motor_41/position':{'Description':'Sample Y','Nickname':'sampleY','motorName':None},
'xfel_bl_3_st_2_motor_42/position':{'Description':'Sample Z','Nickname':'sampleZ','motorName':None},
'xfel_bl_3_st_2_pd_laser_fitting_peak/voltage':{'Description':'Optical power','Nickname':'opticalPower','motorName':None}}

nicknameLookupDict={ pointDetectors[det]['Nickname']:det for det in pointDetectors.keys() }

rois = { 'ROI1': {'Detector':'MPCCD-1-1-010',
                 'Description':'MPCCD tile 10',
                 'X1':1,
                 'X2':10,
                 'Y1':1,
                 'Y2':10} } 

###########################################################################################
# UI thread class
###########################################################################################

class uiThreads(threading.Thread):
    def __init__(self, uiMWClass):
        threading.Thread.__init__(self)
        self.uiObject = None
        self.ui = None
        self.uiMWClass = uiMWClass

    def run(self):
        app = QtWidgets.QApplication(sys.argv)
        self.uiObject= QtWidgets.QMainWindow()
        self.ui =  self.uiMWClass.Ui_MainWindow()
        self.ui.setupUi( self.uiObject )
        self.uiObject.show()
        sys.exit(app.exec_())

###########################################################################################
# Integrated UIs
###########################################################################################

class integratedUIs(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ui = None
        self.uiObject = None
        self.app = None
        self.myDataSaver = None
        self.dataSaverRunning = False

        # Set user variables in dataGrabber
        self.runningGrabber = False
        self.beamline = 3
        self.referenceDetector = 'xfel_bl_3_tc_bm_1_pd/charge'
        self.pointDetectors = pointDetectors.keys()
        self.rois = rois.keys()

        self.pointDetDict = pointDetectors
        self.roisDict = rois

        # Set user variables in Available Point Detectors
        self.search = ''

        

        # All detectors
        self.allDetectors = getEquipmentList()
        self.allROIs      = self.getAvailableROIs()
        self.roiKeys = self.allROIs.keys()

    def run(self):
        self.ui,self.uiObject, self.app = self.load_ui( dataGrabber_ui, start=True, show=True )
        self.ui.pd_ui , self.ui.pd_uiO , dummy =  self.load_ui( availablePDs_ui, start=False, show=False )
        self.ui.roi_ui , self.ui.roi_uiO , dummy =  self.load_ui( availableROIs_ui, start=False, show=False )

        #pd_ui,pd_uiObject, app = self.load_ui( dataGrabber_ui, start=False, show=False )

        # Setup buttons in dataGrabber window
        self.ui.availablePointDetButton.clicked.connect(  self.ui.pd_uiO.show )
        self.ui.availableROIs.clicked.connect(  self.ui.roi_uiO.show )
        self.ui.updateButton.clicked.connect(  self.updateVariables )
        self.ui.startButton.clicked.connect(  self.grabData )
        self.ui.stopButton.clicked.connect(  self.stopGrabbingData )

        # Setup text areas in dataGrabber window
        self.ui.beamlineTextEdit.setPlainText( '3' )
        self.ui.refDetTextEdit.setPlainText( 'xfel_bl_3_tc_bm_1_pd/charge' )

        pds = self.linePrintList( self.pointDetectors )
        self.ui.pointDetectorsInput.setPlainText( pds )

        roiLines = self.linePrintList( self.rois )
        self.ui.roiInput.setPlainText( roiLines )

        # Setup buttons in Available Point Detectors window
        self.ui.pd_ui.pushButtonSearch.clicked.connect(  self.performSearch )

        # Setup text area in Available Point Detectors window
        self.performSearch()

        # Setup text area in Available ROIs window
        roiLines = self.linePrintList( self.roiKeys )
        self.ui.roi_ui.plainTextEditROI.setPlainText( roiLines )
        

        sys.exit(self.app.exec_())

    def getAvailableROIs(self):
        return load_obj('../Viewer/roiDefinitions')

    def grabData(self):
        self.updateDesiredDataDictionaries()
        self.dataSaverRunning = True

        self.myDataSaver = dataSaver()
        self.myDataSaver.setPointDetector( self.pointDetDict )
        self.myDataSaver.setROIs( self.roisDict )
        self.myDataSaver.start()
        
        while self.dataSaverRunning:
            QtCore.QCoreApplication.processEvents()
            self.updateStatus()
            time.sleep(.1)

    def stopGrabbingData(self):
        self.dataSaverRunning = False
        self.myDataSaver.requestStop()
        time.sleep(0.1)
        self.updateStatus()

    def updateDesiredDataDictionaries(self):
        pointDetList = self.ui.pointDetectorsInput.toPlainText().splitlines()
        self.pointDetDict = { pd.strip():{'Description':None,'Nickname':None,'motorName':None} for pd in pointDetList }
        roiList = self.ui.roiInput.toPlainText().splitlines()
        self.roisDict = {roiName:self.allROIs[roiName] for roiName in roiList}

    def updateVariables(self):
        self.allDetectors = getEquipmentList()
        self.allROIs      = self.getAvailableROIs()
        self.roiKeys = self.allROIs.keys()

        # Refresh text area in Available ROIs window
        roiLines = self.linePrintList( self.roiKeys )
        self.ui.roi_ui.plainTextEditROI.setPlainText( roiLines )

        # Refresh text area in Available Point Detectorss window
        self.allDetectors = getEquipmentList()
        self.ui.pd_ui.plainTextEditSearch.setPlainText( '' )
        self.performSearch()

        # Refresh grabber status
        try:
            self.ui.statusLabel.setText( self.myDataSaver.lastStatus() )
        except Exception as e:
            print(str(e))
            self.ui.statusLabel.setText( '' )

    def updateStatus(self):
        # Refresh grabber status
        try:
            self.ui.statusLabel.setText( self.myDataSaver.lastStatus() )
        except Exception as e:
            print(str(e))
            self.ui.statusLabel.setText( '' )
            

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

    def openPointDetectorWindow(self):
        self.load_ui( availablePDs_ui )

    def openROIsWindow(self):
        self.load_ui( availableROIs_ui )

    def linePrintList(self,alist):
        astring=''
        for idx, det in enumerate(alist):
            if idx == 0:
                astring += det
            else:
                astring += '\n'+det
        return astring

    def gatherMatches(self,astr , alist):
        if len(astr) == 0:
            return alist
        matches=[]
        for el in alist:
            if astr in el:
                matches.append(el)
        return matches

    def performSearch( self ):
        self.search = self.ui.pd_ui.plainTextEditSearch.toPlainText().strip()
        matches = self.gatherMatches( self.search , self.allDetectors )
        printedMatches= self.linePrintList( matches )
        self.ui.pd_ui.plainTextEditPDList.setPlainText( printedMatches )

    #def printMatches( self ,  )

###########################################################################################
# Regular UI class
###########################################################################################

class uis():
    def __init__(self, uiMWClass):
        self.uiObject = None
        self.ui = None
        self.uiMWClass = uiMWClass

    def run(self):
        app = QtWidgets.QApplication(sys.argv)
        self.uiObject= QtWidgets.QMainWindow()
        self.ui =  self.uiMWClass.Ui_MainWindow()
        self.ui.setupUi( self.uiObject )
        self.uiObject.show()
        sys.exit(app.exec_())

    def start(self):
        self.run()

###########################################################################################
# UI thread master class
###########################################################################################

import threading
class uiThreadMaster(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.dGthread = uis( dataGrabber_ui )
        self.dGthread.start()
        while self.dGthread.uiObject is None:
            time.sleep(0.1)
        while self.dGthread.ui is None:
            time.sleep(0.1)

        self.dGthread.ui.pointDetectorsInput.setPlainText( 'Hello' )
        self.dGthread.uiObject.show()


        self.dGthread.ui.availablePointDetButton.clicked.connect(self.openPointDetectorWindow)
        self.dGthread.ui.availableROIs.clicked.connect(self.openROIWindow)


        self.go = True

    def openPointDetectorWindow(self):
        self.pDthread = uis( availablePDs_ui )
        self.pDthread.run()
        while self.pDthread.uiObject is None:
            time.sleep(0.1)

        while self.pDthread.ui is None:
            time.sleep(0.1)

    def openROIWindow(self):
        self.roiThread = uis( availableROIs_ui )
        self.roiThread.run()

        while self.roiThread.uiObject is None:
            time.sleep(0.1)
        while self.roiThread.ui is None:
            time.sleep(0.1)

    def run(self):
        
        while self.go:
            continue

    def request_stop(self):
        self.go = Falser
 

###########################################################################################
# UI main
###########################################################################################

if __name__ == "__main__":
    master = integratedUIs()
    master.start()

    



