## INTRO TO GEOPROCESSING

## IN THIS EXERCISE, YOU WILL ACCOMPLISH THE FOLLOWING...
##      1) SET UP ARCPY; DEFINE VARIABLES FOR INPUT DATA
##      2) USE ARCTOOLS TO PERFORM GEOPROCESSING

##---------------------------------------------------------------------

## PART 1: SET UP A GEOPROCESSING SCRIPT ##

## IMPORT MODULES, CREATE AND SET UP ARCPY...

# import the arcpy module...

print('begin initialization')
import arcpy

# allow outputs to be overwritten...

arcpy.env.overwriteOutput = True

# create variables to hold strings that give the paths to our standard directories...

data_path = 'C:/Fall23_Masters/NRE5585/module1/NRE_5585/Data'
temp_path = 'C:/Fall23_Masters/NRE5585/module1/NRE_5585/Temp'
res_path = 'C:/Fall23_Masters/NRE5585/module1/NRE_5585/Results'

# use string concatentation (the + operator) to create a new variable that holds the 
# path (data directory) and name of the apawell shapefile...

apawell_fn = data_path + '/apawell.shp'

# use string concatentation (the + operator) to create a new variable that holds the 
# path (results directory) and name of the to-be-created inactive apawell shapefile...

apawell_inactive_fn = res_path + '/apawell_inactive.shp'

print('ended initialization')

# set a varible to hold the where-clause WELLSTATUS = 'INACTIVE'...

where_clause = "WELLSTATUS = 'INACTIVE'"

# use arcpy.SelectLayerByAttribute_management to create a layer holding the inactive wells...

lyr = arcpy.SelectLayerByAttribute_management(apawell_fn, where_clause=where_clause)

# use arcpy.CopyFeatures_management to create the inactive wells shapefile on the disk...

arcpy.CopyFeatures_management(lyr, apawell_inactive_fn)

print("woohoo it worked. alert the press!")

# open ArcPro and look at the shapefile you just created to make sure it's correct...
# either take a screen shot of the shapefile in ArcPro or, if you like, make a simple
# map of it and export as a pdf. Either way, submit the image along with this script