"""
shafeeq kadri
10/4
"""

import arcpy

dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path

def distance(p_from: list, p_to: list, two_D: True) -> float:
    if two_D:
        return ((p_to[0] - p_from[0]) ** 2 + (p_to[1] - p_from[1]) ** 2) ** 0.5
    else:
        return ((p_to[0] - p_from[0]) ** 2 + (p_to[1] - p_from[1]) ** 2 + (p_to[2] - p_from[2]) ** 2) ** 0.5
## CREATE A SEARCH CURSOR OVER parking_lots.shp, RETRIEVING THE GEOMETRY OBJECT AND 'LOT_NAME'
with arcpy.da.SearchCursor('parking_lots.shp', ['SHAPE@', 'LOT_NAME', 'FID']) as sc:
    ## for each row in the search cursor...
    for row in sc:
        FID = row[2]
        lot_name = row[1]
        polygon = row[0]

        ## get the polygon array from polygon
        polygon_array = polygon.getPart()
        part_no = 0

        ## for each point array in the polygon array...
        for point_array in polygon_array:
            print("-" * 80, "\nPart", part_no)
            d_part = 0  # Initialize perimeter of this part
            xy = []  # List to store rings
            ring = []  # List to store points in this ring

            ## for each point in this point array...
            for point in point_array:
                if point is None:  # Found an inner ring (hole)
                    print("HOLE")
                else:  # Point holds a valid Point object
                    x, y = point.X, point.Y
                    ring.append([x, y])

            ## We're done with this ring, holes and all (if it had any), so append ring to xy
            xy.append(ring)

            ## Now we're going to compute the perimeter of the ring
            for ring in xy:
                p_ring = 0  # Initialize the perimeter of this ring

                ## Sum the distances between every pair of points in the ring
                for i in range(len(ring)):
                    x1, y1 = ring[i]
                    x2, y2 = ring[(i + 1) % len(ring)]  # Wrap around to the first point
                    p_ring += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

                ## Add the distance around this ring to d_part
                d_part += p_ring

                ## Print the distance around this ring to 3 sig. digits
                print(f"Ring {xy.index(ring)} perimeter: {p_ring:.3f}")

            ## Print the number of rings and their total length
            print(f"{lot_name} has {len(xy)} rings. Total perimeter: {d_part:.3f}")

        ## Increment the part number
        part_no += 1