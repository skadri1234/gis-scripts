# your title block goes here

## Setup up your drive letter and path variables. (We won't be using arcpy in this exercise.)
## Import pandas as pd and matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"

## Create variables to hold the path+filename for uconn_woody_plants.xlsx. It seems that the Excel file
## has better data in it, so we'll use it.
trez_xl = data_path + "uconn_woody_plants.xlsx"


# create a pandas ExcelFile handle xlsx
with pd.ExcelFile(trez_xl) as xlsx:
    ## use pd.read_excel(xlsx, 'woody_plants', index_col='TAG_NO') to create a DataFrame.
    ## Using TAG_NO as the index column allows us to select plants by their TAG_NO using df.loc[tag_no],
    ## which is similar to how things work with relational databases: selection by primary-key value.
    df = pd.read_excel(xlsx, 'woody_plants', index_col='TAG_NO')

## Print the names of the genera (no duplicates) sorted ascending
## (the plural of 'genus' is 'genera')
genera_names = df['Genus'].unique()
genera_names.sort()
print("Genera Names:")
print(genera_names)
## Print the number of memorial maple trees (maple is genus Acer) (8)
memorial_maple_count = df[(df['Genus'] == 'Acer') & df['Memorial']].shape[0]
print("\nNumber of Memorial Maple Trees (Genus Acer):", memorial_maple_count)

## Print the index values (df.index)
print("\nIndex Values:")
print(df.index)

## Print the record associated with tag number 6000
print("\nRecord for Tag Number 6000:")
print(df.loc[6000])

## Print the last record of the data frame
print("\nLast Record of the DataFrame:")
print(df.iloc[-1])

## Use matplotlib.pyplot to plot in a single plot all the non-memorial trees (df.Memorial == False) as black dots and all
## the memorial trees (df.Memorial == True) as red dots.

non_mem = df[df.Memorial == False]
plt.plot(non_mem.E, non_mem.N, 'ko', label='Non-Memorial')
mem = df[df.Memorial == True]
plt.plot(mem.E, mem.N, 'ro', label='Memorial')
plt.show()
