## WORKING WITH LISTS

## IN THIS EXERCISE, YOU WILL PERFORM THE FOLLOWING...
##      CREATE A LIST
##      RETRIEVE ELEMENTS FROM A LIST
##      ADD ELEMENTS TO A LIST
##      SORT A LIST
##      DELETE ELEMENTS FROM A LIST
##
## BE MINDFUL WHEN YOU'RE WORKING WITH THE LAST ELEMENT
## AND USE THE -1 INDEXING CONVENTION TO ACCESS ELEMENTS
## AT THE END. (-2 FOR THE PENULTIMATE, ELEMENT, ETC.)

##-------------------------------------------
## CREATE A LIST...

# create a list that contains the following numbers: 300,900,150,600,1000,250... 
numlist = [300,900,150,600,1000,250]

##-------------------
## RETRIEVE ELEMENTS FROM A LIST...

# print the first element from the list... 
print(numlist[0])

# print the last element from the list using the -1 index value...
print(numlist[-1])

# print the 3rd element from the list... 
print(numlist[2])

# use a slice to print the first 3 elements from the list...
print(numlist[:3])

# print list... 
print(numlist)

##-------------------
## ADD ELEMENTS TO A LIST...

# add the number 100 to the end of the list... 
numlist.append(100)
print(numlist)
# insert the number 450 at the beginning of the list...
numlist.insert(0, 450)
print(numlist)

# insert the number 100 at position 2 in the list, which means make it the third element...
numlist.insert(2, 100)
print(numlist)
# insert a value of 50 at position 4 in the list, which means make it the fifth element...
numlist.insert(4, 50)
# print list... 
print(numlist)

##-------------------
## SORT A LIST...

# sort the list in ascending order. use the built-in function sorted(list)
sortedlist = sorted(numlist)

# print list... 
print(sortedlist)

##-------------------
## DELETE ELEMENTS FROM A LIST...

# delete the last element from the list... 
del sortedlist[9]

# print list... 
print(sortedlist)

##-------------------
## NESTED LISTS...

# create a nested list...
XY_list = [[500,1000],[750,1500]]

# print the first sublist in XY_list... 
print(XY_list[0])

# print the first element in the first sublist... 
print(XY_list[0][0])

# print the first element in the second sublist... 
print(XY_list[1][0])


# delete the second element in the second sublist... 
del XY_list[1][1]
print(XY_list)
# add the number 2000 to the end of the second sublist... 
XY_list[1].append(2000)

# print list... 
print(XY_list)
