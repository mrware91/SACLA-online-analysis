import os
import sys
import socket
hostname = socket.gethostname()
if "opcon" not in hostname:
    sys.path.append('/home/software/SACLA_tool/local/python3.5/lib/python3.5/site-packages')
import numpy as np
import io
import time
import dbpy

if "opcon" not in hostname:
	import olpy

import pandas as pd


###########################################################################################
# Useful python commands
###########################################################################################
def merge_dictionaries( *args ):
    z = {}
    for arg in args:
        z.update( arg )
    return z


###########################################################################################
# dbpy fast commands - ie database access
###########################################################################################
def getEquip( tags , equip , hightag=201802 ):
    try:
        return dbpy.read_syncdatalist_float( equip, hightag , tags )
    except Exception as e:
        print(str(e))
        return np.nan

def getEquipInt( tags , equip , hightag=201802 ):
    return dbpy.read_syncdatalist( equip, hightag , tags )

def getNewestTag( equip ):
  newtag = dbpy.read_tagnumber_newest( equip )
  return newtag[1]

def getNewestRun( bl ):
    return dbpy.read_runnumber_newest( bl )

def getDetectorList( bl , run ):
    return dbpy.read_detidlist( bl , run )

def getCurrentDetectorList( bl ):
    return dbpy.read_detidlist( bl , getNewestRun(bl) )

def getEquipmentList(  ):
    return dbpy.read_equiplist(  )

def getHighTag( bl , run ):
    return dbpy.read_hightagnumber( bl , run )

def getCurrentHighTag( bl ):
    return dbpy.read_hightagnumber( bl , getNewestRun(bl) )

def getEndTag( bl , run ):
    return dbpy.read_end_tagnumber( bl , run )

def getStartTag( bl , run ):
    return dbpy.read_start_tagnumber( bl , run )

def getTagRange( bl , run ):
    return getStartTag(bl,run) , getEndTag(bl,run)

def getNewestHighTag( bl ):
    try:
        run = getNewestRun( bl )
        startTags = getStartTag( bl , run )
        return startTags[0]

    except Exception as e:
        print('Could not get newest hightag. Defaulting to 201802. Error was '+str(e))
        return 201802



###########################################################################################
# Experiment data access
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

def nickname2Detector( nickname ):
    return nicknameLookupDict[nickname]

def grabPointData( pointDetectors , tags , hightag=201802 ):
    pointData = { pd:{ 'Data':getEquip( tags , pd , hightag=hightag ) , 
                  'Description':pointDetectors[pd]['Description'] ,
                  'Nickname':pointDetectors[pd]['Nickname']} for pd in pointDetectors.keys() }
    pointData['tags'] = tags
    return pointData

def grabNewestPointData( pointDetectors , ngrab=30, bl=3 , refDet='xfel_bl_3_tc_bm_2_pd/charge', dontPassTag=None ):
    hightag = getNewestHighTag( bl )
    tagf = getNewestTag( refDet )    
    tagLow = tagf-ngrab
    if dontPassTag is not None:
        if tagLow <= dontPassTag:
            tagLow = dontPassTag + 1
    tags = tuple([ idx for idx in range(tagLow, tagf)])
    return grabPointData( pointDetectors , tags , hightag=hightag )

def makeDataFrame( pointData ):
    data={}
    for pid in pointData.keys():
        if pid is not 'tags':
            data[pid] = np.array(pointData[pid]['Data'])
    index = pointData['tags']
#     print(index)
    return pd.DataFrame( index=index, data=data )

