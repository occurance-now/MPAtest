import xarray
import rasterio as rio

from calc_water_speed import calc_water_speed
from visualize_tiff import visualize_tiff_files

#import netCDF4 as nc
#dc = nc.Dataset(fn)#open data set

fn = './DataSet/hycom.nc'
xds = xarray.open_dataset(fn)#open data set with xarray

def setup_lat_lon(xds):
    lon = xds.variables['lon']#get lon variable
    lat = xds.variables['lat']#get lat variable

    #Reproject longitude to 0-180
    converted = []
    for l in lon:
        long1 = ((l+180) % 360 - 180)
        converted.append(long1)

    xds['lon'] = ('lon', converted)#Add converated lon to data set
    xds = xds.sortby('lat', ascending=False)#Reverse latitude list proper North South Orientation

    return xds
def define_tiff_content(xds):
    wT = xds['water_speed']#Define primary variable in TIFF file
    new_dims = ('lat','lon','time')#Define target dimensions

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

    #for each time dimension save a .tiff file with corresponding dimension data
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
