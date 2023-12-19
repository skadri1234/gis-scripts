"""
shafeeq kadri
10/4
"""

## INITIALIZE YOUR SCRIPT WITH IMPORTS, DRIVE LETTER, PATHS, ETC.
import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path
## CREATE A SEARCH CURSOR OVER  parking_lots.shp, RETRIEVING THE GEOMETRY OBJECT AND 'LOT_NAME'


with arcpy.da.SearchCursor('parking_lots.shp', ['SHAPE@', 'LOT_NAME', 'FID']) as sc:
    ## for each row in the search cursor...
    for row in sc:
        ## print the name of this parking lot
        FID = row[2]
        print(FID)
        ## store the geometry object in a variable named 'polygon'
        polygon = row[0]
        lot_name = row[1]
        ## get the polygon array from polygon
        polygon_array = polygon.getPart()
        ## create a variable named part_no and set it to zero
        part_no = 0
        ## for each point array in the polygon array...
        for point_array in polygon_array:
            ## print the part number
            print("-" * 80, "\nPart", part_no)
            d_part = 0  # this will hold the perimeter of this part (distance around the outside)
            xy = []  # list of rings
            ring = []  # a list of points in this ring
            ## for each point in this point array...
            for point in point_array:
                if point is None:  # found an inner ring
                    print("HOLE")
                else:  # point hold a legit Point object
                    x, y = point.X, point.Y
                    ring.append([x, y])
                ## if this point is None...
                    ## WHEN WE SEE A None VALUE, WE'RE DONE WITH THE RING WE'VE BEEN WORKING ON SO...
                    ## print the text string "HOLE" to indicate we found a hole

                    ## append ring to xy to store the ring we've been working on

                    ## set ring to an empty list to start the next ring
                    # start a new ring
                ## else (if point is not None)...
                  # point hold a legit Point object
                    # get the x- and y-coordinates from point

                    # append the pair to ring
            xy.append(ring)

            ## WE'RE DONE WITH THIS RING, HOLES AND ALL (IF IT HAD ANY) SO APPEND ring TO xy

            ## NOW WE'RE GOING TO COMPUTE THE PERIMETER OF ring
            ## for each ring in xy...
            for ring in xy:
                # set a variable to the integer value of zero. This variable will hold the perimeter of the ring
                p_ring = 0
                ## sum the distances between every pair of points in the ring. See the video, and it's the same
                ## as how you did it for polylines
                for i in range(len(ring)):
                    x1, y1 = ring[i]
                    x2, y2 = ring[(i + 1) % len(ring)]
                    p_ring += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                ## add the distance around this ring to d_part
                d_part += p_ring

                ## print the distance around this ring to 3 sig. digits
                print(f"Ring {xy.index(ring)} perimeter: {p_ring:.3f}")
            ## print the number of rings and their total length
            print("There are", len(xy), f"rings. total length {d_part:0.3f}")
        ## increment the part number
        part_no += 1


"""
Q
-------------------------------------------------------------------------------- 
Part 0
ring length 115.418
There are 1 rings. total length 115.418
-------------------------------------------------------------------------------- 
Part 0
ring length 574.577
There are 1 rings. total length 574.577
-------------------------------------------------------------------------------- 
Part 0
ring length 97.954
There are 1 rings. total length 97.954
-------------------------------------------------------------------------------- 
Part 0
ring length 26.500
There are 1 rings. total length 26.500
-------------------------------------------------------------------------------- 
Part 0
ring length 26.360
There are 1 rings. total length 26.360
C
-------------------------------------------------------------------------------- 
Part 0
HOLE
HOLE
ring length 483.454
ring length 25.938
ring length 26.379
There are 3 rings. total length 535.772
Y
-------------------------------------------------------------------------------- 
Part 0
ring length 77.553
There are 1 rings. total length 77.553
Z
-------------------------------------------------------------------------------- 
Part 0
HOLE
HOLE
HOLE
HOLE
HOLE
ring length 278.755
ring length 29.968
ring length 93.574
ring length 24.344
ring length 36.151
ring length 24.096
There are 6 rings. total length 486.887
B
-------------------------------------------------------------------------------- 
Part 0
ring length 127.460
There are 1 rings. total length 127.460
N
-------------------------------------------------------------------------------- 
Part 0
ring length 193.936
There are 1 rings. total length 193.936
A
-------------------------------------------------------------------------------- 
Part 0
ring length 172.592
There are 1 rings. total length 172.592
-------------------------------------------------------------------------------- 
Part 0
HOLE
ring length 368.253
ring length 30.976
There are 2 rings. total length 399.229
"""