def grabROI(det, tags, X1, X2, Y1, Y2, 
                 hightag=201802, equip = 'xfel_bl_3_tc_bm_2_pd/charge'):
    print(det)
    objReader = olpy.StorageReader(det)
    objBuffer = olpy.StorageBuffer(objReader)
    
    detROIs = np.array([0 for tag in tags])

    errorCount = 0
    
    for idx, tag in enumerate(tags):
      try:
        realtag = objReader.collect(objBuffer, tag)
        detArray = objBuffer.read_det_data(0) 
        detROIs[idx] = np.nanmean( detArray[X1:X2,Y1:Y2] )
      except Exception as ex:
        print(str(ex))
        errorCount +=1
     # except (olpy.APIError) as ex:
     #   raise Exception(str(ex))
     # except Exception as ex:
     #   raise Exception(str(ex))

    print('Errored on %d of %d tags'%( errorCount , len(tags) ))
        
    return detROIs

def grabROIData( rois , tags , hightag=201802, equip='xfel_bl_3_tc_bm_2_pd/charge' ):
    roiData = {}
    for roi in rois.keys():
        det = rois[roi]['Detector']
        description = rois[roi]['Description']
        X1 = rois[roi]['X1']
        X2 = rois[roi]['X2']
        Y1 = rois[roi]['Y1']
        Y2 = rois[roi]['Y2']
        print(det)
        roiData[roi] = { 'Data':grabROI(det, tags, X1, X2, Y1, Y2, hightag=hightag, equip = equip), 'Detector':det, 'X1':X1, 'X2':X2, 'Y1':Y1, 'Y2':Y2 }
    roiData['tags'] = tags
    return roiData

def grabNewestROIData( rois , ngrab=30, bl=3 , refDet='xfel_bl_3_tc_bm_2_pd/charge', dontPassTag=None ):
    hightag = getNewestHighTag( bl )
    tagf = getNewestTag( refDet )    
    tagLow = tagf-ngrab
    if dontPassTag is not None:
        if tagLow <= dontPassTag:
            tagLow = dontPassTag + 1
    tags = tuple([ idx for idx in range(tagLow, tagf)])
    return grabROIData( rois , tags , hightag=hightag, equip=refDet )

def grabNewestData( pointDetectors, rois , 
                   ngrab=30, bl=3 , refDet='xfel_bl_3_tc_bm_2_pd/charge',
                   dontPassTag = None):
    hightag = getNewestHighTag( bl )
    print(hightag)

    tagf = getNewestTag( refDet )    
    tagLow = tagf-ngrab
    if dontPassTag is not None:
        if tagLow <= dontPassTag:
            tagLow = dontPassTag + 1
    tags = tuple([ idx for idx in range(tagLow, tagf)])
    return merge_dictionaries( grabROIData( rois , tags , hightag=hightag, equip=refDet ), grabPointData( pointDetectors , tags , hightag=hightag ))


###########################################################################################
# Small data saving
###########################################################################################
import threading

class dataSaver(threading.Thread):
    def __init__(self, bl=3, refDet='xfel_bl_3_tc_bm_2_pd/charge', ngrab=120, maxTags2Save = 1000):
        threading.Thread.__init__(self)
        
        self.stop = False
        self.newestTag = None
        self.dontPassTag = None
        self.df = None
        
        self.ngrab = ngrab
        self.bl= bl
        self.refDet= refDet
        
        self.totalGrabbed = 0
        self.status = 'Waiting for initialization'
        self.last_status = 'Waiting for initialization'
        
        self.t0 = time.time()
        self.elapse = None
        
        self.saveAtTag = None
        self.maxTags2Save = maxTags2Save
        
    def setPointDetector(self, pointDetectors):
        self.pointDetectors = pointDetectors
        self.status += ', point detectors initialized'
    
    def setROIs(self, rois):
        self.rois = rois
        self.status += ', rois initialized'
        
    def run(self):
        self.status += ', running'
        self.last_status = 'running'
        while self.stop is not True:
            if self.newestTag is None:
                data = grabNewestData( self.pointDetectors, self.rois, ngrab=self.ngrab, bl=self.bl, refDet=self.refDet, dontPassTag=self.dontPassTag )
                self.df = makeDataFrame( data )
                self.saveAtTag = self.df.index.values.min()
                self.newestTag = self.df.index.values.max()
                self.totalGrabbed = self.df.index.values.shape[0]
            else:
                data = grabNewestData( self.pointDetectors, self.rois, ngrab=self.ngrab, dontPassTag=self.newestTag, bl=self.bl, refDet=self.refDet )
                self.df = pd.concat([self.df,makeDataFrame( data )],axis=0) 
                self.newestTag = self.df.index.values.max()    
                self.totalGrabbed = self.df.index.values.shape[0] 
                
            pickleName = '/home/mrware/ANAPC/online/dataSaverLoader/smallData/smallData_'+str(self.saveAtTag)+'.pkl' 
            self.df.to_pickle( pickleName )
            if self.totalGrabbed >= self.maxTags2Save:
                self.dontPassTag = self.newestTag
                self.newestTag = None
                self.totalGrabbed = 0
                
            
        self.elapse = time.time()-self.t0
        self.status += ', run completed.'
        self.last_status = 'run completed'
        
    def requestStop(self):
        self.stop = True
        
    def printStatus(self):
        if 'running' in self.status:
            print(self.status+'. # tags grabbed = '+str(self.totalGrabbed))
        else:
            print(self.status)
        
    def lastStatus(self):
        return self.last_status+': '+str(self.totalGrabbed)



