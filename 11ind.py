import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('C:/NRE_5585/Data/uconn_woody_plants.csv')

# Calculate sums
sum_x = df['Tree_Height'].sum()
sum_x_sq = (df['Tree_Height'] ** 2).sum()
sum_y = df['Crown_Radius'].sum()
sum_y_sq = (df['Crown_Radius'] ** 2).sum()
sum_xy = (df['Tree_Height'] * df['Crown_Radius']).sum()
n = len(df)

# Calculate coefficients
m = (n * sum_xy - sum_x * sum_y) / (n * sum_x_sq - sum_x ** 2)
b = (sum_y - m * sum_x) / n
r = (n * sum_xy - sum_x * sum_y) / ((n * sum_x_sq - sum_x ** 2) * (n * sum_y_sq - sum_y ** 2)) ** .5

# Plot data and regression line
plt.scatter(df['Tree_Height'], df['Crown_Radius'])
max_height = df['Tree_Height'].max()
plt.plot([0, max_height], [b, b + m * max_height], c='r')

# Add labels
plt.title('Crown Width Given Tree Height')
plt.xlabel('Tree Height (m)')
plt.ylabel('Crown Radius (m)')

plt.show()




# Function to calculate stats
def get_stats(group):
    # Calculate sums
    n = len(group)
    sum_x = group['Tree_Height'].sum()
    sum_x_sq = (group['Tree_Height'] ** 2).sum()
    sum_y = group['Crown_Radius'].sum()
    sum_y_sq = (group['Crown_Radius'] ** 2).sum()
    sum_xy = (group['Tree_Height'] * group['Crown_Radius']).sum()

    # Calculate coefficients
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x_sq - sum_x ** 2)
    b = (sum_y - m * sum_x) / n
    r = (n * sum_xy - sum_x * sum_y) / ((n * sum_x_sq - sum_x ** 2) * (n * sum_y_sq - sum_y ** 2)) ** .5

    return pd.Series([m, b, r], index=['m', 'b', 'r'])


results = df.groupby('Genus').apply(get_stats).reset_index()
# Print results
print(results[results['Genus'] >= 20])