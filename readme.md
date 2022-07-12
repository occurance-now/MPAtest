
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





