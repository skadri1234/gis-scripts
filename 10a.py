import csv  # Makes easier to read csv files
import matplotlib.pyplot as plt
import os
dl = "C:/"
data_path = dl + "NRE_5585/Data/"
os.chdir(data_path)

# Initialize dictionaries to count records by study area and sex
study_area_counts = {}
sex_counts = {}

# Read the csv file and populate the dictionaries
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

# Define the order of study areas and sex
study_area_order = ["CO", "Patagonia", "WY"]
sex_order = ["F", "M"]

# Prepare the data for plotting
study_areas = []
female_counts = []
male_counts = []

for study_area in study_area_order:
    study_areas.append(study_area)
    female_counts.append(sex_counts["F"][study_area])
    male_counts.append(sex_counts["M"][study_area])

# Create bar plot
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.3
index = range(len(study_area_order))

plt.bar(index, female_counts, bar_width, label="Female", color="red")
plt.bar(index, male_counts, bar_width, label="Male", color="blue", bottom=female_counts)

plt.show()