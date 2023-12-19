"""
Fibonacci Lattices

From

Basela, Serigo (2018) Fibonacci lattices for the evaluation and optimization of map projections. In
Computers and Geosciences, 117, 1-8.

Thomas H. Meyer (c) Aug 27, 2019
University of Connecticut, Department of Natural Resources and the Environment
"""
import numpy as np
from scipy import constants

const = 2.0 * np.pi / constants.golden_ratio
twopi = 2.0 * np.pi


def fibLattice(N: int):
    """
    Returns np arrays for longitude and latitude for <2N+1> points on a spherical Fibonacci Lattice.
    :param N: int > 0 = number of points to return per hemisphere (North, South).
    :return: [np.array[lon...], np.array[lat...]] Each array is 2N+1 long
    """
    N_values = np.arange(-N, N+1)
    phi = np.arcsin((2.0*N_values) / (2.0*N + 1.0))
    lam = const * N_values % twopi - np.pi
    return lam, phi


def fibLatticeFiltered_slower(N:int, lonMin:float, lonMax:float, latMin:float, latMax:float):
    """
    Returns np arrays for longitude and latitude out of <2N+1> points on a spherical Fibonacci Lattice
    that fall within a bounding box of longitude and latitude.

    Algorthim is brute force: compute all longitudes and latitudes for all 2N+1 points and
    then select those in the box.
    :param N: int > 0 = number of points to return
    :param lonMin: float = minimum longitude, [-pi..pi]
    :param lonMax: float = maximum longitude, [-pi..pi]
    :param latMin: float = minimum latitude, [-pi/2..pi/2]
    :param latMax: float = maximum latitude, [-pi/2..pi/2]
    :return: [np.array[lon...], np.array[lat...]]
    """
    lam, lat = fibLattice(N)
    okLam = np.logical_and(lam >= lonMin, lam <= lonMax)
    okLat = np.logical_and(lat >= latMin, lat <= latMax)
    ok = np.logical_and(okLat, okLam)
    return lam[ok], lat[ok]


def fibLatticeFiltered(N:int, lonMin:float, lonMax:float, latMin:float, latMax:float):
    """
    Returns np arrays for longitude and latitude out of <2N+1> points on a spherical Fibonacci Lattice
    that fall within a bounding box of longitude and latitude.

    Algorthim is to compute all longitudes and select out those in the bounding box. Then compute
    only those latitudes also in the box, which then informs which longitudes to keep.
    :param N: int > 0 = number of points to return
    :param lonMin: float = minimum longitude, [-pi..pi]
    :param lonMax: float = maximum longitude, [-pi..pi]
    :param latMin: float = minimum latitude, [-pi/2..pi/2]
    :param latMax: float = maximum latitude, [-pi/2..pi/2]
    :return: [np.array[lon...], np.array[lat...]]
    """
    N_latMin = int(np.sin(latMin)*(2.0*N + 1.0)/2.0) + 1
    N_latMax = int(np.sin(latMax)*(2.0*N + 1.0)/2.0)
    N_values = np.arange(N_latMin, N_latMax)
    lon = const * N_values % twopi - np.pi
    """
    Find the values from np.arange(-N, N+1) that fall within the longitude range.
    Use longitude because it's a faster computation than latitude, and longitude
    tends to be more restrictive due to convergence of the meridians
    """
    ok_lon = np.logical_and(lon >= lonMin, lon <= lonMax)  # list of booleans
    lonNdx_in_range = np.array(N_values[ok_lon])
    """
    compute latitudes only for longitudes that fall in range
    """
    lat = np.arcsin((2.0*lonNdx_in_range) / (2.0*N + 1.0))
    """
    pick out the latitudes that also fall in range
    """
    ok_lat = np.logical_and(lat >= latMin, lat <= latMax)
    lonNdx_in_range = lonNdx_in_range[ok_lat]
    """
    re-computing longitude is faster than picking it out via
    lon[ok_lon][ok_lat]
    """
    return const * lonNdx_in_range % twopi - np.pi, lat[ok_lat]


if __name__ == '__main__':
    import time
    #  Bounding box for Connecticut
    lonMin = np.radians(-73.0 - 44.0 / 60.)
    lonMax = np.radians(-71.0 - 47.0 / 60.)
    latMin = np.radians(40.0 + 58.0/60.)
    latMax = np.radians(42.0 + 3.0/60.)

    N = 20000000  # 20,000,000 = need 20 million points to get > 1500 in CT
    print('go')
    now = time.clock()
    ans0 = fibLatticeFiltered_slower(N, lonMin, lonMax, latMin, latMax)
    t0 = time.clock()
    ans1 = fibLatticeFiltered(N, lonMin, lonMax, latMin, latMax)
    t1 = time.clock()
    print(len(ans0[0]), len(ans0[1]))
    print(len(ans1[0]), len(ans1[1]))
    print(t1 - now, t1 - t0)
    print(ans1[0] - ans0[0])
    print(ans1[1] - ans0[1])