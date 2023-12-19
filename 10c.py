import os
import csv
import matplotlib.pyplot as plt

# Set the directory
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
csv_directory = data_path + "Weather_data/"

os.chdir(csv_directory)

# Initialize a list to store the wind speeds
wind_speeds = []

# Iterate over each csv file in the directory
for filename in os.listdir(csv_directory):
    if filename.endswith(".csv"):
        # Open the csv file
        with open(filename, "r") as file:
            # Create a csv reader object
            csv_reader = csv.reader(file)

            # Skip the 4 header rows
            for i in range(4):
                next(csv_reader)

            # Read the wind speeds from the csv file
            for row in csv_reader:
                wind_speed = row[2]
                if wind_speed != 'NaN':  # Skip rows with NaN values.
                    try:
                        wind_speed = int(float(wind_speed))
                        bin_number = wind_speed // 1
                        if bin_number > 5:
                            bin_number = 5
                        wind_speeds.append(bin_number)
                    except ValueError:  # Continues to the next row without adding the bin number if NaN
                        pass

# Count the occurrences of each bin
bin_counts = [wind_speeds.count(i) for i in range(6)]

# Create labels for the pie chart
labels = ['0', '1', '2', '3', '4', '5']

# Create the pie chart
plt.pie(bin_counts, labels=labels, autopct='%1.1f%%')
plt.title('Wind Speeds')
plt.show()
