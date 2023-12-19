## PARSING FILES

## IN THIS EXERCISE, YOU WILL PERFORM THE FOLLOWING...
##      OPEN A FILE IN READ MODE
##      SKIP THE HEADER LINES
##      READ THE DATA LINES AFTER THE HEADER, PARSING THEM
##      COMPUTE THE AVERAGE WINDSPEED

##-------------------------------------------------------------
## PART 1: INITIALIZE YOUR SCRIPT WITH VARIABLES FOR PATHS, ETC
#
import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path
##-------------------------------------------------------------
## PART 2: ITERATE THROUGH THE CSV FILE, SKIPPING THE HEADER RECORDS, AND COMPUTING
##         THE AVERAGE WIND SPEED
#

## THE FILE IS IN THE WEATHER_DATA SUBFOLDER OF THE DATA DIRECTORY.
## THE FILE'S NAME IS ROVER_TI_3_1H.CSV
# Open the file with a text editor. Notice that the data records begin with a date. All data records' first character
# is a number, and no header records begin with a number. We can use this to discriminate between header
# records and data records. Which column holds windspeed?
# Exit out of the text editor you're looking at the file with.

# create a variable that will count the number of data records in the file
countrecords = 0
# create a variable that will be the sum of all the windspeed values
total_windspeed = 0.0

# open the file in a for-loop statement. Name the index variable 'line' as I did in the slides.

with open(data_path + '/Weather_data/' + 'Rover_TI_3_1h.csv') as file:
    for line in file:
        if line[0].isnumeric():
            line = line.strip('\n')
            values = line.split(',')
            windspeed = float(values[2])
            total_windspeed += windspeed
            countrecords += 1


# this is a data record so parse it
        # get rid of the last character in <line>, the newline character, and ...
        # split the line into a list of values

        # cast the element of the value-list holding the wind speed to a float

        # add the wind speed value to your variable above that is summing the wind speeds

        # increment the variable above you're counting data records with

    # this if-statement does not have an else-clause; it's just the if-statement and its body, so there's
    # nothing else in the for-loop

# compute the average wind speed
avg_windspeed = total_windspeed / countrecords
# print the number of records (85779) and the ws avg (1.312) to three sig. digits and with proper units
print(countrecords)
print(f"{avg_windspeed:.3f}")