"""
shafeeq kadi
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

# Create a search cursor for 'bldg_corners.shp', retriveing the geometry object (SHAPE@) and FID so ['SHAPE@', 'FID']...

with arcpy.da.SearchCursor('bldg_corners.shp', ['SHAPE@', 'FID']) as sc:
    # for each building feature...
    for row in sc:
        # Print FID
        FID = row[-1]
        print(FID)

        # assign a variable named mp, for "multi-part", the SHAPE@ element in row
        mp = row[0]
        # get the Array of Points by calling mp.getPart()..
        points = mp.getPart()
        # for each point in the part..
        for point in points:
            x = point.X
            y = point.Y

            print(f"x:{x:.3f}, y:{y:.3f}")

            #  print the X- and Y-coordinate to three significant digits
