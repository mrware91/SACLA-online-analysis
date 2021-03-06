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

# there is the detector called det in the H5
# there is detector info called info in the H5

# I need to figure out how to get the detector coordinates from the database

detector_stage_direction_in_degree = [ 0 , 0 , 0 ,0 ,0,0,0,0]
detector_stage_shift_weight = [ 0 , 0 , 0 ,0,0,0,0,0]
manipulator_position_in_micro_meter = [ 0 , 0 , 0 ,0,0,0,0,0]
detector_coordinate_in_micro_meter = [ (-1599.23,51678.8) , (-1655.65,25016) , (799.187,-1735.1) , (782.785,-28498.8) , (-792.005,28477.5) , (-838.52,1818.2) , (1650.0,-24900.0) , (1618.37,-51643.8)]
detector_rotation_angle_in_degree = [ 269.925 , 269.966 , 269.969 , 269.855 , 90.0468 , 89.965 , 90.0 , 90.018]


def generate_tile_coords():
        x_all = np.zeros((512,1024,8))
        y_all = np.zeros((512,1024,8))
        tilesize = (512,1024)

        for idx in range(8):
            origin = detector_coordinate_in_micro_meter[idx]
            thetad  = detector_rotation_angle_in_degree[idx]

            x , y = single_tile_coords( tilesize , origin , thetad )


            theta_shift = detector_stage_direction_in_degree[idx] * np.pi/180.
            shiftweight = detector_stage_shift_weight[idx]
            manip = manipulator_position_in_micro_meter[idx]

            x = x + np.cos(theta_shift) * shiftweight * manip
            y = y + np.sin(theta_shift) * shiftweight * manip

            x_all[:,:,idx] = x
            y_all[:,:,idx] = y

        return x_all, y_all



def single_tile_coords( tilesize , origin , theta ):
        '''
                Takes data in tile and places first number at origin and assigns coordinats to pixels.
                Theta is rotation from origin being in upper left

                Theta should be specified in degrees. Origin in micron.
        '''
        xp = np.arange( tilesize[0] )
        yp = np.arange( tilesize[1] )

        x_micron = xp*50.
        y_micron = yp*50.

        theta_rad = theta*np.pi/180.
        R = np.mat([[np.cos(theta_rad) , np.sin(theta_rad)] , [-np.sin(theta_rad) , np.cos(theta_rad)]])

        x = np.zeros( tilesize )
        y = np.zeros( tilesize )

        for ix,x in enumerate(x_micron):
                for iy, y in enumerate(y_micron)
                        v = R*np.array( [x,y] )
                        x[ix,iy] , y[ix,iy] = v[0], v[1] 
        return x+origin[0], y+origin[1]




