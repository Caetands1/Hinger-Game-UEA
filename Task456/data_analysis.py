
"""
Hinger Project
Coursework 001 for: CMP-5058A Artificial Intelligence

Task 6 - Exploratory data analysis (EDA)

@author: B26 (100457714, 100500854, 100464375, 100501057)
@date:   25/11/2026

Input: features_raw.csv and features_clean.csv
The analysis prints dataset statistics in the terminal
"""

# pandas reads and analyses CSV data
import pandas as pd

# ceil rounds the class average up to a whole photograph for display only
from math import ceil

# path helps find files wherever the project folder is copied
from pathlib import Path


folder = Path(__file__).parent

# read the raw and clean datasets
raw = pd.read_csv(folder / "features_raw.csv")
clean = pd.read_csv(folder / "features_clean.csv")

# we need at least one usable photograph to analyse class counts
if clean.empty:
    raise SystemExit("ERROR: There are no clean records to analyse.")

# count the number of usable photographs for each letter A-Z. Include letters with zero photographs so we can check all 26 letters
counts = clean["label"].value_counts().reindex(
    list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), fill_value=0
)
nonzero = counts[counts > 0]

# present the dataset summary
print("Dataset analysis:")
print(f"  ASL letters represented: {len(nonzero)}/26")

# show one simple rounded average
print(f"  Average images per letter: {ceil(len(clean) / 26)}")

# count the original detections so we can compare raw and cleaned records
detected = raw["detected"].astype(str).str.lower() == "true"

# show how many photographs from each group member survived cleaning
print("  Clean images by student:")
for student, amount in clean["student"].value_counts().sort_index().items():
    print(f"    {student}: {amount}")

# display the number of usable images for every letter A-Z.
print("  Usable images for each letter:")
for letter, amount in counts.items():
    print(f"    {letter}: {amount}")

# show how many images MediaPipe could and could not recognise
print(f"  Raw MediaPipe detections: {int(detected.sum())}")
print(f"  Raw MediaPipe failures: {int((~detected).sum())}")

# the coordinate ranges are the smallest and largest original MediaPipe
# x, y and z values among usable hands, before normalisation
print("  Original landmark coordinate ranges:")
for axis in ["x", "y", "z"]:
    columns = [f"{axis}{i}" for i in range(21)]
    values = clean[columns].to_numpy(dtype=float)
    minimum = values.min()
    maximum = values.max()
    print(f"    {axis}: [{minimum:.3f}, {maximum:.3f}]")
