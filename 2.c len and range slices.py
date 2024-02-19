"""
shafeeq kadri
"""

## IN THIS EXERCISE YOU WILL IMPORT A DEM INTO A NUMPY ARRAY...
## COMPUTE THE AVERAGE HEIGHT OF EACH ROW...
## COMPUTE THE AVEERAGE HEIGHT OF THE ENTIRE DEM

# import arcpy, set up variables for your drive letter and data path. Set the workspace to the data directory...

import arcpy

dl = "C:/"
data_path = "NRE_5585/Data/"

## This statement verifies if your path is correct
assert dl + data_path == dl + "NRE_5585/Data/", f'your path is {dl + data_path} but it should be {dl + "NRE_5585/Data/"}'

#  Open arcpro and look at dem.img. It's always a good idea to visualize your data.
#  Use arcpy.RasterToNumPyArray('dem.img') to import the dem into a variable named np_dem...

raster = arcpy.Raster('C:/NRE_5585/Data/DEM.img')
np_dem = arcpy.RasterToNumPyArray(raster)

##  the dem is organized as a two-dimensional array. The rows hold heights that
##  run east-west, and row zero is at the north. So the rows are ordered north to south, and the columns
##  are ordered west to east. Not all dems are organized like this so you need to take care in this regard.
##  How can you determine how a dem is organized by using arcpro?
#  create and print a variable to store len(np_dem), which is the number of rows in the dem...

n_rows = len(np_dem)
print(n_rows)

#  create and print a variable to store len(np_dem[0]), which is the number of columns per row. (NB this is assuming
#  that every row has the same number of columns...

n_cols = len(np_dem[0])
print(n_cols)

## First, let's compute the average height per row. The last row is 149.605 m
## np_dem is a list of lists: [row0, row1, ... , row999] where
## each row is a list of 1000 heights
## row0 = [h00, h01, h02, ... , h0999]
## row1 = [h10, h11, h12, ... , h1999]
## write a for-statement to iterate over the rows in np_dem:

for row in np_dem:
    # assign a variable named total the value of zero.
    total = 0
    # write a for-statement to iterate over each height in row...
    for h in row:
        # add h to total
        total = total + h
    # the average height for this row is total / n_cols
avg_height_per_row = total / n_cols
    # print this row's average height to 3 sig. digits
print(f"the avg height of this row is {avg_height_per_row: .3f}")

## Now, let's compute the average height of the whole dem. 170.121 m
## Assign zero to be the variable total's value
total = 0
## write a for-statement to iterate over the rows in np_dem:
for row in np_dem:
    for h in row:
        total += h
    # write a for-statement to iterate over each height in row...
        # add h to total
# print dem's average height to 3 sig. digits
avg_height_dem = total / (n_cols * n_rows)
print(f"avg height of dem is {avg_height_dem: .3f}")
################################################################ EXTRA CREDIT 1 PTS

## Our goal is compute the mean height of the dem a different way.
## numpy arrays have a method named flatten() that will reshape the array into a one-dimensional list.
# Invoke np_dem.flatten() and save the result in a variable named dem...

#dem = np_dem.flatten()

#  Print the number of elements in dem using len(dem). You'll see it's 1,000,000, which verifies that it's just a flat list now...


#  Write a for-loop to compute the mean height of the dem. Print the height to 3 digits. (170.121 m)...

# set total to zero

# iterate over dem and add all the heights in dem to total

# the mean value is total / the number of heights in dem. Print the mean height to 3 sig. digits. Compare with
# the value above to verify they are the same


################################################################ EXTRA CREDIT 2 PTS

## COMPUTE AND PRINT THE MEAN HEIGHT FOR EACH ROW

## HAVING FLATTENED DEM, WE'LL NEED TO PROCESS IT IN SLICES ONE ROW LONG. THE FIRST SLICE IS
## 0..999, THE SECOND IS 1000..1999, ETC. WE'LL USE THE range() FUNCTION TO GENERATE THE PROPER
## STARTING INDEX VALUES, NAMELY, 0, 1000, 2000, 3000, ..., 999000
#  Write a for-statement with index variable r_ndx that iterates over the range starting at zero,
#  ending at len(dem), in steps equal to the number of columns per row...

#for r_ndx in range(0, len(dem), n_cols):
    ## COMPUTE THE MEAN FOR DEM ELEMENTS r_ndx through r_ndx+n_cols
    # set total to zero...

    # write a for-statement with index variable h that iterates over dem using a slice starting at
    # r_ndx : r_ndx + n_cols, and add h to total...
    #for h in dem[
        # add h to total

    # compute this row's average as total divided by n_cols...

    # print this row's mean height to 3 sig.dig. (1 has 181.300, 2 has 181.316, ..., 1000 has 149.605)...
    #print(
