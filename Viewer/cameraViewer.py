import os
import sys
os.environ['dropboxPath'] = '/home/mrware/ANAPC/online/Dropbox'
sys.path.append('/home/software/SACLA_tool/local/python3.5/lib/python3.5/site-packages')
sys.path.append('/home/mrware/ANAPC/online/dataSaverLoader')
sys.path.insert(0, os.environ['dropboxPath'] + '/Code/mattsTools')


import numpy as np
import io
import time

from Database import *

import pandas as pd

import matplotlib.pyplot as plt
from plotStyles import *

###########################################################################################
# Camera integration
###########################################################################################

def integratedCamera(det, tags, hightag=201802, equip = 'xfel_bl_3_tc_bm_2_pd/charge'):
    objReader = olpy.StorageReader(det)
    objBuffer = olpy.StorageBuffer(objReader)
    
    detArray = np.zeros((1024,512))
    ntags = 0.
    for tag in tags:
        try:
            realtag = objReader.collect(objBuffer, tag)
            detArray += objBuffer.read_det_data(0) 
            ntags += 1.
        #except (olpy.APIError) as ex:
        #    raise Exception(str(ex))
        except Exception as ex:
            print(str(ex))
        
    return detArray/ntags

def runIntegratedCamera( det , run , bl , equip = 'xfel_bl_3_tc_bm_2_pd/charge' ):
    tagRange = getTagRange( bl , run )
    print(tagRange)
    tags = [ tag for tag in range(tagRange[0][1],tagRange[1][1]) ]

    hightag = getHighTag( bl , run )
    return integratedCamera( det, tags, hightag=hightag, equip=equip )

def liveIntegratedCamera( det , ntags , bl , equip = 'xfel_bl_3_tc_bm_2_pd/charge' ):
    tagHigh = getNewestTag( equip )
    tagLow = tagHigh - ntags
    tagRange = (tagLow, tagHigh)
    tags = [ tag for tag in range(tagRange[0],tagRange[1]) ]

    hightag = getNewestHighTag( bl )

    return integratedCamera( det, tags, hightag=hightag, equip=equip )
