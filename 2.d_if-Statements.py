## WORKING WITH IF STATEMENTS

## IN THIS EXERCISE, YOU WILL PERFORM THE FOLLOWING...
##      CREATE A SIMPLE IF STATEMENT
##      CREATE A MULTI-TEST IF STATEMENT
##      CREATE A COMPLEX COMPOUND STATEMENT

##-----------------------------------------------
## PART 1 - CREATE A SIMPLE (ONE-PART) IF STATEMENT... 

# create a condition...

z = 20

# create an if statement that prints z if z < 25... 
if z < 25:
    print(z)


##-----------------------------------------------
## PART 2 - CREATE A MULTI-TEST IF STATEMENT...
    
##------------
## CREATE A SINGLE MULTI-TEST IF STATEMENT
   
# create a condition...

elevation = 8000

# if elevation is less than or equal to 4000, print "low"... 
if elevation <= 4000:
    print("low")
elif elevation > 4000 <= 8000:
    print("moderate")
else:
    print("high")

# if elevation is greater than 4000 but less than or equal to 8000, print "moderate"... 


# otherwise, print "high"... 


    
## NOTE: THE ABOVE IF STATEMENT SHOULD CONTAIN EACH OF THE FOLLOWING PARTS: THE IF
## PART, THE ELIF PART, THE ELSE PART; THEREFORE, NOTICE THAT THE IF STATEMENT
## CAN SPAN THE COMMENTS. COULD AN ELIF PART BE USED IN PLACE OF THE ELSE PART?

##-----------------------------------------------
## PART 3 - COMPLEX COMPOUND STATEMENTS - A FOR LOOP CONTAINING AN IF STATEMENT...
    
##------------
## FROM THE LIST BELOW, SEPARATE EVEN AND ODD VALUES INTO TWO SEPARATE LISTS...
    
# initial list...

valueList = [34, 65, 89, 67, 109, 90, 76, 86, 55]

# create empty list for even values...

evens = []

# create empty list for odd values...

odds = []

# create for-loop statement, iterate over the list above... 
for i in valueList:
    if i % 2 == 0:
        evens.append(i)
    else:
        odds.append(i)

    # test if value is even. Note: a value is even if it has a remainder of 0 when divided by 2.
	# recall the mod division operator %. Refer back to computations, for a refresher.

    
        # append value to evens list...   
        # (NB: it's more common to just say "add the value to the list")

            
    # if value is not even... 

    
        # append value to odds list...    
                    
   
# print the evens list...
print(evens)

# print the odds list...
print(odds)