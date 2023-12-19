"""
Shafeeq Kadri
9/17/23
3IND
"""


import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True


arcpy.env.workspace = temp_path
dem = data_path + "DEM.img"
converted_dem = temp_path + "conv_dem.txt"


arcpy.conversion.RasterToASCII(dem, converted_dem)

contours = {}


with open(converted_dem, 'r') as file:
    for row in file:
        fl = row[0]
        if not fl.isnumeric():
            continue

        values = row.strip().split()

        for value in values:
            value = float(value)

            h = int(round(value))

            if h not in contours:
                contours[h] = 0

            contours[h] += 1



for height in sorted(contours.keys()):
    count = contours[height]
    print(f"height {height} has {count} cells")





