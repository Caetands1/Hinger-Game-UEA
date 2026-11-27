#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-5058A Artificial Intelligence

Task 6 - Normalise landmarks and create new numerical features

@author: B26 (100457714, 100500854, 100464375, 100501057)
@date:   25/11/2026

Input: features_clean.csv.
Output: features_final.csv, containing normalised landmarks, new features
and numeric class labels for A-Z.
"""

# pandas reads and saves the CSV data
import pandas as pd

# numpy is used for distance calculations
import numpy as np

# path finds the CSV file in the project folder
from pathlib import Path


folder = Path(__file__).parent

# read the cleaned hand landmark data
data = pd.read_csv(folder / "features_clean.csv")
if data.empty:
    raise SystemExit("ERROR: No clean photographs are available.")

# build a list of the 63 coordinates from the 21 hand landmarks
features = []
for number in range(21):
    features.extend([f"x{number}", f"y{number}", f"z{number}"])

# position normalisation:
# subtract the wrist position from every point so the wrist becomes zero
wrist_x = data["x0"].copy()
wrist_y = data["y0"].copy()
wrist_z = data["z0"].copy()

for number in range(21):
    data[f"x{number}"] = data[f"x{number}"] - wrist_x
    data[f"y{number}"] = data[f"y{number}"] - wrist_y
    data[f"z{number}"] = data[f"z{number}"] - wrist_z

# size normalisation:
# measure the distance from the wrist to the base of the middle finger
# this helps reduce differences caused by hands being closer to the camera
hand_size = np.sqrt(data["x9"] ** 2 + data["y9"] ** 2)

# do not divide by zero or an invalid hand measurement
valid = hand_size > 1e-6
if not valid.all():
    print("WARNING: Extra invalid hand sizes removed:", int((~valid).sum()))
    data = data.loc[valid].copy()
    hand_size = hand_size.loc[valid]

if data.empty:
    raise SystemExit("ERROR: No valid hand sizes remain.")

# divide all 63 coordinates by the same hand size for each photograph
for number in range(21):
    data[f"x{number}"] = data[f"x{number}"] / hand_size
    data[f"y{number}"] = data[f"y{number}"] / hand_size
    data[f"z{number}"] = data[f"z{number}"] / hand_size

# feature engineering:
# add five distances from the wrist to each fingertip
# the wrist is now (0, 0), so we use the fingertip x and y values
fingertips = {"thumb": 4, "index": 8, "middle": 12, "ring": 16, "pinky": 20}
extra_features = []

for finger, point_number in fingertips.items():
    column = "distance_" + finger
    data[column] = np.sqrt(
        data[f"x{point_number}"] ** 2 + data[f"y{point_number}"] ** 2
    )
    extra_features.append(column)

# label encoding:
# give every letter a number from 0 to 25 so the classifier can learn it
label_numbers = {}
for number, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    label_numbers[letter] = number

data["label_id"] = data["label"].map(label_numbers)

# keep the photograph information, correct answer and 68 numeric inputs
output_columns = ["student", "filename", "label", "label_id"] + features + extra_features
final_data = data[output_columns]

# save the final data for classifier training
final_data.to_csv(folder / "features_final.csv", index=False)

# show a short summary of the final dataset
print("Feature engineering:")
print(f"  Usable photographs: {len(final_data)}")
print("  Hand landmarks normalised for position and size")
print("  Features: 63 coordinates + 5 finger distances = 68")
print("  Output: features_final.csv")
