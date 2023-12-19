"""
NRE5585
Defining functions

You'll write function that computes 2-d and 3-d distances between two input points,
and a function to compute grid azimuths
"""

###########################################################
## PART 1: INITIALIZATION

# import whatever modules you need
import numpy as np


###########################################################
## PART 2: WRITE A FUNCTION TO COMPUTE GRID AZIMUTHS

## Write a function to compute grid azimuths. You can just implement the code you
## saw in the video, including the testing code.
twopi = 2 * np.pi
def azimuth(p_from: list, p_to: list, converge=0.0) -> float:
    if p_from == p_to:
        print("p_from cant be equal to p_to")
        return None
    az = (np.arctan2(p_to[0]-p_from[0], p_to[1]-p_from[1]) + converge) % twopi
    return az

print(azimuth([0,0],[0,0]))
angles = np.linspace(0, twopi, 20, endpoint=False)
for angle in angles:
    e = np.sin(angle)
    n = np.cos(angle)
    az = azimuth([0,0], [e,n])
    residual = abs(az - angle)
    if residual > 1e-12:
        print(angle, az, residual)


###########################################################
## PART 3: WRITE A FUNCTION TO COMPUTE GRID DISTANCES

## Write a function to compute grid distances. Include a proper documentation
## string, type hints for the arguments and the return type, and testing
## code guarded with the if __name__... statement. The optional third
## argument <two_D> controls whether this is a 2-d or a 3-d distance. Ie, if
## <two_D> is True, compute a 2-d distance; otherwise computer a 3-d distance.
## 3-d distances are computed from x, y, and z coordinates, so the list
## of coordinates is (at least) length three.
## Your testing code needs to exercise both cases.

## When I wrote the testing code for the azimuth function I
## generated angles, then eastings and northings from those angles, then
## called my azimuth() to compute its version of those angles. In other
## words, I figured out a way to test my function against known values.
## It's not enough to just see that it returns a number--does it return
## the right number?

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


if __name__ == "__main__":
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