###########################################################################################
# Small data loading
###########################################################################################
def getLowTags( directory='/home/mrware/ANAPC/online/dataSaverLoader/smallData' ):
    fns = os.listdir( directory )
    return np.array([int(fn[10:-4]) for fn in fns])

def nearestValue( nparray , val ):
    idx = np.argmin(np.abs( nparray-val ))
    return idx, nparray[idx]

def loadJunkData( tagLow=None , tagHigh=None , directory='/home/mrware/ANAPC/online/dataSaverLoader/smallData' ):
    junkVariables = ['A','B','C','D']
    data = { var:np.random.rand(100) for var in junkVariables }
    return pd.DataFrame(data)

def loadData( tagLow , tagHigh , directory='/home/mrware/ANAPC/online/dataSaverLoader/smallData' ):
    print(tagLow,tagHigh)
    lowTags = getLowTags( directory=directory )
    nearestIdx, nearestSaveTag = nearestValue( lowTags , tagLow )
    if nearestSaveTag > tagLow:
        if nearestIdx - 1 < 0:
            raise Exception( 'tagLow does not exist in saved data' )
        nearestSaveTag = lowTags[nearestIdx - 1]
        nearestIdx = nearestIdx - 1
        
    df = pd.read_pickle( directory+'/smallData_'+str(int(nearestSaveTag))+'.pkl' )
    while df.index.values.max() < tagHigh:
        nearestIdx += 1
        if nearestIdx >= lowTags.shape[0]:
            break
        nearestSaveTag = lowTags[nearestIdx]
        df_sub = pd.read_pickle( directory+'/smallData_'+str(int(nearestSaveTag))+'.pkl' )
        df = pd.concat([df,df_sub],axis=0)
        
    df = df[~df.index.duplicated(keep='first')]
    loadedTags = df.index.values
    dummy,minIdx = nearestValue(df.index.values , tagLow)
    dummy,maxIdx = nearestValue(df.index.values , tagHigh) 
    return df.loc[minIdx:maxIdx]

def loadRunData( bl , run ,  directory='/home/mrware/ANAPC/online/dataSaverLoader/smallData'  ):
    tagLow, tagHigh = getTagRange( bl , run )
    return loadData( tagLow[1] , tagHigh[1] , directory=directory )
    
def loadLiveData( ntags, directory='/home/mrware/ANAPC/online/dataSaverLoader/smallData', equip='xfel_bl_3_tc_bm_2_pd/charge' ):
    tagHigh = getNewestTag( equip )
    tagLow = tagHigh - ntags
    return loadData( tagLow , tagHigh , directory=directory )

