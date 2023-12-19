import arcpy
import numpy as np
import time

# Set up the environment
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path


def fibLatticeFiltered(N: int, lonMin: float, lonMax: float, latMin: float, latMax: float):
  const = 2 * np.pi
  twopi = 2 * const
  N_latMin = int(np.sin(latMin) * (2.0 * N + 1.0) / 2.0) + 1
  N_latMax = int(np.sin(latMax) * (2.0 * N + 1.0) / 2.0)
  N_values = np.arange(N_latMin, N_latMax)
  lon = const * N_values % twopi - np.pi
  lon_rad = np.radians(lon) # Convert the longitude values to radians
  ok_lon = np.logical_and(lon_rad >= lonMin, lon_rad <= lonMax) # list of booleans
  lonNdx_in_range = np.array(N_values[ok_lon])
  lat = np.arcsin((2.0 * lonNdx_in_range) / (2.0 * N + 1.0))
  ok_lat = np.logical_and(lat >= latMin, lat <= latMax)
  lonNdx_in_range = lonNdx_in_range[ok_lat]
  lat = lat[ok_lat]
  print(f"lon: {lon}")
  print(f"lat: {lat}")
  print(f"lonNdx_in_range: {lonNdx_in_range}")
  return const * lonNdx_in_range % twopi - np.pi, lat

# Define the bounding box and generate the Fibonacci lattice points
lonMin = np.radians(-73.0 - 44.0 / 60.)
print(f"lonMin:{lonMin}")
lonMax = np.radians(-71.0 - 47.0 / 60.)
print(f"lonMax:{lonMax}")
latMin = np.radians(40.0 + 58.0/60.)
print(f"latMin:{latMin}")
latMax = np.radians(42.0 + 3.0/60.)
print(f"latMax:{latMax}")

N = 20000000
lon_fib, lat_fib = fibLatticeFiltered(N, lonMin, lonMax, latMin, latMax)
print(f"lon_fib, lat_fib: {lon_fib},{lat_fib}")
# Convert the longitudes to decimal degrees (DD)
# Convert the latitudes to decimal degrees (DD)
lon = np.rad2deg(lon_fib)
lat = np.rad2deg(lat_fib)
print(f"lon, lat:{lon},{lat}")

# Convert the Fibonacci lattice points to a numpy array
fib_points = np.column_stack((lon, lat))
print(f"fib_points:{fib_points}")
# Start the timer
start_time = time.time()

# Open the shapefile
with arcpy.da.SearchCursor("APAWELL.shp", ["FID", "SHAPE@"]) as cursor:
    desc = arcpy.Describe("APAWELL.shp")
    print(f"Shapefile bounding box: {desc.extent}")
    #Open the CSV file
    with open(res_path + "output.csv", "w") as outfile:
       # Write the header
       outfile.write("FID,E,N,Dist(m)\n")
       # Loop through each row in the shapefile
       for row in cursor:
           # Get the FID and the point
           fid = row[0]
           point = row[1]
           x = point.firstPoint.X
           y = point.firstPoint.Y
           # Convert the point to a numpy array
           point = np.array([x, y])
           print(f"Shape of 'point': {point.shape}")
           print(f"Content of 'point': {point}")
           # Find the nearest lattice point
           dists = np.sqrt((fib_points[:, 0] - point[0])**2 + (fib_points[:, 1] - point[1])**2)
           min_index = np.argmin(dists)
           min_dist = dists[min_index]
           # Write the results to the CSV file
           outfile.write(f"{fid},{fib_points[min_index, 0]},{fib_points[min_index, 1]},{min_dist}\n")

# Stop the timer and print the elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")