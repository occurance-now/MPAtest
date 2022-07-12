
<h1>MPAtest</h1>

<h3>Description</h3 style="bold">
MPAtest is a tool for reading oceanographic data from a .nc file, writing that data as .tiff, and visualizing the data by timestamp using matplotlib.

<h3>The tool utilizes the following technologies:</h3 style="bold">

<ul>
  <li>matplotlib==3.5.2</li>
  <li>numpy==1.23.0</li>
  <li>pandas==1.4.3</li>
  <li>rasterio==1.3.0</li>
  <li>xarray==2022.3.0</li>
</ul>


<h3>Definitions</h3 style="bold">

<ol>
<li>xds: The 'xarray data sheet' variable represents the entire .nc data sheet in array using xarray for conversion.</li>
<li>wT: The 'water speed table' variable is used to perform functions specifically on the water speed variable.</li>
<li>primary_var: Holds the value of the variable name of the variable used to plot graphic.</li>
<li>time: Holds a list of values of the 'Time' dimension.</li>
<li>converted: Used to hold a list of longitude variables converted from 0-360 to 0-180.</li>
<li>new_dims: The list of dimensions that are to be visualized. </li>
</ol>


<h3>Methodology</h3 style="bold">

<b>Read Data</b><br>
In the main.py file the relative file path of the .nc file is described using the fn variable. The fn variable is then converted to an array using the xarray module.

<b>Calculate Water Speed</b><br>
The calc_water_speed.py file is use to calculate the water speed at each 'lat'-'lon' coordinate using the variables 'water-u' and 'water-v'. The 'water-u' represents the eastern velocity vector at each data point and the 'water-v' variable represents the northern velocity vector at each data point. Using Pythagorean Theorem we can calculate water speed for each pair. The water_speed variable is then assigned back to the xds array.

<b>Write Tiff File</b><br>
The main.py file then prepares the water_speed variable to be saved as a .tiff file. We first convert the 'lon' variable from 0-360 to 0-180 for a more typical visualization. Then we define the proper dimensions in the water_speed variable. For example we don't need the 'depth' dimension for plotting water speed. After that we write a .tiff file for each timestamp dimension of the water_speed variable. 

<b>Visualize Data</b><br>
The visualize_tiff.py file takes advantage of the rasterio.plot.show method and matplotlib. We first start by visualizing the fire set of data in the time stamp series. Then with the help of a custom budget widget we can cycle through each time stamp and visualize the corresponding data. Once the file timestamp is reach the loop starts again from the first timestamp in the series. 

<h3>Usage</h3 style="bold">

<ul>
  <li>Please place your .nc file in the 'Dataset' folder.</li>
  <li>Please address the name of your .nc file in the main.py file as the 'fn' variable.</li>
</ul>

