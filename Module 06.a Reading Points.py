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

## COMPUTE THE CENTROID OF THE LWDS FEATURE CLASS USING SHAPE@XY

# create a search cursor named <sc> for the LWDS feature class with 'SHAPE@XY' as the field_name

with arcpy.da.SearchCursor('LWDS.shp', ['SHAPE@XY']) as sc:
    x_sum = 0
    y_sum = 0
    total_count = 0
    # set up variable to allow you compute the average for the x- and y-coordinates...

    for row in sc:
        #  get the x- and y-coordinates from row
        x, y = row[0]
        x_sum += x
        y_sum += y
        total_count += 1

    x_bar = x_sum / total_count
    y_bar = y_sum / total_count

print(f"x bar:{x_bar:.2f}")
print(f"y bar:{y_bar:.2f}")
        # do whatever you need to do to compute the averages...

    # print the averages to 2 significant digits (xbar 982437.97, ybar 759739.15)

