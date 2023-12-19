"""
Shafeeq Kadri
7ind
"""

import arcpy

dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"

arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path

in_csv = data_path + "PumaPositions.csv"
out_shp = res_path + "WyomingCougars.shp"

# spatial reference UTM zone 12N
sr = arcpy.SpatialReference(26912)

# Create shapefile for wyoming cougars
arcpy.CreateFeatureclass_management(res_path, "WyomingCougars.shp", "MULTIPOINT",
                                    spatial_reference=sr)

# add cougarid and sex fields
arcpy.AddField_management(out_shp, "CougarID", "TEXT")
arcpy.AddField_management(out_shp, "Sex", "TEXT")

# Read through each line in the csv file with readlines method
with open(in_csv) as file:
    lines = file.readlines()

#strip all commas from all lines
header = lines[0].strip().split(',')
rows = [line.strip().split(',') for line in lines[1:]]

# filter for WY and insert records
with arcpy.da.InsertCursor(out_shp, ["CougarID", "Sex", "SHAPE@"]) as ic:
    for row in rows:
        if row[4] == "WY":
            ic.insertRow([row[1], row[3],
                              arcpy.Multipoint(arcpy.Array([arcpy.Point(float(row[7]), float(row[8]))]), sr)])
            #add eastings and northings as xy point data, along with cougarID and sex
