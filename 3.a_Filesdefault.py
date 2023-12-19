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


# open file, from previous statement, in write mode... 


# define a variable for the line that will be written to the file...
line = "100 250 500\n"      ##  WHY IS THE \n NEEDED?

# write line, from previous statement, to the file...


# define a variable for the next line that will be written to the file... 
line = "1000 1250 1500\n"         ## NOTE: VARIABLES CAN BE REUSED BY ASSIGNING THEM TO NEW VALUES

# write line to the file... 


# close the file...   


## OPEN THE FILE IN NOTEPAD AND CONFIRM THAT IT CONTAINS THE APPROPRIATE DATA. THEN CLOSE NOTEPAD.

##-------------------------------------------------------------
## PART 2: READ FROM A FILE

##-----------
## OPEN FILE AND READ LINE...   

# open the file from PART 1 in read mode... 


# read first line from the file and assign to variable... 
line = 

# print line...


## WHAT SEPARATES THE VALUES IN THE LINE?

##-----------
## SEPARATE THE VALUES IN THE LINE AND STORE IN A LIST...

# split the line, by the appropriate character, to separate the values into a list... 
line =

# print line...


## WHAT IS THE DATA TYPE FOR THE VALUES IN THE LIST?

##-----------
## CONVERT VALUES TO NUMBERS...

# assign variable to first value in the list...
val = 

# convert the value, from line above, to an integer... (not in lecture, learn by example)
val = int(val)      ## int( ) IS A COMMAND THAT CONVERTS STRINGS TO INTEGERS
print('the int value is ', val)

# convert the value, from line above, to a decimal number... (not in lecture, learn by example)
val = float(val)      ## float( ) IS A COMMAND THAT CONVERTS STRINGS OR INTEGERS TO DECIMAL NUMBERS
print('the float value is ', val)

##-----------
## GET NEXT LINE FROM FILE...

# read second line from the file and assign to variable... 
line =

# print line


##-----------
## GET NEXT LINE FROM FILE...

# read the next line from the file and assign to variable... 
line = 

## IN THE PYTHON SHELL, TYPE IN LINE AND HIT ENTER. NOTICE THAT THE LINE IS NOW JUST AN EMPTY STRING - THIS INDICATES YOU HAVE REACHED THE END OF THE FILE.

# close the file...


## A LOOP IS VERY USEFUL WHEN YOU NEED TO READ THROUGH FILES SINCE IT IS A REPETITIVE PROCESS.
