import os
import sys
import socket
import numpy as np
import io
import time

import pandas as pd

def loadJunkData( tagLow=None , tagHigh=None , directory='/home/mrware/ANAPC/online/dataSaverLoader/smallData' ):
    junkVariables = ['A','B','C','D']
    data = { var:np.random.rand(100) for var in junkVariables }
    return pd.DataFrame(data)

def loadData( tagLow=None , tagHigh=None , directory='/home/mrware/ANAPC/online/dataSaverLoader/smallData' ):
    junkVariables = ['A','B','C','D']
    data = { var:np.random.rand(100) for var in junkVariables }
    return pd.DataFrame(data)

def loadRunData( bl , run ,  directory='/home/mrware/ANAPC/online/dataSaverLoader/smallData'  ):
    return loadData(  )
    
def loadLiveData( ntags, directory='/home/mrware/ANAPC/online/dataSaverLoader/smallData', equip='xfel_bl_3_tc_bm_2_pd/charge' ):
    return loadData(  )

