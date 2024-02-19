# Your title block goes here
"""
shafeeq kadri
"""
## INTRO TO NUMPY

## IN THIS EXERCISE, YOU WILL ACCOMPLISH THE FOLLOWING...
##      1) CREATE TWO 3-D POINT DATA SETS
##      2) COMPUTE THE HORIZONTAL DISTANCES BETWEEN THE POINT PAIRS
##      3) COMPUTE THE SLOPE DISTANCES BETWEEN THE POINT PAIRS
##      4) COMPUTE THE SLOPES (PERCENT) BETWEEN THE POINT PAIRS
##      5) COMPUTE THE AZIMUTHS BETWEEN THE POINT PAIRS


##---------------------------------------------------------------------

## PART 1: CREATE TWO 3-D POINT DATA SETS ##

# import numpy as np...

import numpy as np

# import the normal random number method as 'normal'

from numpy.random import normal

# create a variable n_pts that holds the number of points to create = 20
n_pts = 20

# create and print two unit normal 3-D point sets in column orientation, so shape=(3, n_pts)

p1 = normal(size=(3, n_pts))
p2 = normal(size=(3, n_pts))
print('p1:', p1)
print('p2:', p2)
## PART 2: COMPUTE THE HORIZONTAL (2-D) DISTANCES BETWEEN THE POINT PAIRS ##

# dH involves only the x- and y-coordinates
dH = np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
print('dH:', dH)

## PART 3: COMPUTE THE SLOPE (3-D) DISTANCES BETWEEN THE POINT PAIRS ##
## Extra credit (1 pt) Write a single line that will work properly regardless of how
## many dimensions the points have (i.e., it works correctly--without modification-- for
## 2-d, 3-d, 69-d, etc., points.

# dS involves the x-, y-, and z-coordinates
dS = np.sqrt(np.sum((p1 - p2)**2, axis=0))
print('dS:', dS)

# assert that all the slope distances are greater than the horizontal distances

assert np.all(dS > dH)

## PART 4: COMPUTE THE SLOPES (DD) BETWEEN THE POINT PAIRS ##
## SLOPE IS RISE / RUN. dH ALREADY HOLDS THE 'RUN', WHICH IS CONVENIENT

# assert that all the dH values are not zero so that dividing by them doesn't cause a crash

assert np.all(dH != 0)

## compute the slope as arctangent of change-in-z divided by change-in-horizontal distance between the points.
## this is a single statement

slope = np.arctan2(p2[2] - p1[2], dH)

## print slope in decimal degrees
print('slope:', np.rad2deg(slope))

## PART 5: COMPUTE THE AZIMUTHS BETWEEN THE POINT PAIRS IN THE RANGE[0, 360) ##
## RECALL THAT AZIMUTH = ARCTAN2( dx, dy )
azimuth = np.rad2deg(np.arctan2(p2[0] - p1[0], p2[1] - p1[1]))
azimuth[azimuth < 0] += 360

print('azimuth:', azimuth)


## PRINT THE AZIMUTHS AND THE X-, Y- COORDINATES OF THE LAST TWO POINTS OF YOUR DATA SETS. MAKE
## SURE YOUR ANSWER LOOKS RIGHT

print(p1[0,-1], p1[1,-1])
print(p2[0,-1], p2[1,-1])

print('script completed, yo')
