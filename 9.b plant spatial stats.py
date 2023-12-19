## GROUPING TREES TOGETHER BY GENUS AND COMPUTING SPATIAL STATISTICS FOR EACH GROUP

## IN THIS EXERCISE, YOU WILL PERFORM THE FOLLOWING...
##      READ AND PARSE A FILE HOLDING UCONN CAMPUS TREE INFORMATION...
##      GROUP THE RECORDS BY GENUS...
##      COMPUTE THE CENTROID OF EACH GROUP...
##      COMPUTE THE AVERAGE DISTANCE OF EACH INDIVIDUAL PLANT TO ITS GROUP'S CENTROID
##-------------------------------------------------------------

## PART 1: INITIALIZE YOUR SCRIPT WITH VARIABLES FOR PATHS, ETC
import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path

# create a variable that holds the tree file's path and name
tree_file = data_path + "uconn_woody_plants.csv"

## READING THE DATA FROM THE CSV FILE

# open the file and use readline() to read the first line, which holds the names of the columns
# calling readline() skips the header line so we don't have to monkey around with it in the processing loop
with open(tree_file, 'r') as fh:
    header = fh.readline().strip().split(',')
    lines = fh.readlines()

## SPIN THROUGH THE DATA RECORDS AND POPULATE THE DICTIONARY

trez = {}  # create an empty dictionary to hold the groups

for line in lines:  # readline() above has read the header record, so <line> holds only data records hereafter
    # parse the lines
    columns = line.strip().split(',')
    genus = columns[1]
    e = float(columns[7])
    n = float(columns[8])
    # if the genus of this tree isn't in <trez>, add an element to trez: genus -> []
    if genus not in trez:
        trez[genus] = []

    # put the easting and northing values into a list and append it to the list in trez[genus]
    trez[genus].append([e, n])

# the code after here does not belong in the for-loop you just wrote.

## COMPUTE THE CENTROID FOR EACH GENUS
#  The centroid of a data set is simply the point (e_bar, n_bar) where
#  e_bar = mean(eastings) and n_bar = mean(northings)

centroids =  {} # create an empty dictionary to hold the centroids


for genus, enlist in trez.items():  # iterate over trez to get the eastings and northings for each genus
    # Your elements in <trez> look like easting,northing pairs, so trez[genus] looks like
    # [[e,n], [e,n], ..., [e,n]]
    e, n = zip(*enlist)# use zip(* ...) to produce a list of eastings <e> and a list of northing <n>

    # compute the average easting <e_bar> and the average northing <n_bar>
    e_bar = sum(e) / len(e)
    n_bar = sum(n) / len(n)

    centroids[genus] = e_bar, n_bar  # store this group's centroid in the <centroids> dictionary as a tuple

    print(f'{genus} has {len(e)} plants and a centroid at {e_bar:0.1f}, {n_bar:0.1f}')

"""
Aesculus has 15 plants and a centroid at 346237.1, 261018.1
Magnolia has 53 plants and a centroid at 346247.2, 260892.8
Gleditsia has 78 plants and a centroid at 346271.0, 260755.5
...
"""

## COMPUTE THE AVERAGE DISTANCE OF EACH TREE FROM ITS GROUP'S CENTROID

# iterate over <centroids> to get the centroid for each genus
for genus, centroid in centroids.items():  # Iterate over centroids to get the centroid for each genus
    e_bar, n_bar = centroid  # Get the centroid (e, n) from centroids
    distances = []

    # for each tree in the genus for this centroid...
    for e, n in trez[genus]:
        # get this tree's position (e,n)
        distance = ((e - e_bar) ** 2 + (n - n_bar) ** 2) ** 0.5

        # compute how far this point is from its genus's centroid
        distances.append(distance)

    # compute the average distance of all trees in this genus to its genus's centroid
    d_bar = sum(distances) / len(distances)
    
    print(f'Mean distance to centroid for {genus} is {d_bar:0.1f}')

"""
Mean distance to centroid for Aesculus is 331.0
Mean distance to centroid for Magnolia is 327.5
Mean distance to centroid for Gleditsia is 522.6
...
"""
