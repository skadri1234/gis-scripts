"""
your title block goes here
"""

## INITIALIZE YOUR SCRIPT WITH IMPORTS, DRIVE LETTER, PATHS, ETC.
##
## IMPORT ARCPY AND SET THE WORKSPACE TO THE TEMP DIRECTORY, ETC.
import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = temp_path


WKID = 6433
# Create a point feature class in your TEMP directory named survey_markers.shp referred to SPC83(m)
arcpy.management.CreateFeatureclass(temp_path, "survey_markers.shp", "POINT", spatial_reference = WKID)
# Add a column for PID: str = Permanent Id, a unique identification code for this survey marker
arcpy.management.AddField("survey_markers.shp", "PID", "TEXT")
# Add a column for DESIG: str = "designation" is the common name for a survey marker. it's stamped on the disk
arcpy.management.AddField("survey_markers.shp", "DESIG", "TEXT")

# take a screenshot of your feature class's attribute table in arcpro.
# submit this script and the screenshot