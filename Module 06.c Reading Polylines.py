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

# Create a search cursor for 'curbs.shp', retriveing the geometry object (SHAPE@) and FID...
def distance(p_from: list, p_to: list, two_D: True) -> float:
    if two_D:
        return ((p_to[0] - p_from[0]) ** 2 + (p_to[1] - p_from[1]) ** 2) ** 0.5
    else:
        return ((p_to[0] - p_from[0]) ** 2 + (p_to[1] - p_from[1]) ** 2 + (p_to[2] - p_from[2]) ** 2) ** 0.5

with arcpy.da.SearchCursor('curbs.shp', ['SHAPE@', 'FID']) as sc:
    # for each curb feature...
    for row in sc:
        # Print FID...
        FID = row[-1]
        print(FID)

        # assign the geometry object to a variable named polyline...
        polyline = row[0]

        # get the Array of parts using the getPart() method...
        parts = polyline.getPart()

        # initialize a variable to the integer zero. This variable will hold the total length of each curb
        total_length = 0

        # for each point_array in the array of parts
        for point_array in parts:
            # create an empty list xy to hold the x- and y-coordinates
            xy = []

            # for each point in the part array..
            for point in point_array:
                x,y = point.X,point.Y
                print(f"X: {x:.3f}, Y: {y:.3f}")
                xy.append([x,y])

                #  print the X- and Y-coordinate to three significant digits...


                #  append the coorindates to the xy list


            # calculate the length of this part
            d = 0
            for ndx in range(len(xy) - 1):
                d += distance(xy[ndx], xy[ndx+1], two_D=True)
                print(f"length:{d:.3f}")
                total_length += d
        print(f"length: {total_length:.3f}")
            # print the length

            # add the length of this part to the total

        # print the total length to 3 sig. digits (311.063, 133.706, 104.025)
