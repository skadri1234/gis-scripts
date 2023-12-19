## INTRO TO GEOPROCESSING

## IN THIS EXERCISE, YOU WILL ACCOMPLISH THE FOLLOWING...
##      1) SET UP ARCPY; DEFINE VARIABLES FOR INPUT DATA
##      2) USE ARCTOOLS TO PERFORM GEOPROCESSING

##---------------------------------------------------------------------

## PART 1: SET UP A GEOPROCESSING SCRIPT ##

## IMPORT MODULES, CREATE AND SET UP ARCPY...

# import the arcpy module
import arcpy

dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path

# allow outputs to be overwritten... 


# assign variables to "middlesexsoils.shp" and "towns.shp" in the Data folder...
soils = "C:/NRE_5585/Data/middlesexsoils.shp"
towns = "C:/NRE_5585/Data/towns.shp"

# set the default geoprocessor workspace to your "Results" folder... 
arcpy.env.workspace = res_path

##----------------------------------------------------------------------

## PART 2: WORKING WITH ARCTOOLS...


##---------------------
## CREATE LAYER CONTAINING TOWN OF HADDAM...

# selection expression for the following Make Feature Layer tool statement...
expression = "TOWN = 'Haddam'"         

# Make Feature Layer tool: use towns for input; "town_lyr" for output; variable in previous line for expression...

lyr = arcpy.MakeFeatureLayer_management(towns, "town_lyr", expression)

##---------------------
## CLIP THE SOILS FILE TO THE "town_lyr" FILE...

# Clip tool: use soils (input); "town_lyr" (clip file); "town_soils.shp" (output) 
arcpy.analysis.Clip(soils, lyr, "town_soils.shp")

##---------------------
## CREATE LAYER CONTAINING HYDRIC SOILS FROM "town_soils.shp"

# selection expression for the following Make Feature Layer tool statement...
expression = "Hydric = 'Yes'"

# Make Feature Layer tool: "town_soils.shp" (input); "town_wetland_lyr" (output); variable in previous line for expression... 
town_wetland_lyr = arcpy.management.MakeFeatureLayer("town_soils.shp", "town_wetland_lyr", expression)

##---------------------
## BUFFER "town_wetland_lyr" BY 100 FEET...

# Buffer tool: "town_wetland_lyr" (input); "wetland_buf.shp" (output); "100 FEET" (distance); "ALL" (dissolve option)... 
arcpy.analysis.Buffer(in_features=town_wetland_lyr, out_feature_class="wetland_buf.shp",
                      buffer_distance_or_field="100 FEET", dissolve_option="ALL")

##---------------------
## ADD "Area" FIELD TO "wetland_buf.shp"...
arcpy.management.AddField("wetland_buf.shp", "Area", "DOUBLE")

# Add Field tool: "wetland_buf.shp" (input); "Area" (field name); "DOUBLE" (field type)... 


##---------------------
## ADD "Area" and "Perimeter" FIELDS TO "wetland_buf.shp"...
arcpy.management.CalculateGeometryAttributes("wetland_buf.shp", [["Area", "AREA"], ["Perimeter", "PERIMETER_LENGTH"]],
                                             length_unit='METERS', area_unit='HECTARES')
## Use arcpy.management.CalculateGeometryAttributes() to add an attribute column named 'area' that holds the polygon's
## area (AREA) in hectares and 'perimeter' that holds the polygon's perimeter's length (PERIMETER_LENGTH) in meters.

##---------------------
## INDICATE THAT SCRIPT HAS FINISHED...

# print message to interactive window...
print("script complete")

## Turn in this script, the shapefile you created, and a screenshot of it in ArcPro