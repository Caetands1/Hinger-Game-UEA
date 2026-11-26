
"""
Hinger Project
Coursework 001 for: CMP-5058A Artificial Intelligence

Task 6 - Data cleaning, duplicates and outlier checking

@author: B26 (100457714, 100500854, 100464375, 100501057)
@date:   25/11/2026

Input: features_raw.csv.
Output: features_clean.csv with invalid and repeated rows removed.
"""

# pandas helps us read CSV data and remove invalid or repeated rows
import pandas as pd

# numpy provides simple maths for measuring hand distances
import numpy as np

# path finds photographs and CSV files
from pathlib import Path



# find the current project folder and load the MediaPipe results
folder = Path(__file__).parent
raw_file = folder / "features_raw.csv"
if not raw_file.is_file():
    raise SystemExit("ERROR: features_raw.csv missing. Run extract_features.py first.")

data = pd.read_csv(raw_file)
raw_count = len(data)
# keep a small summary of how many rows each cleaning rule removes
removed = {}

# build the list of the 63 coordinate columns
features = []
for number in range(21):
    features.extend([f"x{number}", f"y{number}", f"z{number}"])

# identifying columns to find each photo
required = ["student", "filename", "label", "detected"] + features
missing_columns = [column for column in required if column not in data.columns]
if missing_columns:
    raise SystemExit("ERROR: Missing CSV columns: " + str(missing_columns))

# failed hand detection:
# these records must remain in the RAW CSV as 63 zeros but they cannot be used to train the classifier
detected = data["detected"].astype(str).str.lower() == "true"
removed["failed detections"] = int((~detected).sum())
data = data.loc[detected].copy()

# missing values:
# a hand needs all 63 coordinates
missing_values = data[features].isna().any(axis=1)
removed["missing values"] = int(missing_values.sum())
data = data.dropna(subset=features).copy()

# duplicate records:
# pandas checks whether two records have the same ASL letter and all 63 hand coordinates
# keep the first record and remove the repeated one
duplicate_columns = ["label"] + features
before_duplicates = data.copy()
data = data.drop_duplicates(subset=duplicate_columns).copy()
removed["duplicate records"] = len(before_duplicates) - len(data)

# record the filenames that were dropped, so we can show them in the terminal
duplicate_photo_details = []
for index, row in before_duplicates.iterrows():
    if index not in data.index:
        duplicate_photo_details.append(str(row["filename"]))

# save the names of any unusual records found later
outlier_details = []

# stop if no valid hand observations are left
if data.empty:
    raise SystemExit("ERROR: No usable records remain after data cleaning.")

# hand size check:
# check the distance between the wrist and the base of the middle finger
# the distance cannot be zero because we use it to normalise hand size
hand_size = np.sqrt(
    (data["x9"] - data["x0"]) ** 2 +
    (data["y9"] - data["y0"]) ** 2
)
valid_size = hand_size > 1e-6
removed["invalid hand size"] = int((~valid_size).sum())
data = data.loc[valid_size].copy()
hand_size = hand_size.loc[valid_size]

if data.empty:
    raise SystemExit("ERROR: No records have a valid hand-size measurement.")

# outlier check:
# compare the distances from the wrist to each fingertip dividing by hand size helps us compare hands at different distances
fingertips = {"thumb": 4, "index": 8, "middle": 12, "ring": 16, "pinky": 20}
measurements = pd.DataFrame(index=data.index)

for finger, landmark in fingertips.items():
    distance = np.sqrt(
        (data[f"x{landmark}"] - data["x0"]) ** 2 +
        (data[f"y{landmark}"] - data["y0"]) ** 2
    )
    measurements[finger] = distance / hand_size

# check each letter separately because different letters have different hand shapes 
outliers = pd.Series(False, index=data.index)

for letter in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    group = data[data["label"] == letter]

    # we need a few examples to calculate a useful average
    if len(group) < 3:
        continue

    for finger in fingertips:
        values = measurements.loc[group.index, finger]
        average = values.mean()
        deviation = values.std()

        # if the distances are all the same, there is no unusual range to check
        if pd.isna(deviation) or deviation < 1e-9:
            continue

        # mark distances more than three standard deviations from the average
        lower = average - 3 * deviation
        upper = average + 3 * deviation
        unusual = values[(values < lower) | (values > upper)].index

        for index in unusual:
            if not outliers.loc[index]:
                outlier_details.append((letter, str(data.at[index, "filename"])))
            outliers.loc[index] = True

# remove unusual records from the clean dataset but keep the original photos
removed["possible outliers"] = int(outliers.sum())
data = data.loc[~outliers].reset_index(drop=True)

# save the cleaned data in one CSV file
data.to_csv(folder / "features_clean.csv", index=False)
# show how many records were removed at each main stage
other_removed = removed["missing values"] + removed["invalid hand size"]
duplicates = removed["duplicate records"]
print("Data cleaning:")
print(f"  Records received: {raw_count}")
print(f"  Failed hand detections: {removed['failed detections']}")
print(f"  Duplicate records removed: {duplicates}")
print(f"  Invalid/missing records removed: {other_removed}")
print(f"  Possible outliers excluded: {removed['possible outliers']}")
print(f"  Clean records remaining: {len(data)} ({len(data) / raw_count:.1%})")
print("  Output: features_clean.csv")

# show the names of repeated and unusual records
if duplicate_photo_details:
    print("  Duplicate landmark records:")
    for name in duplicate_photo_details:
        print("    " + str(name))
if outlier_details:
    print(f"  Possible outlier photographs ({len(outlier_details)}):")
    for letter, name in sorted(outlier_details):
        print(f"    {letter}: {name}")
