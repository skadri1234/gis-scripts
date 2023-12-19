"""
your title block goes here
"""

## INITIALIZE YOUR SCRIPT WITH IMPORTS, DRIVE LETTER, PATHS, ETC.
## SET THE WORKSPACE TO THE TEMP DIRECTORY
import arcpy
import numpy as np

dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = temp_path

# import fibonacci_lattice
from fibonacci_lattice import *

### Open ArcPro and create a point feature class in your temp folder named 'CT_grid.shp'.
### Use NAD 83 (2011) for the XY coordinate system.
### Remove it from the contents pane to release the lock ArcPro puts on the shapefile

# Create variables for minimum, maximum latitude, longitude (total of four variables) for CT

lonMin = np.radians(-73.00 - 44.00 / 60.)
lonMax = np.radians(-71.00 - 47.00 / 60.)
latMin = np.radians(40.00 + 58.00 / 60.)
latMax = np.radians(42.00 + 3.00 / 60.)

# Use fibLatticeFiltered(N, lonMin, lonMax, latMin, latMax) with N = 20_000_000 to create the grid points'
# coordinates
N = 20_000_000
lon, lat = fibLatticeFiltered(N, lonMin, lonMax, latMin, latMax)

# Convert the longitudes to decimal degrees (DD)
# Convert the latitudes to decimal degrees (DD)
lon = np.rad2deg(lon)
lat = np.rad2deg(lat)


# Create an insert cursor for CT_grid.shp with field-list 'SHAPE@XY'
# Recall that the 2nd argument to arcpy.da.InsertCursor() can be either the name of a single attribute or
# a list of attributes names. Here, we use the single name because there are no other attributes.

with arcpy.da.InsertCursor('ct_grid.shp', 'SHAPE@XY') as ic:
    # iterate over zip(lon, lat). Assign the longitude to 'x' and the latitude to 'y'
    for x, y in zip(lon, lat):
        # use the insertRow([x,y]) method of the insert cursor to create this grid point.
        ic.insertRow([(x, y)])

# use arcpy.analysis.Clip() to clip CT_grid.shp to the Towns.shp shapefile in the data directory. Name
# the output CT_grid_clipped.shp and create it in the temp directory
arcpy.analysis.Clip('ct_grid.shp', data_path + 'Towns.shp', 'ct_grid_clip.shp')

# Open your feature class in arcpro and take a screenshot of it.
# Submit this script, your CT_grid_clipped.shp, and the screenshot. How far apart are the points (km)?