import math
import numpy as np

def calc_water_speed(xds):
    vlc_north = xds.variables['water_v']#vector North
    vlc_east =  xds.variables['water_u']#vector East

    #Start Pathag Theorom
    vlc_north = np.square(vlc_north)#square the north vector
    vlc_east = np.square(vlc_east)#square east vector

    xds = xds.assign(water_speed=(vlc_east+vlc_north))#create new variable in dim table

    water_speed = xds.variables['water_speed']#assign dim variable to local var
    water_speed = np.sqrt(water_speed)#finish pythag theorum
    np.set_printoptions(suppress=True)#surpress scientific notation

    #Define Water_Speed Variable attributes
    attrs = {
        'units': 'm/s', 'long_name': 'Water Speed', 'standard_name': 'water_speed', 'NAVO_code': 'N/A'
    }
    xds['water_speed'].attrs = attrs

    return xds
