import arcpy
import numpy as np
import time
start_time = time.time()
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = temp_path
# Load shapefiles
apawell_path = data_path + "APAWELL.shp"
ct_grid_path = temp_path + "ct_grid.shp"
# Create a spatial reference for WKID 6434
sr = arcpy.SpatialReference(6434)
# Load ct_grid points into arrays and project them to the coord system
ct_grid_lon = []
ct_grid_lat = []
with arcpy.da.SearchCursor(ct_grid_path, ["SHAPE@X", "SHAPE@Y"], spatial_reference=sr) as sc:
    for row in sc:
        ct_grid_lon.append(row[0])
        ct_grid_lat.append(row[1])
# Create CSV file for results
csv_path = res_path + "results.csv"
with open(csv_path, "w") as csv_file:
    csv_file.write("FID,E,N,Dist(m)\n")
# Iterate through apawell points
with arcpy.da.SearchCursor(apawell_path, ["FID", "SHAPE@X", "SHAPE@Y"], spatial_reference=sr) as sc:
    for row in sc:
        fid, lon_apawell, lat_apawell = row
        min_distance = np.inf
        closest_lon, closest_lat = 0, 0

        # Find the closest point in ct_grid
        for i in range(len(ct_grid_lon)):
            # Calculate distance in meters using projected coordinates
            distance = np.sqrt((lon_apawell - ct_grid_lon[i]) ** 2 + (lat_apawell - ct_grid_lat[i]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_lon, closest_lat = ct_grid_lon[i], ct_grid_lat[i]

        with open(csv_path, "a") as csv_file:
            csv_file.write(f"{fid},{closest_lon},{closest_lat},{min_distance}\n")

end_time = time.time() - start_time
print(f"Processing time: {end_time} seconds")