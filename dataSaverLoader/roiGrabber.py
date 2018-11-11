import os
import sys

import numpy as np
import io
import time

from Database import *

import pandas as pd

def integratedMPCCD(det, tags, hightag=201802, equip = 'xfel_bl_3_tc_bm_2_pd/charge'):
    objReader = olpy.StorageReader(det)
    objBuffer = olpy.StorageBuffer(objReader)
    
    tag0 = tags[0]
    realtag = objReader.collect(objBuffer, tag0)
    detArray = objBuffer.read_det_data(0) 
    for tag in tags[1:]:
        try:
            realtag = objReader.collect(objBuffer, tag)
            detArray += objBuffer.read_det_data(0) 
        except (olpy.APIError) as ex:
            raise Exception(str(ex))
        except Exception as ex:
            raise Exception(str(ex))
        
    return detArray
    
tagHigh = getNewestTag( 'xfel_bl_3_tc_bm_2_pd/charge' )
tagLow = tagHigh - 100
tagRange = (tagLow, tagHigh)
tags = [ tag for tag in range(tagRange[0],tagRange[1]) ]

iM = integratedMPCCD( 'MPCCD-8-2-002-3' , tags  )
