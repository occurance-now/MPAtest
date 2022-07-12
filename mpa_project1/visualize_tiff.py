import rasterio as rio
import rasterio.plot
from rasterio.plot import show
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from datetime import datetime


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
