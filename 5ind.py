"""
shafeeq kadri
9/30
5ind
"""
import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path

# 1. Create a copy of LWDS.shp in the Results directory
lyr = arcpy.management.CopyFeatures('LWDS.shp', res_path + 'LWDS_CT.shp')

# 2. Compute and print the centroid of the features, SHAPE@XY makes this easier
centroid = arcpy.management.FeatureToPoint(lyr, 'LWDS_Centroid.shp', 'CENTROID')
x_sum = 0
y_sum = 0
total_count = 0

with arcpy.da.SearchCursor(lyr, ['SHAPE@XY']) as sc:
    for row in sc:
        x_centroid, y_centroid = row[0]
        x_sum += x_centroid
        y_sum += y_centroid
        total_count += 1

centroid_avg_x = x_sum / total_count
centroid_avg_y = y_sum / total_count
print(f"centroid: ({centroid_avg_x:.3f}, {centroid_avg_y:.3f})")

# 3. Find and print the minimum and maximum distances from each LWDS feature to the centroid and the range

min_dist = float("inf")  # Initialize min_dist to positive infinity
max_dist = 0

with arcpy.da.SearchCursor(lyr, ['SHAPE@XY']) as sc:
    for row in sc:
        x, y = row[0]
        distance = ((x - centroid_avg_x) ** 2 + (y - centroid_avg_y) ** 2) ** 0.5
        if distance < min_dist:
            min_dist = distance
        if distance > max_dist:
            max_dist = distance
print(f"min distance to centroid: {min_dist:.3f}")
print(f"max distance to centroid: {max_dist:.3f}")

range_dist = max_dist - min_dist
print(f"range is {range_dist:.3f}")

# Set the value for DESCRIP2 in your feature class to “lower”, “middle,” or “upper”
with arcpy.da.UpdateCursor(lyr, ["SHAPE@XY", "DESCRIP2"]) as uc:
    for row in uc:
        x, y = row[0]
        distance = ((x - centroid_avg_x) ** 2 + (y - centroid_avg_y) ** 2) ** 0.5
        if min_dist <= distance < (min_dist + range_dist / 3):
            row[1] = "lower"
        elif (min_dist + range_dist / 3) <= distance < (min_dist + 2 * range_dist / 3):
            row[1] = "middle"
        else:
            row[1] = "upper"
        uc.updateRow(row)

lowercount = 0
middlecount = 0
uppercount = 0

with arcpy.da.SearchCursor(lyr, ["DESCRIP2"]) as sc:
    for row in sc:
        if row[0] == "lower":
            lowercount += 1
        if row[0] == "middle":
            middlecount += 1
        if row[0] == "upper":
            uppercount += 1
print(f"lower count:{lowercount}, middle count:{middlecount}, upper count:{uppercount}")


