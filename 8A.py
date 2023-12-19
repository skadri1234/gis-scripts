## Your title block goes here

"""
This exercise explores a little about what our GPS-on-puma data can tell us about how these cats spend their time.
Animals apparently establish home ranges in which they live. We can see that the GPS track of any animal shows
"fidelity to place," meaning that they revisit the same places again and again, as opposed to meandering off
across the countryside. Creating the minimum bounding polygon of the GPS points, called a "convex hull,"
establishes the maximum extent of the animal's trek. We can look at the intersections of these polygons to
determine whether the animals co-habitat the same space, which might be different for females and for males.
"""

## Import arcpy and create local path variables. We'll be using the wy_pumas_pnts.shp feature class from before.
## Import tabulate, too

import arcpy
from tabulate import tabulate
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"

arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path

## Create the convex hulls. Use arcpy.management.MinimumBoundingGeometry(). See the manual page for more details
## in_features = wy_pumas_pnts.shp
# out_feature_class = wy_pumas_pgons.shp. Create this feature class in your results directory
# geometry_type='CONVEX_HULL'. There are numerous other choices, which makes this a very handy tool.
# group_field='Cougar_ID. This means to group the points by Cougar_ID, so each cat gets its own polygon.
# group_option='LIST'. Input features will be grouped based on their common values in the specified field or fields
# in the group field parameter.

pgons = arcpy.management.MinimumBoundingGeometry(in_features = "wy_pumas_pnts.shp",
                                                 out_feature_class = res_path + "wy_pumas_pgons.shp",
                                                 geometry_type = "CONVEX_HULL",
                                                 group_option = "LIST",
                                                 group_field = "COUGAR_ID")


## Use arcpy.management.CalculateGeometryAttributes() to add an attribute column named 'area' to the polygon
## feature class we just created. The column will holds the polygon's area in hectares.
## The first argument is the input feature class, the polygons we just created.
## The second argument is a list of lists, called a 'Value Table'. We're only calculating one
## field, so the outer list holds one inner list. The first element of the inner list is the name of the field to add to the
## attribute table, 'area', and the second element is a keyword telling arcpy what to compute, in this case, it's
## 'AREA'. see the manual page for more information.
## The third argument is area_unit='HECTARES', so calculate the area in hectares.

pgons = arcpy.management.CalculateGeometryAttributes(pgons, [["area",'AREA']], area_unit='HECTARES')

## Use arcpy.management.AddField() to add a text field named SEX to wy_pumas_pgons.shp
arcpy.env.workspace = res_path
arcpy.management.AddField("wy_pumas_pgons.shp", "SEX", "TEXT")

"""
We'll now populate the SEX field with each cat's gender.
"""

## Create an UpdateCursor on wy_pumas_pgons.shp with ['COUGAR_ID', 'SEX'] as the field list

with arcpy.da.UpdateCursor("wy_pumas_pgons.shp", ["COUGAR_ID", "SEX"]) as uc:
    # for each row in the update cursor...
    for row in uc:
        # extract the elements of the row into local variables
        COUGAR_ID = row[0]

        # if the first letter of COUGAR_ID is 'M'...
        if COUGAR_ID[0] == 'M':
            row[1] = 'M'
            # set the last (also the second) element of the row to 'M'


        else:
            row[1] = 'F'
            # set the last (also the second) element of the row to 'F'

        # update the attribute table by calling the updateRow() method of the cursor
        uc.updateRow(row)

"""
Now we'll calculate the overlap of all the polygons. We do this by computing the intersection
of the polygons (the intersection is the area the two polygons have in common) and displaying 
it as a percentage of the first polygon's area.
"""

## Create an empty list named ovrlap. This will hold lists of percentage overlap
overlap = []

## Create an emtpy list named nms. This will hold the cats' names.
nms = []

## Create a search cursor for wy_pumas_pgons.shp using ['SHAPE@', 'COUGAR_ID', 'AREA'] for the field list
with arcpy.da.SearchCursor("wy_pumas_pgons.shp", ["SHAPE@", "COUGAR_ID", "AREA"]) as sc:
    # for each row in the search cursor...
    for row in sc:

        # extract the row's elements into local variables
        p1, nm, a1 = row[0], row[1], row[2]

        # create a local variable holding a list containing the cat's name.
        this_row = [nm]

        # append the cats' name to nms
        nms.append(nm)


        # we will now spin through all the polygons again to examine all the pairs.
        # Create another search cursor WITH A DIFFERENT NAME than the one for the outer loop
        # for wy_pumas_pgons.shp using ['SHAPE@', 'COUGAR_ID', 'AREA'] for the field list
        with arcpy.da.SearchCursor(pgons, ['SHAPE@', 'COUGAR_ID', 'AREA']) as sc2:
            # for each row in the search cursor...
            for row2 in sc2:
                # extract the polygon from row into a local variable. don't overwrite the variable in the outer loop!
                p2 = row2[0]
                a2 = row2[2]
                # we don't need to compute the intersection of a polygon with itself. We also can check if
                # the polygons don't touch (are disjoint) and have no intersection.
                # use the p1.equals(p2) method to determine whether the polygons are the equal.
                # use the p1.disjoint(p2) method to determine whether the polygons are disjoint.
                # if they are equal or disjoint,
                if p1.equals(p2) or p1.disjoint(p2):

                    # append a zero to this_row...
                    this_row.append(0)

                    # and continue
                    continue
                # If we get here, these are intersecting, non-equal polygons. Compute their intersection,
                # which we specify to be a Polygon object by using 4 as the 2nd argument to the intersect method.
                inters = p1.intersect(p2, 4)
                # convert the intersection polygon's area to hectares by multiplying by 1e-4
                inters_area = inters.area * 1e-4

                # divide the intersection area by p1's area, convert to percent, and round() to an integer
                overlap_percent = int((inters_area / a1) * 100)

                # append the rounded percentage to this_row
                this_row.append(overlap_percent)

            # after the inner loop is done, append this_row to ovrlap
            overlap.append(this_row)

# print the results using tabulate
print(tabulate(overlap, headers=nms, tablefmt="github"))
# open