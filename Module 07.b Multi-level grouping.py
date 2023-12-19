"""
shafeeq kadri
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
Open eop.shp in ArcPro and label the points with the expression 
$feature.road + '-' + $feature.curb
and turn on the labels. You'll see that the 'road' attribute identifies
which road a point is on (unsurprisingly), and that the 'curb' attribute
puts each point into a group according to the mapper's thinking about which curb
it belongs to.

Remove eop from the contents pane to release the lock ArcPro put on it.

In this exercise will we gather the points in eop.shp into multi-level 
groups in preparation for writing multipoint features later on.
"""

# create an empty dictionary named 'roads'

roads = {}

#create a SearchCursor for eop.shp, reading in the SHAPE@XY, road, and curb attributes
with arcpy.da.SearchCursor('eop.shp', ['SHAPE@XY', 'road', 'group']) as sc:
    # iterate over the search cursor
    for row in sc:
        # extract the x,y coordinates
        x, y = row[0]
        # extract the road name
        road_name = row[1]
        # extract the curb
        group = row[2]
        # if we haven't seen this road name before..
        if road_name not in roads:
            # associate that road name in 'roads' with an empty dictionary
            roads[road_name] = {}
        # if we haven't seen this road-name|curb before...
        if group not in roads[road_name]:
            # associate that curb with an empty list
            roads[road_name][group] = []

        # add the x,y coordinates to the list associated with roads[road_nm][curb]
        roads[road_name][group].append((x, y))

# Print the results:
# for each road...
for road_name, curbs in roads.items():
    # for each curb in this road...
    for curb_name, points in curbs.items():
        print(f"Road: {road_name}, Curb: {curb_name}")
        for x, y in points:
            print(f"  Point: ({x}, {y})")

        # print the road, curb, and coordinates of the point


