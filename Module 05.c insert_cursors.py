"""
shafeeq kadri
9/30
5c
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
#  Create a variable named <lyr> that holds a copy of LWDS.shp. Name the output layer LWDS_CT.SHP
#  and put it in the TEMP directory...
lyr = arcpy.management.CopyFeatures('LWDS.shp', temp_path + 'LWDS_CT.shp')

# See the manual page for arcpy.Clip_analysis()
# Assign <lyr> the value returned by arcpy.Clip_analysis(). Use <lyr> as the input features,
# TOWNS.SHP as the clip features, and LWDS_CT_clip as the output features...
lyr = arcpy.Clip_analysis(lyr, 'Towns.shp', 'LWDS_CT_clip.shp')

# In a with-statement, create a variable <ic> that is an InsertCursor for <lyr>, with
# AV_LEGEND, LWNAME, LWACTIVE for the field_names...

with arcpy.da.InsertCursor(temp_path + 'LWDS_CT.shp', ('AV_LEGEND', 'LWNAME', 'LWACTIVE')) as ic:
    # insert a row with your own values--not the ones I gave in the video--for the three fields
    ic.insertRow(('my', 'own', 'values'))

## Open the layer in arcpro to verify that the values have been changed
## Take and submit a screen shot of the feature class and the attribute to verify the change.