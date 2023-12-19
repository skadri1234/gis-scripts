# NESTED LOOPS
# IN THIS EXERCISE, YOU WILL PERFORM THE FOLLOWING...
#      CONVERT A RASTER DIGITAL ELEVATION MODEL (DEM) (dem.img) TO AN ASCII TEXT FILE,
#      CREATE A DICTIONARY TO HOLD THE RESULTS,
#      ITERATE OVER THE CELLS, WHICH ARE ELEVATIONS,
#      ROUND THE ELEVATIONS TO THE NEAREST INTEGER,
#      AND COUNT THE NUMBER OF CELLS HAVE THAT (ROUNDED) ELEVATION...
#      USING THE DICTIONARY

# -------------------------------------------------------------------------------------------------------------

# PART 1: INITIALIZE YOUR SCRIPT: IMPORT arcpy AND CREATE VARIABLES FOR PATHS, ETC
import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True

# create a variable that holds the DEM's path and name
arcpy.env.workspace = temp_path
dem = data_path + "DEM.img"
converted_dem = temp_path + "conv_dem.txt"

# convert the raster to an ASCII text file, putting the result in the temp directory. Do NOT put it in the data dir.
arcpy.conversion.RasterToASCII(dem, converted_dem)

# create an empty dictionary to hold the counts of how many heights are in a particular contour interval
contours = {}  # dictionary mapping elevation -> count

# open the converted_dem file for reading
with open(converted_dem, 'r') as file:
    # iterate over each line in the file
    for row in file:
        fl = row[0]
        if not fl.isnumeric():
            continue

        # split the row into cell values (heights) omitting the terminating \n character
        values = row.strip().split()

        # for each value in the list of values
        for value in values:
            # convert ASCII cell block to float type so we can begin to analyze it
            value = float(value)

            # grab the height in another variable after rounding, then casting to whole integer
            h = int(round(value))

            # if h is not in your dictionary of contours,
            if h not in contours:
                # add it to the dictionary with a count of zero.
                contours[h] = 0

            # now your dictionary definitely has an entry for h, so increment the count for that h
            contours[h] += 1










# PRINT THE RESULTS. eg There are 18102 cells at height 159
for height, count in contours.items():
    print(f"There are {count} cells at height {height}")

# Now we will determine which contour interval has the most cells, and print the contour interval and the count
# create a variable to hold the maximum count seen so far, which, right now, is zero

max_count = 0

#for each height, count pair in the dictionary:
for height, count in contours.items():
    if count > max_count:
        max_count = count
        h = height

print(f"Elevation {h} has the most cells: {max_count}")

# Here's some code that will plot your results to the screen, which is a much better way to understand
# the results. We'll learn more about plotting later on, so this is a bit of foreshadowing
#
# Create a list of the contour intervals, which are the dictionary's key values
intervals = list(contours.keys())
#
# # Create a list of the contour interval counts, which are the dictionary's values
counts = list(contours.values())
#
import matplotlib.pyplot as plt
plt.plot(intervals, counts, 'r+')
plt.title("Distribution of heights")
plt.xlabel("height (m)")
plt.ylabel("number of cells")
plt.show()



