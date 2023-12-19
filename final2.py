import arcpy
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

# Set the workspace and shapefile path
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"
height_path = data_path + "Height_validation_data/"
arcpy.env.overwriteOutput = True
arcpy.env.workspace = height_path
shapefile_path = height_path + "Height_validation_data.shp"

# Read the shapefile into a Pandas DataFrame
fields = ['LiDAR_Ht', 'Field_Ht', 'Spp', 'SppType']
df = pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(shapefile_path, fields))

# Calculate residuals
df['Residuals'] = df['LiDAR_Ht'] - df['Field_Ht']

# Part 1: Test residuals for equal variance and normality
# Scatter plot of residuals
plt.scatter(range(len(df)), df['Residuals'])
plt.xlabel('Data Points')
plt.ylabel('Residuals')
plt.title('Residuals Scatter Plot')
plt.show()

# Bartlett test for each species with at least 24 members
species_counts = df['Spp'].value_counts()
for species in species_counts.index[species_counts >= 24]:
    species_residuals = df[df['Spp'] == species]['Residuals']
    stat, p_value = stats.bartlett(species_residuals, df['Residuals'])
    print(f'Bartlett test for {species}: p-value = {p_value:.3f}')

# Quantile-Quantile plot and normality tests
stats.probplot(df['Residuals'], dist='norm', plot=plt)
plt.title('Quantile-Quantile Plot')
plt.show()

shapiro_stat, shapiro_p_value = stats.shapiro(df['Residuals'])
ks_stat, ks_p_value = stats.kstest(df['Residuals'], 'norm')
ad_stat, ad_p_value, _ = stats.anderson(df['Residuals'], dist='norm')

print(f'Shapiro-Wilk test: p-value = {shapiro_p_value:.3f}')
print(f'Kolmogorov-Smirnov test: p-value = {ks_p_value:.3f}')
print(f'Anderson-Darling test: p-value = {ad_p_value[0]:.3f}')

# Part 2: Linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(df['LiDAR_Ht'], df['Field_Ht'])
regression_equation = f'y = {slope:.3f}x + {intercept:.3f}'

plt.scatter(df['LiDAR_Ht'], df['Field_Ht'], label='Data Points')
plt.plot(df['LiDAR_Ht'], slope * df['LiDAR_Ht'] + intercept, color='red', label='Regression Line')
plt.xlabel('LiDAR Height')
plt.ylabel('Field Height')
plt.title('Linear Regression')
plt.text(0.7, 0.1, f'R-squared = {r_value**2:.3f}\nP-value = {p_value:.3f}\n{regression_equation}',
         transform=plt.gca().transAxes)
plt.legend()
plt.show()

# Part 3: Boxplots by species and species type
plt.figure(figsize=(15, 10))

# Boxplots by species
plt.subplot(2, 1, 1)
species_to_test = species_counts.index[species_counts >= 30]
boxplot_data_species = [df[df['Spp'] == species]['Residuals'].tolist() for species in species_to_test]
plt.boxplot(boxplot_data_species, labels=species_to_test)
plt.title('Boxplots by Species')

if shapiro_p_value < 0.05:
    # Data not normal, use Wilcoxon rank sum test
    stat, p_value = stats.ranksums(df[df['Spp'].isin(species_to_test)]['Residuals'], df['Residuals'])
    test_type = 'Wilcoxon Rank Sum'
else:
    # Data normal, use ANOVA
    stat, p_value = stats.f_oneway(*boxplot_data_species)
    test_type = 'ANOVA'

print(f'{test_type} for Boxplots by Species: p-value = {p_value:.3f}')

# Boxplots by species type
plt.subplot(2, 1, 2)
boxplot_data_species_type = [df[df['SppType'] == species_type]['Residuals'].tolist() for species_type in df['SppType'].unique()]
plt.boxplot(boxplot_data_species_type, labels=df['SppType'].unique())
plt.title('Boxplots by Species Type')

if shapiro_p_value < 0.05:
    # Data not normal, use Wilcoxon rank sum test
    stat, p_value = stats.ranksums(df[df['SppType'].isin(['compound', 'simple', 'conifer'])]['Residuals'], df['Residuals'])
    test_type = 'Wilcoxon Rank Sum'
else:
    # Data normal, use ANOVA
    stat, p_value = stats.f_oneway(*boxplot_data_species_type)
    test_type = 'ANOVA'

print(f'{test_type} for Boxplots by Species Type: p-value = {p_value:.3f}')

plt.tight_layout()
plt.show()
# Part 4: Pairwise tests of residuals by species
species_list = species_counts.index[species_counts >= 2].tolist()
pairwise_tests = pd.DataFrame(index=species_list, columns=species_list)

for species1 in species_list:
    for species2 in species_list:
        if species1 != species2:
            data1 = df[df['Spp'] == species1]['Residuals']
            data2 = df[df['Spp'] == species2]['Residuals']

            if shapiro_p_value < 0.05:
                # Data not normal, use Wilcoxon rank sum test
                stat, p_value = stats.ranksums(data1, data2)
                test_type = 'Wilcoxon Rank Sum'
            else:
                # Data normal, use 2-sample t-test
                stat, p_value = stats.ttest_ind(data1, data2)
                test_type = '2-sample t-test'

            pairwise_tests.at[species1, species2] = p_value

# Print the pairwise tests table
print("Pairwise 2-sample tests by species (non-parametric)")
print(pairwise_tests)
# Save Pairwise 2-sample tests by species table to a CSV file
pairwise_tests.to_csv(res_path + 'pairwise_tests.csv')
print("Pairwise tests table saved to pairwise_tests.csv in the Results Directory")
