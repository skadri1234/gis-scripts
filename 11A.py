# your title block goes here
import pandas as pd
## Setup up your drive letter and path variables. (We won't be using arcpy in this exercise.) Import pandas as pd
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"

## Create variables to hold the path+filename for uconn_woody_plants.xlsx and for uconn_woody_plants.csv
trez_xl = data_path + "uconn_woody_plants.xlsx"
trez_csv = data_path + "uconn_woody_plants.csv"

## use pd.read_csv(...) to create a DataFrame holding uconn_woody_plants.csv
df_csv = pd.read_csv(trez_csv)

# create a pandas ExcelFile handle xlsx
with pd.ExcelFile(trez_xl) as xlsx:
    ## use pd.read_excel(xlsx, ...) to create a DataFrame holding the woody_plants sheet from uconn_woody_plants.xlsx
    df_xl = pd.read_excel(xlsx,  sheet_name='woody_plants')

# print the Excel-based DataFrame
print("DataFrame from Excel:")
print(df_xl)

# print df_xl == df_csv
print(df_xl == df_csv)

## It strikes as as rather odd that the Tree_Height and Crown_Radius columns are not equal. I suspect that
## the values in those columns got truncated when I saved the Excel file in csv format: Excel didn't write
## out those values to their full number of digits, apparently. Good to know...