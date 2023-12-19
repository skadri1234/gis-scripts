import arcpy
import numpy as np
import time

# Set up environment
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path

# Start timer
start = time.time()

# Define the parameters for the Fibonacci lattice
N = 20000000
lonMin = np.radians(-73.0 - 44.0 / 60.)
lonMax = np.radians(-71.0 - 47.0 / 60.)
latMin = np.radians(40.0 + 58.0/60.)
latMax = np.radians(42.0 + 3.0/60.)

# Define the Fibonacci lattice function
def fibLatticeFiltered(N: int, lonMin: float, lonMax: float, latMin: float, latMax: float):
 const = 2 * np.pi
 twopi = 2 * const
 N_latMin = int(np.sin(latMin) * (2.0 * N + 1.0) / 2.0) + 1
 N_latMax = int(np.sin(latMax) * (2.0 * N + 1.0) / 2.0)
 N_values = np.arange(N_latMin, N_latMax)
 lon = const * N_values % twopi - np.pi
 ok_lon = np.logical_and(lon >= lonMin, lon <= lonMax) # list of booleans
 lonNdx_in_range = np.array(N_values[ok_lon])
 lat = np.arcsin((2.0 * lonNdx_in_range) / (2.0 * N + 1.0))
 ok_lat = np.logical_and(lat >= latMin, lat <= latMax)
 lonNdx_in_range = lonNdx_in_range[ok_lat]
 return const * lonNdx_in_range % twopi - np.pi, lat[ok_lat]


# Generate the Fibonacci lattice
lon, lat = fibLatticeFiltered(N, lonMin, lonMax, latMin, latMax)

spRef = arcpy.SpatialReference(6434)

# Open search cursor on wells
wellRows = arcpy.da.SearchCursor("APAWELL", ["FID", "X", "Y"])

# Open file to write results
f = open(res_path + "nearest_neighbors.csv", 'w')
f.write("FID,E,N,Dist(m)\n")

# Process each well
for wellRow in wellRows:
    wellX = wellRow[1]
    wellY = wellRow[2]

    minDist = float("inf")
    nearX = None
    nearY = None

    for i in range(len(lon)):
        point = arcpy.Point()
        point.X = lon[i]
        point.Y = lat[i]
        projectedPoint = point.projectAs(spRef)

        # Compute distance
        xdist = wellX - projectedPoint.X
        ydist = wellY - projectedPoint.Y
        dist = (xdist ** 2 + ydist ** 2) ** 0.5

        # Check if new min
        if dist < minDist:
            minDist = dist
            nearX = lon[i]
            nearY = lat[i]

    # Write results
    f.write("%s,%s,%s,%s\n" % (wellRow[0], nearX, nearY, minDist))

f.close()
print(f"Processing time: {time.time() - start} seconds")