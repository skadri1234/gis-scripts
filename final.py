import arcpy
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Set up arcpy workspace and access the shapefile
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
arcpy.env.workspace = data_path + "Height_validation_data/"
shp_file = "Height_validation_data.shp"

# Extract data from the shapefile
fields = ['LiDAR_Ht', 'Field_Ht', 'Spp', 'SppType']
data = [list(row) for row in arcpy.da.SearchCursor(shp_file, fields)]

# 1) Tests of equal variance and normality
residuals = [row[0] - row[1] for row in data]
n = len(residuals)

plt.figure(figsize=(12, 8))

# Scatter plot of residuals
plt.subplot(221)
plt.scatter(range(n), residuals)
plt.title("Residuals Scatter Plot")

# Barlette test
species_counts = {}
for row in data:
    species = row[2]
    if species in species_counts:
        species_counts[species] += 1
    else:
        species_counts[species] = 1

for species, count in species_counts.items():
    if count >= 24:
        species_residuals = [row[0] - row[1] for row in data if row[2] == species]
        _, p_value = stats.bartlett(species_residuals, residuals)
        if p_value < 0.05:
            plt.text(n + 10, np.mean(species_residuals), f"{species}: Unequal Var")
        else:
            plt.text(n + 10, np.mean(species_residuals), f"{species}: Equal Var")

# Q-Q plot
plt.subplot(222)
stats.probplot(residuals, plot=plt)
plt.title("Quantile-Quantile Plot")

# Normality tests
plt.subplot(223)
shapiro_p = stats.shapiro(residuals)[1]
kstest_p = stats.kstest(residuals, 'norm')[1]
adtest_result = stats.anderson(residuals, dist='norm')

if shapiro_p < 0.05:
    plt.text(-2, 2, f"Shapiro-Wilk: Not Normal (p={shapiro_p:.3f})")
else:
    plt.text(-2, 2, f"Shapiro-Wilk: Normal (p={shapiro_p:.3f})")

if kstest_p < 0.05:
    plt.text(-2, 1, f"Kolmogorov-Smirnov: Not Normal (p={kstest_p:.3f})")
else:
    plt.text(-2, 1, f"Kolmogorov-Smirnov: Normal (p={kstest_p:.3f})")

critical_values = adtest_result[1]
if adtest_result[0] > critical_values[2]:  # Check the test statistic against the critical values
    plt.text(-2, 0, f"Anderson-Darling: Not Normal")
else:
    plt.text(-2, 0, f"Anderson-Darling: Normal")

# 2) Linear regression model
plt.subplot(224)
LiDAR_Ht = [row[0] for row in data]
Field_Ht = [row[1] for row in data]
slope, intercept, r_value, p_value, std_err = stats.linregress(LiDAR_Ht, Field_Ht)
plt.scatter(LiDAR_Ht, Field_Ht, label="Data Points")
plt.plot(LiDAR_Ht, intercept + slope * np.array(LiDAR_Ht), 'r', label="Regression Line")
plt.legend()
plt.title("Linear Regression")
plt.xlabel("LiDAR_Ht")
plt.ylabel("Field_Ht")
plt.text(min(LiDAR_Ht), max(Field_Ht), f"R-squared: {r_value ** 2:.3f}\nP-value: {p_value:.3f}")
plt.show()

# 3) Boxplots
species_counts = {}
species_type_counts = {'compound': 0, 'simple': 0, 'conifer': 0}
species_residuals = {}
species_type_residuals = {'compound': [], 'simple': [], 'conifer': []}

for row in data:
    species = row[2]
    species_type = row[3]
    if species in species_counts:
        species_counts[species] += 1
        species_residuals[species].append(row[0] - row[1])
    else:
        species_counts[species] = 1
        species_residuals[species] = [row[0] - row[1]]

    species_type_counts[species_type] += 1
    species_type_residuals[species_type].append(row[0] - row[1])

# Boxplots by species
plt.figure(figsize=(12, 6))
plt.subplot(121)
species_with_enough_data = [species for species, count in species_counts.items() if count > 30]
boxplot_data = [species_residuals[species] for species in species_with_enough_data]

if shapiro_p < 0.05:
    test_stat, p_value = stats.levene(*boxplot_data)
    test_used = 'Levene'
else:
    test_stat, p_value = stats.f_oneway(*boxplot_data)
    test_used = 'ANOVA'

plt.boxplot(boxplot_data, labels=species_with_enough_data)
plt.title("Boxplots by Species")
plt.text(1.2, max(max(boxplot_data), 0.5), f"{test_used}: p={p_value:.3f}")

# Boxplots by species type
plt.subplot(122)
boxplot_data = [species_type_residuals['compound'], species_type_residuals['simple'], species_type_residuals['conifer']]

if shapiro_p < 0.05:
    test_stat, p_value = stats.levene(*boxplot_data)
    test_used = 'Levene'
else:
    test_stat, p_value = stats.f_oneway(*boxplot_data)
    test_used = 'ANOVA'

plt.boxplot(boxplot_data, labels=species_type_residuals.keys())
plt.title("Boxplots by Species Type")
plt.text(1.2, max(max(boxplot_data), 0.5), f"{test_used}: p={p_value:.3f}")
plt.show()

# 4) Test for differences among residuals of each species
residual_table = []
for i in range(len(species_with_enough_data)):
    for j in range(i + 1, len(species_with_enough_data)):
        species1 = species_with_enough_data[i]
        species2 = species_with_enough_data[j]
        if shapiro_p < 0.05:
            test_stat, p_value = stats.ranksums(species_residuals[species1], species_residuals[species2])
            test_used = 'Wilcoxon Rank Sum'
        else:
            test_stat, p_value = stats.ttest_ind(species_residuals[species1], species_residuals[species2])
            test_used = '2 Sample T-Test'
        residual_table.append([species1, species2, p_value])

# Print the table
print("Pairwise Tests of Residuals")
print(f"{'Species 1':<20}{'Species 2':<20}{'P-value'}")
for row in residual_table:
    print(f"{row[0]:<20}{row[1]:<20}{row[2]:.3f}")