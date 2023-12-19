"""
Shafeeq Kadri
11ind
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('C:/NRE_5585/Data/uconn_woody_plants.csv')

# Calculate variables
sum_x = sum(df.Tree_Height)
sum_x_sq = sum(df.Tree_Height**2)
sum_y = sum(df.Crown_Radius)
sum_y_sq = sum(df.Crown_Radius**2)
sum_x_y = sum(df.Tree_Height * df.Crown_Radius)
n = len(df)

# Calculate coefficients
b = (sum_y * sum_x_sq - sum_x * sum_x_y) / (n * sum_x_sq - sum_x**2)
m = (n * sum_x_y - sum_x * sum_y) / (n * sum_x_sq - sum_x**2)
r = (n * sum_x_y - sum_x * sum_y) / ((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2))**0.5

# Print regression results
print(f"Slope (m): {m:.2f}")
print(f"Intercept (b): {b:.2f}")
print(f"Correlation coefficient (r): {r:.2f}")

# Make the plot
max_height = df.Tree_Height.max()
plt.scatter(df.Tree_Height, df.Crown_Radius, label='Data Points')
plt.plot([0, max_height], [b, b + m * max_height], color='red', label=f'Regression Line (m={m:.2f}, b={b:.2f}, r={r:.2f})')

plt.xlabel('Tree Height (m)')
plt.ylabel('Crown Radius (m)')
plt.title('Linear Regression: Crown Radius vs. Tree Height')
plt.legend()
plt.show()

# Filter Genera with >= 20 trees
genus_counts = df['Genus'].value_counts()
selected_genera = genus_counts[genus_counts >= 20].index

result_df = pd.DataFrame(columns=['Genus', 'Slope', 'Intercept', 'r'])

for genus in selected_genera:
    genus_data = df[df['Genus'] == genus]

    sum_x = sum(genus_data.Tree_Height)
    sum_x_sq = sum(genus_data.Tree_Height ** 2)
    sum_y = sum(genus_data.Crown_Radius)
    sum_y_sq = sum(genus_data.Crown_Radius ** 2)
    sum_x_y = sum(genus_data.Tree_Height * genus_data.Crown_Radius)
    n = len(genus_data)

    b = (sum_y * sum_x_sq - sum_x * sum_x_y) / (n * sum_x_sq - sum_x ** 2)
    m = (n * sum_x_y - sum_x * sum_y) / (n * sum_x_sq - sum_x ** 2)
    r = (n * sum_x_y - sum_x * sum_y) / ((n * sum_x_sq - sum_x ** 2) * (n * sum_y_sq - sum_y ** 2)) ** 0.5

    result_df = result_df.append({
        'Genus': genus,
        'Slope': m,
        'Intercept': b,
        'r': r
    }, ignore_index=True)

# Print the result table
print(result_df)