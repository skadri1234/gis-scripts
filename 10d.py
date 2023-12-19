import os
import matplotlib.pyplot as plt

# Set the directory
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
csv_directory = data_path + "Weather_data/"

# Initialize a list to store the wind speeds
wind_speeds = []

# Loop through the csv files in the directory
for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        # Open the csv file
        with open(os.path.join(csv_directory, filename), 'r') as file:
            # Skip the header rows
            for i in range(4):
                next(file)
            # Read the wind speed column
            for row in file:
                # Split the line into columns
                columns = row.strip().split(',')
                # Get the wind speed value from the third column
                wind_speed = float(columns[2])
                # Ignore wind speeds greater than 10 m/s
                if wind_speed <= 10:
                    wind_speeds.append(wind_speed)

# Define the bin edges
bin_edges = range(0, 11)

# Create the histogram
plt.hist(wind_speeds, bins=bin_edges, edgecolor='black')
plt.title('Wind Speed (m/s)')
plt.show()