"""
NRE5585
Defining a library module

You'll write your utility functions in this file from here on out.

This file is a module. You use it by putting the following line in another one of your scripts:

import lib5585

Feel free to import with an alias (import lib5585 as ...) or (from lib5585 import *), if you wish.

This file has testing code embedded in it. You'll find the (rather odd) statement:
if __name__ == '__main__':  # this is the start of a testing block

This if-statement prevents the testing code from being run when you import this file from another file.
However, if you run this file, all the testing code will be run. If the tests work properly, nothing
gets printed to the console. If there's a problem, things will be printed to the console. Do not delete
or change the testing code. It's there for your benefit and for mine.

I give you either the entire function declaration or just the name so that
my testing code will work properly.
"""

###########################################################
## PART 1: INITIALIZATION

# import whatever things you need
import numpy as np


###########################################################
## PART 2: WRITE VARIOUS FUNCTIONS
if __name__ == '__main__':
    print("testing lib5585")

## copy your distance function from the previous assignmment here
def distance(p_from: list, p_to: list, two_D: True) -> float:
    """
        Computing grid distances between two points.

        Arguments:
            p_from (list): A list representing the coordinates of the starting point.
            p_to (list): A list representing the coordinates of the ending point.
            two_D (boolean, optional): Controls whether to compute a 2D or 3D distance.
                If True, computes a 2D distance; if False, computes a 3D distance.

        Returns:
            float: The computed grid distance.

        Note:
            - For 2D distances, the input lists should have at least two elements (x and y coordinates).
            - For 3D distances, the input lists should have at least three elements (x, y, and z coordinates).

        Examples:
            p1 = [1, 2]
            p2 = [4, 6]
            distance(p1, p2)
            Answer should be 5.0,
            sqrt((4 - 1)^2 + (6 - 2)^2) = 5

            p3 = [0, 0, 0]
            p4 = [1, 1, 1]
            distance(p3, p4, two_D=False)
            Answer should be 1.7320508075688772, the square root of 3,
            the correct 3D Euclidean distance between 0,0,0 and 1,1,1
        """
    if two_D:
        return ((p_to[0] - p_from[0]) ** 2 + (p_to[1] - p_from[1]) ** 2) ** 0.5
    else:
        return ((p_to[0] - p_from[0]) ** 2 + (p_to[1] - p_from[1]) ** 2 + (p_to[2] - p_from[2]) ** 2) ** 0.5
## copy your azimuth function from the previous assignment here
twopi = 2 * np.pi
def azimuth(p_from: list, p_to: list, converge=0.0) -> float:
    if p_from == p_to:
        print("p_from cant be equal to p_to")
        return None
    az = (np.arctan2(p_to[0]-p_from[0], p_to[1]-p_from[1]) + converge) % twopi
    return az
## write a function that takes a dmss list and converts it to an angle. Return either in
## radians (default) or decimal degrees.
## a dmss list is a list (or tuple) like [degrees:int, minutes:int, seconds:float, sign:-1 or 1]
## eg, [72,15,02.04187,-1] is -(72 + 15/60 + 02.04187/3600) = -72.25056718611111
## optional argument <units> can be either 'radians' or 'DD'
## Also, see to_dmss() below. Your code should obey the following:
##
## angle == from_dmss(to_dmss(angle))

def from_dmss(dmss:list, units='radians')->float:
    degrees, minutes, seconds, sign = dmss
    dd = sign * (degrees + minutes / 60 + seconds / 3600)
    if units == 'radians':
        return np.deg2rad(dd)
    else:
        return dd


###########################################################
## PART 3: HERE ARE SOME HANDY FUNCTIONS I'M PROVIDING YOU
## TO GIVE SOME MORE EXAMPLES OF WRITING FUNCTIONS


def to_dmss(angle: float) -> list:
    """
    Takes the angle in radians and returns [d, m, s, sign]
    angle: float = angle in radians to convert.
    return: [d, m, s, sign] where
    d: int = [0, 360), degrees
    m: int =  [0, 60), minutes
    s: float = [0, 60), decimal seconds
    sign: int = +1 or -1 for non-negative, negative angles
    """
    dd = np.rad2deg(angle)
    if dd < 0:
        sgn = -1
        dd = -dd  # make it positive
    else:
        sgn = 1
    d = np.trunc(dd)  # integer degrees
    m = np.trunc(60 * (dd - d))
    s = 3600 * (dd - d - m / 60)
    return [d, m, s, sgn]


def pp_dmss(dmss: list, kind='azimuth') -> str:
    """
    Pretty-print a dmss list. See to_dmss()
    kind: str = controls the value in <sign>. If kind == 'azimuth', then <sign> is either '+' or '-'.
    If kind == 'lat', then <sign> is either 'N' or 'S'. If kind == 'lon', then <sign> is either 'E' or 'W'.
    return: ddd-mm-ss.ss or ddd-mm-ss.sssss
    """
    d, m, s, sgn = dmss
    if kind == 'azimuth':
        return f"{int(d):03d}-{int(m):02d}-{s:05.2f} ({'+' if sgn > 0 else '-'})"
    elif kind == 'lat' or kind == 'lon':
        return f"{int(d):03d}-{int(m):02d}-{s:.5f} ({'N' if sgn > 0 else 'S'})" if kind == 'lat' else f"{int(d):03d}-{int(m):02d}-{s:.5f} ({'E' if sgn > 0 else 'W'})"

def en2rc(easting, northing, origin_easting, origin_northing, cellsize):
    """
    Convert eastings and northings to row and column index values for a raster.
    """
    col = int((easting - origin_easting) / cellsize)
    row = int((origin_northing - northing) / cellsize)
    return row, col

if __name__ == '__main__':
    # Test 2D distance
    p1 = [1, 2]
    p2 = [4, 6]
    d_2d = distance(p1, p2, two_D=True)
    print(f"2D Distance: {d_2d}")

    # Test 3D distance
    p3 = [0, 0, 0]
    p4 = [1, 1, 1]
    d_3d = distance(p3, p4, two_D=False)
    print(f"3D Distance: {d_3d}")

    # Test azimuth function
    p5 = [0, 0]
    p6 = [1, 1]
    az = azimuth(p5, p6)
    print(f"Azimuth: {az}")

    # Test from_dmss function
    angle_dd = from_dmss([72, 15, 02.04187, -1], units='DD')
    angle_rad = from_dmss([72, 15, 02.04187, -1], units='radians')
    print(f"Angle in Decimal Degrees: {angle_dd}")
    print(f"Angle in Radians: {angle_rad}")

    # Test to_dmss function
    angle = np.deg2rad(-72.25056718611111)
    dmss_angle = to_dmss(angle)
    print(f"Angle in DMSS: {dmss_angle}")

    # Test pp_dmss function
    pp_angle = pp_dmss(dmss_angle)
    print(f"Pretty Printed Angle: {pp_angle}")
    # Test en2rc function
    origin = [5000, 1000]
    cellsize = 10
    nrows = 1000
    ncols = 1000
    en_coord = [5010, 990]
    rc = en2rc(en_coord[0], en_coord[1], origin[0], origin[1], cellsize)
    print(f"Row, Column for ({en_coord[0]}, {en_coord[1]}): {rc}")

