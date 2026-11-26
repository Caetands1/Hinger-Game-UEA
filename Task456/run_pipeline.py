
"""
Hinger Project
Coursework 001 for: CMP-5058A Artificial Intelligence

Run hand-landmark extraction, cleaning, analysis and feature engineering.
The starting input is prepared photographs inside processed/.

@author: B26 (100457714, 100500854, 100464375, 100501057)
@date:   25/11/2026
"""

# subprocess runs the Python scripts in order
import subprocess

# sys uses the same Python installation for each script
import sys

# path finds the scripts and photographs in the project folder
from pathlib import Path


folder = Path(__file__).parent

# these are the four scripts used for tasks 5 and 6
scripts = [
    "extract_features.py",    # Task 5: extract 63 hand landmark coordinates
    "data_cleaning.py",       # Task 6: remove invalid and repeated records
    "data_analysis.py",       # Task 6: describe the remaining dataset
    "feature_engineering.py"  # Task 6: create 68 numeric classifier inputs
]

# run each script 
for number, filename in enumerate(scripts, start=1):
    print(f"\n[{number}/{len(scripts)}] {filename}", flush=True)
    result = subprocess.run([sys.executable, str(folder / filename)],cwd=folder)
    if result.returncode != 0:
        raise SystemExit("ERROR: " + filename + " failed.")

# check that all three CSV files were created
datasets = ["features_raw.csv", "features_clean.csv", "features_final.csv"]

print("\nPipeline complete:")
print("  Processing stages finished: 4/4")
print("  Generated CSV datasets: 3")
for filename in datasets:
    print("    " + filename)
