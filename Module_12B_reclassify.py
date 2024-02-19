"""
Shafeeq Kadri
"""

## RECLASSIFICATION USING NUMPY

## IN THIS EXERCISE, YOU WILL PERFORM THE FOLLOWING...
##      OPEN THE LANDCOVER.IMG RASTER AS A NUMPY ARRAY
##      USE Describe() TO GET ITS DESCRIPTION DICTIONARY
##      USE NUMPY'S unique() METHOD TO GET THE RASTER'S VALUES AND COUNTS
##      CREATE A RECLASSIFICATION ARRAY
##      CONVERT THE RECLASSIFICATION ARRAY INTO A RASTER
##      SET THE RASTER'S PROJECTION AND SAVE IT AS A .IMG RASTER
##-------------------------------------------------------------
## PART 1: INITIALIZE YOUR SCRIPT WITH VARIABLES FOR PATHS, ETC
#
import numpy as np
import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path
##-------------------------------------------------------------
## PART 2: RECLASSIFICATION
#

# use arcpy.RasterToNumPyArray() to read in Data\landcover.img
landcover_raster = arcpy.RasterToNumPyArray(data_path + 'landcover.img')

#use arcpy.da.Describe() to get the description dictionary of Data\landcover.img
desc = arcpy.da.Describe(data_path + 'landcover.img')
extent = desc['extent']
llx = extent.XMin
lly = extent.YMin
dx = desc['meanCellWidth']
dy = desc['meanCellHeight']
O = arcpy.Point(llx, lly)
sr = desc['spatialReference']
# get the raster's values (ie the integer values in the cells) and their counts.
# look at landcover.img's attribute table in ArcPro to see what the values and their counts should be
values, counts = np.unique(landcover_raster, return_counts=True)

# create a numpy array filled with zeroes whose shape matches the landcover_raster numpy array from above
reclass = np.zeros(landcover_raster.shape)

# print (hectares) the area occupied by water (category 7)
area_water = counts[values == 7]
print(f'Area of water: {area_water * dx * dy / 10000} hectares')
# create a mask for water
mask_7 = landcover_raster == 7

# use the mask to set the values in the zeros array to 1 for cells with water
reclass[mask_7] = landcover_raster[mask_7]

# convert the reclass numpy array to an arcpy raster
reclass_ras = arcpy.NumPyArrayToRaster(reclass, O, dx, dy)
# set its projection to match that of landcover.img
arcpy.management.DefineProjection(reclass_ras, sr)
# save the raster to the Results directory with a name suggesting it is vegetation
reclass_ras.save(res_path + "vegetation7_reclass.img")

# print (hectares) the area occupied by buildings and roads (category 1 and category 3)
area_buildings_roads = counts[values == 1] + counts[values == 3]
print(f'Area occupied by buildings and roads: {area_buildings_roads * dx * dy / 10000} hectares')

# create a numpy array filled with zeroes whose shape matches the landcover_raster numpy array from above
reclass = np.zeros(landcover_raster.shape)

# repeat for buildings and roads (category 1 and category 3)
mask_1 = landcover_raster == 1
mask_3 = landcover_raster == 3

# use np.logical_or() to OR the masks into a single mask and use it to set the reclassification numpy array.
mask_buildings_roads = np.logical_or(mask_1, mask_3)
reclass[mask_buildings_roads] = landcover_raster[mask_buildings_roads]
# convert the reclass numpy array to an arcpy raster
reclass_ras = arcpy.NumPyArrayToRaster(reclass, O, dx, dy)
# set its projection to match that of landcover.img
arcpy.management.DefineProjection(reclass_ras, sr)
# save the raster to the Results directory with a name suggesting it is vegetation
reclass_ras.save(res_path + "vegetation13_reclass.img")


# create a numpy array filled with zeroes whose shape matches the landcover_raster numpy array from above
reclass = np.zeros(landcover_raster.shape)
# print (hectares) the area occupied grasslands (category 4), for lawns (category 2), and for woods (category 5)
area_lawns_woods = counts[values == 2] + counts[values == 4] + counts[values == 5]
print(f'Area occupied by grasslands, lawns, and woods: {area_lawns_woods * dx * dy / 10000} hectares')
# create a mask for grasslands (category 4), for lawns (category 2), and for woods (category 5)
mask_2 = landcover_raster == 2
mask_4 = landcover_raster == 4
mask_5 = landcover_raster == 5
# use np.logical_or() to OR the three masks into a single mask
# use the mask to set the values in the zeros array to 1
mask_lawns_woods = np.logical_or(mask_2, mask_4, mask_5)
reclass[mask_lawns_woods] = landcover_raster[mask_lawns_woods]

# convert the reclass numpy array to an arcpy raster
reclass_ras = arcpy.NumPyArrayToRaster(reclass, O, dx, dy)

# set its projection to match that of landcover.img
arcpy.management.DefineProjection(reclass_ras, sr)

# save the raster to the Results directory with a name suggesting it is vegetation
reclass_ras.save(res_path + "vegetation245_reclass.img")

print('done.')

# submit screenshots of your reclassification rasters, the rasters themselves, and your script
