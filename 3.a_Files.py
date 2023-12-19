## WORKING WITH FILES

## IN THIS EXERCISE, YOU WILL PERFORM THE FOLLOWING...
##      OPEN A FILE IN WRITE MODE
##      WRITE TO A FILE
##      CLOSE A FILE
##      OPEN A FILE IN READ MODE
##      READ FROM A FILE

##-------------------------------------------------------------
## PART 1: WRITING TO A FILE

# define variable for a new file (use "C:\NRE_5585\Results" as the location)... 
import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path
newfile = 'newfile.csv'


# open file, from previous statement, in write mode... 
fh = open(data_path+'newfile.csv', mode='w')


# define a variable for the line that will be written to the file...
line = "100 250 500\n"      ##  WHY IS THE \n NEEDED?

# write line, from previous statement, to the file...
fh.write(line)


# define a variable for the next line that will be written to the file... 
line = "1000 1250 1500\n"         ## NOTE: VARIABLES CAN BE REUSED BY ASSIGNING THEM TO NEW VALUES

# write line to the file... 
fh.write(line)

# close the file...   
fh.close()

## OPEN THE FILE IN NOTEPAD AND CONFIRM THAT IT CONTAINS THE APPROPRIATE DATA. THEN CLOSE NOTEPAD.

##-------------------------------------------------------------
## PART 2: READ FROM A FILE

##-----------
## OPEN FILE AND READ LINE...   

# open the file from PART 1 in read mode... 
fh = open(data_path+'newfile.csv', mode='r')

# read first line from the file and assign to variable... 
line = fh.readline()

# print line...
print(line)

## WHAT SEPARATES THE VALUES IN THE LINE?

##-----------
## SEPARATE THE VALUES IN THE LINE AND STORE IN A LIST...

# split the line, by the appropriate character, to separate the values into a list... 
line = line[:-1]
line = line.split()

# print line...
print(line)

## WHAT IS THE DATA TYPE FOR THE VALUES IN THE LIST?

##-----------
## CONVERT VALUES TO NUMBERS...

# assign variable to first value in the list...
val = line[0]

# convert the value, from line above, to an integer... (not in lecture, learn by example)
val = int(val)
## int( ) IS A COMMAND THAT CONVERTS STRINGS TO INTEGERS
print('the int value is ', val)

# convert the value, from line above, to a decimal number... (not in lecture, learn by example)
val = float(val)      ## float( ) IS A COMMAND THAT CONVERTS STRINGS OR INTEGERS TO DECIMAL NUMBERS
print('the float value is ', val)

##-----------
## GET NEXT LINE FROM FILE...

# read second line from the file and assign to variable... 
line = fh.readline()

# print line
print(line)


##-----------
## GET NEXT LINE FROM FILE...

# read the next line from the file and assign to variable... 
line = fh.readline()

## IN THE PYTHON SHELL, TYPE IN LINE AND HIT ENTER. NOTICE THAT THE LINE IS NOW JUST AN EMPTY STRING - THIS INDICATES YOU HAVE REACHED THE END OF THE FILE.

# close the file...
fh.close()

## A LOOP IS VERY USEFUL WHEN YOU NEED TO READ THROUGH FILES SINCE IT IS A REPETITIVE PROCESS.
