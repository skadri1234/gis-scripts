## NESTED LOOPS

## IN THIS EXERCISE, YOU WILL PERFORM THE FOLLOWING...
##      CONVERT A RASTER DIGITAL ELEVATION MODEL (DEM) (dem.img) TO AN ASCII TEXT FILE,
##      CREATE A DICTIONARY TO HOLD THE RESULTS,
##      ITERATE OVER THE CELLS, WHICH ARE ELEVATIONS,
##      ROUND THE ELEVATIONS TO THE NEAREST INTEGER,
##      AND COUNT THE NUMBER OF CELLS HAVE THAT (ROUNDED) ELEVATION...
##      USING THE DICTIONARY

##-------------------------------------------------------------
## PART 1: INITIALIZE YOUR SCRIPT: IMPORT arcpy AND CREATE VARIABLES FOR PATHS, ETC
#

# set the workspace to the temp directory
# create a variable that holds the DEM's path and name
# create a variable that holds the converted DEM's path and name. Put it in the 
# temp directory and use a .txt extension
# convert the raster to an ASCII text file, putting the result in the temp directory. 
# Do NOT put it in the data directory
arcpy.conversion.RasterToASCII(

# create an empty dictionary to hold the counts of how many heights are in a particular contour interval
contours = {}  # dictionary mapping elevation -> count

# for each row in the ASCII raster file...
for row in
    #  skip over the header lines

    #  split <row> into cell values (heights) omitting the terminating \n character

    # for each value in the list of values
    for
        # value is a string so cast it to a float

        # round value to the nearest int. round() returns a float, so cast to an int
		h = int(round(value))

        # if h is not in your dictionary

            # add it to the dictionary with a count of zero

        # now your dictionary definately has an entry for h, so increment the count for that h

## PRINT THE RESULTS. eg There are 18102 cells at height 159

for height, count in contours.items():
    print(f"There are {count} cells at height {height}")

## Now we will determine which contour interval has the most cells, and print the contour interval and the count

# create a variable to hold the maximumn count seen so far, which, right now, is zero

max_count = 0

# for each height, count pair in the dictionary:

	# if the count is greater than max_count, 
	
		# set max_count to the count 
		
		# set h to the height

print(f"Elevation {h} has the most cells: {max_count}")

## Here's some code that will plot your results to the screen, which is a much better way to understand
## the results. We'll learn more about plotting later on, so this is a bit of foreshadowing

# Create a list of the contour intervals, which are the dictionary's key values
intervals = list(contours.keys())

# Create a list of the contour interval counts, which are the dictionary's values
counts = list(contours.values())

import matplotlib.pyplot as plt
plt.plot(intervals, counts, 'r+')
plt.title("Distribution of heights")
plt.xlabel("height (m)")
plt.ylabel("number of cells")
plt.show()



