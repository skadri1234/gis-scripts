## DICTIONARIES

## IN THIS EXERCISE, YOU WILL PERFORM THE FOLLOWING...
##      READ AND PARSE A FILE HOLDING INFORMATION ABOUT UCONN TREES AND SHRUBS (uconn_woody_plants.csv)...
##      PLACE THE DATA ROWS OF THAT FILE INTO A DICTIONARY KEYED ON TREE_ID
##      ITERATE OVER THE DICTIONARY PRINTING THE ID VALUE AND THE OTHER VALUES FOR THAT TREE
##-------------------------------------------------------------
## PART 1: INITIALIZE YOUR SCRIPT WITH VARIABLES FOR PATHS, ETC
#  The data are stored in uconn_woody_plants.csv in the data directory
#
import arcpy
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = data_path
#  Create an empty dictionary to hold the plants' records. You'll be grouping by <id>

trez = {}

##-------------------------------------------------------------
## PART 2: ITERATE OVER THE FILE, PARSE THE LINES, AND POPULATE THE DICTIONARY

# open the file, and for each line in the file
with open(data_path + "uconn_woody_plants.csv", 'r') as f:
    lines = f.readlines()
    # skip the first record
    for line in lines[1:]:

        # split into columns
        column = line.strip().split(',')


        # parse the line doing all the proper castings.
        tag_no = column[0]
        genus = column[1]
        species = column[2]
        common_name = column[3]
        tree_shrub = column [4]
        multi_stem = column[5]
        memorial = column [6]
        E = float(column[7])
        N = float(column[8])
        tree_height = float(column[9])
        stem_d = int(column[10])
        crown_r = float(column[11])

        # put all the values for the columns into a list, one for each tree

        tree = [tag_no, genus, species, common_name, tree_shrub, multi_stem, memorial, E, N, tree_height, stem_d, crown_r]

    # add this tree to its group in the dictionary, grouping by tree id (second column, Genus)
        if genus not in trez:
            trez[genus] = []

        trez[genus].append(tree)

##-------------------------------------------------------------
## PART 3: ITERATE OVER THE DICTIONARY PRINTING THE GENUS AND THE NUMBER OF TREES IN THIS GENUS

for genus, trees in trez.items():
    print(f"{genus} has {len(trees)} trees in it")

# Aesculus has 15 trees in it
# Magnolia has 53 trees in it
# Gleditsia has 78 trees in it
# Acer has 513 trees in it
