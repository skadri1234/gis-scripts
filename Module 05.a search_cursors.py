"""
Shafeeq Kadri
9/27/23
5A
"""

## INITIALIZE YOUR SCRIPT WITH IMPORTS, DRIVE LETTER, PATHS, ETC.
import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path

## SOME OF THE POINTS IN THE LWDS FEATURE CLASS LAY OUTSIDE OF CONNECTICUT.
## WE WILL CLIP LWDS TO THE TOWNS FEATURE CLASS TO REMOVE THE POINTS OUTSIDE
## CONNECTICUT.

#  See the manual page for arcpy.CopyFeatures_management().
#  We must not make changes to anything in the Data directory, so we start by making a
#  copy of LWDS.shp.
#  Create a variable named <lyr> that holds a copy of LWDS.shp.
#  Use LWDS.shp as the value for in_features, and name the out_feature_class LWDS_CT.SHP
#  and put it in the TEMP directory...

lyr = arcpy.management.CopyFeatures('LWDS.shp', 'LWDS_CT.shp')

# See the manual page for arcpy.Clip_analysis()
# Re-assign <lyr> to be the value returned by arcpy.Clip_analysis(). Use <lyr> as the input features,
# TOWNS.SHP as the clip features, and LWDS_CT_clip as the output features...

lyr = arcpy.Clip_analysis(lyr, 'Towns.shp', 'LWDS_CT_clip.shp')

# Create a dictionary to group AV_LEGEND values by the values in LWFLOW ...

grp = {'GROUND': [], 'SURFACE': []}

# In a with-statement, create a varioble <sc> that is a SearchCursor for <lyr> with 'AV_LEGEND','LWFLOW' for the field names...

with arcpy.da.SearchCursor(lyr, ['AV_LEGEND', 'LWFLOW']) as sc:
    #  for each row in <sc>, append the AV_LEGEND value to the list in the dictionary...
    for row in sc:
        grp[row[1]].append(row[0])

# Print the number of AV_LEGEND values in each LWFLOW group...
print(len(grp['GROUND']))
print(len(grp['SURFACE']))
