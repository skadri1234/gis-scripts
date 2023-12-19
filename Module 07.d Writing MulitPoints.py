"""
your title block goes here
"""

## INITIALIZE YOUR SCRIPT WITH IMPORTS, DRIVE LETTER, PATHS, ETC.
import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path
"""
In this exercise we will be creating multipoint features using the eop.shp feature class as input.
eop stands for 'edge of pavement,' and it is a term using by surveyors to denote a point on the
edge of a road. Roads are usually mapped by collecting eop points and then "connecting the dots",
using the eop attribute information to group the points into roads and into segments of roads.

eop.shp has attributes 'road' and 'curb' that create a two-level grouping: first by road, and
then groups within road by which curb the point belongs to.

Let's start with creating the multi-level groupings
"""

## Create an empty dictionary named grps to hold the road groupings.
grps = {}
## Create a search cursor on eop.shp extracting the 'SHAPE@XY','road','curb' attributes
with arcpy.da.SearchCursor('eop.shp', ['SHAPE@XY', 'road', 'group']) as sc:
    ## for each row in the cursor...
    for row in sc:
        ## extract the attributes and put them into variables.
        x, y, road, curb = row[0][0], row[0][1], row[1], row[2]
        ## if the road's name isn't in the dictionary, associate an empty dictionary with this road name
        if road not in grps:
            grps[road] = {}
        ## if the curb's name isn't in the road-name's dictionary, associate an empty list with this curb name
        if curb not in grps[road]:
            grps[road][curb] = []
        ## append the x,y coordinates to this road|curb list
        grps[road][curb].append((x, y))

"""
Now we'll create a new feature class to hold the multipoint features. Call the new MULTIPOINT feature class 
eop_grouped.shp and create it in your results directory. Use State Plane 1983 Connecticut meters FIP 0600 for the spatial
reference. Then add text attribute fields named 'road' and 'curb'.
"""
arcpy.env.workspace = res_path
## Create the feature class
arcpy.CreateFeatureclass_management(out_path=res_path, out_name="eop_grouped.shp", geometry_type="MULTIPOINT", spatial_reference=arcpy.SpatialReference(6433)
                                    )

## use arcpy.management.AddField to add the text field named 'road' to the attribute table
arcpy.AddField_management(in_table="eop_grouped.shp", field_name="road", field_type="TEXT")
## use arcpy.management.AddField to add the text field named 'curb' to the attribute table
arcpy.AddField_management(in_table="eop_grouped.shp", field_name="curb", field_type="TEXT")
"""
Now we create the multipoint features
"""

## create an InsertCursor for your new feature class with attribute list ['SHAPE@', 'ROAD', 'curb']
with arcpy.da.InsertCursor("eop_grouped.shp", ['SHAPE@', 'road', 'curb']) as ic:
    ## for each road name in grps...
    for road_nm in grps:
        ## for each curb in grps[road_nm]
        for curb in grps[road_nm]:
            ## create an arcpy.Array to hold the multipoint feature's points
            point_lst = arcpy.Array()
            ## for each x,y pair in grps[road_nm][curb]
            for x, y in grps[road_nm][curb]:
                ## create an arcpy.Point object with the x,y pair
                point = arcpy.Point(x, y)
                point_lst.add(point)
                ## append the Point to point_lst
            ## create an arcpy.Multipoint object from point_lst
            mp = arcpy.Multipoint(point_lst)
            ## use the insertRow() method of the insert cursor to insert the new feature
            ic.insertRow([mp, road_nm, curb])

## Turn in this script, the shapefile you created, and a screenshot of it in ArcPro

