import arcpy
import numpy as np
import time
from scipy import constants
start_time = time.time()
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = temp_path


const = 2.0 * np.pi / constants.golden_ratio
twopi = 2.0 * np.pi

def fibLatticeFiltered(N:int, lonMin:float, lonMax:float, latMin:float, latMax:float):
    N_latMin = int(np.sin(latMin)*(2.0*N + 1.0)/2.0) + 1
    N_latMax = int(np.sin(latMax)*(2.0*N + 1.0)/2.0)
    N_values = np.arange(N_latMin, N_latMax)
    lon = const * N_values % twopi - np.pi
    ok_lon = np.logical_and(lon >= lonMin, lon <= lonMax)  # list of booleans
    lonNdx_in_range = np.array(N_values[ok_lon])
    lat = np.arcsin((2.0*lonNdx_in_range) / (2.0*N + 1.0))
    ok_lat = np.logical_and(lat >= latMin, lat <= latMax)
    lonNdx_in_range = lonNdx_in_range[ok_lat]
    return const * lonNdx_in_range % twopi - np.pi, lat[ok_lat]

lonMin = np.radians(-73.00 - 44.00 / 60.)
lonMax = np.radians(-71.00 - 47.00 / 60.)
latMin = np.radians(40.00 + 58.00 / 60.)
latMax = np.radians(42.00 + 3.00 / 60.)

N = 20_000_000
lon, lat = fibLatticeFiltered(N, lonMin, lonMax, latMin, latMax)
lon = np.rad2deg(lon)
lat = np.rad2deg(lat)