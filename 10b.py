import csv  # Makes easier to read csv files
import matplotlib.pyplot as plt
import os
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
os.chdir(data_path)

# Initialize dictionaries to count study area and sex
study_area_counts = {}
sex_counts = {}

# Read the csv file and fill the dictionaries
with open("PumaPositions.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)  # Iterates over each csv row while accounting for the header row
    for row in csv_reader:
        study_area = row["StudyArea"]
        sex = row["Sex"]

        if study_area not in study_area_counts:
            study_area_counts[study_area] = {"F": 0, "M": 0}
        if sex not in sex_counts:
            sex_counts[sex] = {"CO": 0, "Patagonia": 0, "WY": 0}

        study_area_counts[study_area][sex] += 1
        sex_counts[sex][study_area] += 1

# Define the order of study areas and sex and color
study_area_order = ["CO", "Patagonia", "WY"]
sex_order = ["F", "M"]
colors = {'CO': 'blue', 'Patagonia': 'orange', 'WY': 'green'}

# Prepare the data for plotting
female_counts = [sex_counts["F"][area] for area in study_area_order]
male_counts = [sex_counts["M"][area] for area in study_area_order]

bar_width = 0.30
index = range(len(study_area_order))
male_bar = [i - bar_width / 2 for i in index]
female_bar = [i + bar_width / 2 for i in index]

# Create bar plot
fig, ax = plt.subplots()
# Obtain both the index i and the corresponding area in the study_area_order and iterate counts to create bars
for i, area in enumerate(study_area_order):
    plt.bar(male_bar[i], male_counts[i], bar_width, label="Male", color=colors[area], edgecolor="black")
    plt.bar(female_bar[i], female_counts[i], bar_width, label="Female", color=colors[area], edgecolor="black")


# Label and show the plot
plt.xlabel("Study Area")
plt.ylabel("Count of Records per Sex")
plt.title("Puma Record Comparison")
plt.xticks(index, study_area_order)
plt.legend()
plt.show()
