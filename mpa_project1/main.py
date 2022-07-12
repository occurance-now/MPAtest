import netCDF4 as nc
import numpy as np
import rioxarray
import xarray
import rasterio as rio
import rasterio.plot
from rasterio.plot import show
import pymatlab
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import scipy
from datetime import datetime
import ipywidgets as widgets
import os
import math

fn = './DataSet/hycom.nc'
dc = nc.Dataset(fn)#open data set
xds = xarray.open_dataset('./DataSet/hycom.nc')#open data set with xarray

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
    print(xds['water_speed'][0,0,100,100])
    return xds
def setup_lat_lon(xds):
    lon = xds.variables['lon']
    lat = xds.variables['lat']
    #time = xds.variables['time']
    print((290+180) % 360 - 180)
    print(xds['water_speed'][0,0,100,100])

    #Reproject longitude to 0-180
    converted = []
    for l in lon:
        long1 = ((l+180) % 360 - 180)
        converted.append(long1)

    xds['lon'] = ('lon', converted)
    #xds = xds.sortby('lat', ascending=False)#Reverse latitude list proper North South Orientation

    return xds
def define_tiff_content(xds):
    wT = xds['water_speed']#Define primary variable in TIFF file
    new_dims = ('lat','lon','time')

    for i in wT.dims:
        if i in (new_dims):
            pass#Remove other dimensions for 2d visualization
        else:
            wT = wT.squeeze(i)#Remove dimensions for variable other than lat, lon, and time
    return wT
def write_tiff_file(wT):
    counter = 0 # counter for iterating though time dimension values
    primary_var = wT.standard_name#file name
    time = wT.coords['time'].values#return time stamps for time dimensions
    print(xds['water_speed'][0,0,100,100])

    for i in time:
        wT = xds['water_speed'][counter]
        wT = wT.rio.set_spatial_dims(x_dim='lon', y_dim='lat')#set TIFF x and y params
        wT.rio.crs

        # Define the CRS projection
        wT.rio.write_crs("epsg:4326", inplace=True)
        tiff_file_name = (f"./geoTIFF/%s_%s.tiff" % (primary_var, counter))
        wT.rio.to_raster(tiff_file_name)#write the tiff files
        counter += 1 #track iteration and time dimension index



    return primary_var, time
def visualize_tiff_files(primary_var, time):
    #Open the first Data set
    data_name = f"./geoTIFF/water_speed_0.tiff"
    tiff1 = rasterio.open(data_name)
    image1 = tiff1.read()

    #Get dictionary of key, values for all files in geoTIFF directory
    file_data = dict()
    for filename in os.listdir('./geoTIFF/'):
        file_data[filename] = rasterio.open('./geoTIFF/%s' % (filename))

    #List of dictionary keys
    titles = list(file_data.keys())

    #Index button clicks
    global button_count
    button_count = 1

    #List of formatted times for graph title
    strf_time = []
    for dt in time:
        ts = pd.to_datetime(str(dt))
        d = ts.strftime('%y-%m-%d Hour:%H')
        strf_time.append(d)

    #Plot graph
    fig, ax = plt.subplots()
    ax.invert_yaxis()


    im = image1[0,:,:]
    image_hidden = ax.imshow(im)
    plot1 = rio.plot.show(source=tiff1, ax=ax, title = (f'%s\n %s' % (titles[0], strf_time[0])))

    fig.colorbar(image_hidden, ax=ax)

    #On-click button event handler
    def _yes(event):
        global button_count
        if button_count < len(strf_time):
            plot1 = rio.plot.show(source=file_data['water_speed_%s.tiff' % (button_count)], ax=ax, title = (f'%s\n %s' % (titles[button_count], strf_time[button_count])))
            fig.canvas.draw()
            button_count += 1
            print(button_count)
        elif button_count == len(strf_time):
            button_count = 0
            plot1 = rio.plot.show(source=file_data['water_speed_%s.tiff' % (button_count)], ax=ax, title = (f'%s\n %s' % (titles[button_count], strf_time[button_count])))
            fig.canvas.draw()
            print(button_count)
        else:
            print("something went wrong")

    #define button
    axes = plt.axes([0.5, 0.000001, 0.4, 0.075])#button position and size
    button = Button(axes, 'Next Data Sample', color='grey',hovercolor='blue' )
    button.on_clicked(_yes)
    plt.show()

if __name__ == "__main__":
    try:
        xds = calc_water_speed(xds)#calc water speed and add water_speed var to data table
        xds = setup_lat_lon(xds)#setup lat/lon coordinates
        wT = define_tiff_content(xds)#define the content of the geoTIFF file
        primary_var, time = write_tiff_file(wT)#write TIFF files to GeoTIFF folder
        visualize_tiff_files(primary_var, time)#visualize the the tiff files
    except Exception as e:
        print(e)
else:
    pass#main is not meant to be a module
