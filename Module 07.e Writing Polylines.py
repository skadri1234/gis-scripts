"""
shafeeq kadri
"""

"""
In this exercise we will be creating polyline features using the eop_grouped.shp feature class as input.
This is a "connect the dots" workflow in which we have (possibly we created) a point-feature class
that is a collection of points that represent a linear or areal feature. In this example,
we have points that a surveyor collected by walking along a road with a GPS that determined its
position every few meters. Now we turn those points into curb features.
"""

## INITIALIZE YOUR SCRIPT WITH IMPORTS, DRIVE LETTER, PATHS, ETC.
import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = res_path

"""
Create a POLYLINE feature class named curbs_grouped.shp in your results directory. Set 
the spatial reference to SPC83 Connecticut (meters) 0600, then add a TEXT field to the
attribute table named 'ROAD'
"""

## see previous assignment for a code template. Just change MULTIPOINT to POLYLINE
arcpy.CreateFeatureclass_management(out_path=res_path, out_name="curbs_grouped.shp", geometry_type="POLYLINE", spatial_reference=arcpy.SpatialReference(6433))
arcpy.AddField_management(in_table="curbs_grouped.shp", field_name="road", field_type="TEXT")
"""
Now we do the multi-level groupings using the multipoint feature class created in the last assignment.
We'll create one curb feature from each group of points.
"""

## Create an empty dictionary to hold the groups

roads = {}

## Create a search cursor on eop_grouped.shp with 'SHAPE@','road','curb' for the attribute list
with arcpy.da.SearchCursor('eop_grouped.shp', ['SHAPE@', 'road', 'curb']) as sc:
    ## for each row in the cursor
    for row in sc:


        ## assign the contents of the row to variables
        mp, road_nm, curb = row

        ## if the road name isn't in the dictionary, associate an empty list with it
        if road_nm not in roads:
                roads[road_nm] = []

        ## get the Array of Points in mp by calling the getPart() method on the multipoint object

        parts = mp.getPart()

        ## create an empty list to hold the Points in mp

        point_lst = []

        # for each point in points.
        for point in parts:
                point_lst.append(point)

            ## append the point to point_lst


        ## append the point_lst to list associated with road_nm
        roads[road_nm].append(point_lst)

## Create an insert cursor on the new feature class with 'SHAPE@','road' for the attribute list

with arcpy.da.InsertCursor("curbs_grouped.shp", ['SHAPE@', 'ROAD']) as ic:
    ## for each road in roads...
    for road in roads:

        ## assign the list in roads[road] to a local variable
        point_lst = roads[road]
        ## create an arcpy.Array from point_lst
        array = arcpy.Array(point_lst)
        ## create an arcpy.Polyline object from array
        poly = arcpy.Polyline(array)
        ## insert the polyline into the feature class using the insertRow method of the insert cursor
        ic.insertRow([poly, road])

## submit this script, the feature class you created, and a screen shot of it in ArcPro
