## WORKING WITH FOR LOOPS

## IN THIS EXERCISE, YOU WILL PERFORM THE FOLLOWING...
##      CREATE A FOR LOOP
##      USE THE RANGE FUNCTION TO CREATE A SEQUENTIAL LIST

##-----------------------------------------------
## PART 1 - CREATE A FOR LOOP... 

# create a list with the following values: 100,300,500,250...  
alist = [100,300,500,250]

# create a for loop that prints each value in the list... 
for e in alist:
    print(e)

    
# create a for loop that divides each value by 2 and prints the result.
# Note: this should require 3 or less statements...
for e in alist:
    print(e / 2)


    

##-----------------------------------------------
## PART 2 - CREATE A FOR LOOP THAT RUNS A SPECIFIED NUMBER OF TIMES
    
##-------------
## USE THE RANGE FUNCTION TO CREATE SEQUENTIAL LISTS
    
# create the list [0,1,2,3,4,5]
blist = [0,1,2,3,4,5]

# print the list...
print(blist)

##-------------
## USE THE RANGE FUNCTION WITH A FOR LOOP

# create a for loop that runs 10 times, and prints the iteration number. Use the range function to generate the list...
# we can iterate on the value returned by range() directly, without converting it to a list.
for i in range(10):
    print("Iteration:", i)


##-------------
## PART 3: CREATE A FOR LOOP THAT SUMS ALL NUMBERS BETWEEN 10 AND 100 (INCLUSIVE)
## This means compute the sum 10 + 11 + 12 + 13 + ... + 99 + 100
    
# define variable for the total...
total = 0

# create for loop that adds numbers (10-100) to the variable in the line above...
for i in range(10, 101):
    total += i

    
# print total...
print(total)
#woohoo