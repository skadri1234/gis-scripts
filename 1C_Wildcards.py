"""
NRE5585 Module 1B
WILD CARDS AND ARCPY.LISTFEATURES
"""

## IN THIS EXERCISE, YOU WILL PERFORM THE FOLLOWING...
##      USE ARCPY.LISTFEATURECLASS WITH AND WITHOUT WILDCARDS

##-------------------------------------------------------------
## PART 1: CREATE THE GEOPROCESSOR...

# import the arcpy module...
import arcpy
# create variables for the drive letter and the path to the Data directory

dl = "C:"
data_path = dl + '/Fall23_Masters/NRE5585/module1/NRE_5585/Data'

# set the arcpy environmental variables for overwriting as True...
# and the workspace is the data directory...
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path


# use arcpy.ListFeatureClasses() to get a list of the names in the Data directory
# for feature classes...

fc_lst = arcpy.ListFeatureClasses()

# print the list
print(fc_lst)

# use arcpy.ListFeatureClasses() with a wildcard string to get a list of the 
# names in the Data directory for feature classes whose name begins with the letter t

fc_t_lst = arcpy.ListFeatureClasses(wild_card='t*')

# print the list
print(fc_t_lst)
print("done")
