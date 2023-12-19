import os
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
temp_path = dl + "NRE_5585/Temp/"
res_path = dl + "NRE_5585/Results/"

# Change the working directory to the data_path weather path
os.chdir(data_path + "Weather_data/")

# Create a dictionary to insert wind speeds grouped by day
daily_wind_speeds = {}

# List of file names in the data directory
file_names = os.listdir()
print(file_names)

# Function to parse a date timestamp into a (month, day, year, hour, min, sec) tuple
def parse_day(date_str):
    date_parts = date_str.split('/')
    if len(date_parts) == 3:
        return int(date_parts[1])  # return the day as an integer
    return None


# Iterate through the files in the folder, skip all non csv files
for file_name in file_names:
    if not file_name.endswith(".csv"):
        continue

    with open(file_name, 'r') as f:
        lines = f.readlines()

        # Iterate through the data in the file, skip the first 4 header lines
        for line in lines[4:]:
            # Split the line by comma to get columns
            columns = line.strip().split(',')

            # Extract the timestamp and wind speed from the columns
            timestamp = columns[0]
            wind_speed_ms = columns[2]

            # Skip rows with missing or invalid wind speed values
            if wind_speed_ms == "NAN" or float(wind_speed_ms) > 20.0:
                continue

            # Parse the day from the timestamp
            day = parse_day(timestamp)

            # Store wind speed in the daily_wind_speeds dictionary
            if day not in daily_wind_speeds:
                daily_wind_speeds[day] = []
            daily_wind_speeds[day].append(float(wind_speed_ms))

# After processing the files, compute and print daily average wind speeds
for day, wind_speeds in daily_wind_speeds.items():
    day_avg_wind_speed = sum(wind_speeds) / len(wind_speeds)
    print(f"Day {day} avg ws was {day_avg_wind_speed:.3f} m/s")