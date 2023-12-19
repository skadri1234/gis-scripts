
from lib5585 import *
import arcpy
import numpy as np

dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"

arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path
dem_raster = data_path + "DEM.img"

# Open DEM raster using describe
desc = arcpy.Describe(dem_raster)
cellsize = desc.meanCellHeight
e = desc.extent.XMin
n = desc.extent.YMax

# Load the DEM into a NumPy array
dem_array = arcpy.RasterToNumPyArray(dem_raster)

# project survey points to match the DEM
arcpy.management.Project("surveyPts.shp", "surveyPts_projected.shp", desc.spatialReference)

# Create an empty list to hold errors
errors = []

# Open the projected survey points
with arcpy.da.SearchCursor("surveyPts_projected.shp", ["SHAPE@XY", "FIELD_ELEV"]) as cursor:
    for row in cursor:
        easting, northing = row[0]
        elevation = float(row[1])
        row_index, col_index = en2rc(easting, northing, e, n, cellsize)
        dem_elevation = float(dem_array[row_index, col_index])
        error = elevation - dem_elevation
        errors.append(error)

# Calculate mean and standard deviation of errors
mean_error = np.mean(errors)
std_deviation = np.std(errors)

print(f"Mean Error: {mean_error:.3f}")
print(f"Standard Deviation: {std_deviation:.3f}")