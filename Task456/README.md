# Hinger ASL Data Pipeline — Group B26

CMP-5058A Artificial Intelligence, Coursework 001  
Student IDs: 100457714, 100500854, 100464375, 100501057

## Setup

The processed folder contains prepared 256 × 256 JPG photographs, organised by student and letter (A–Z).
 Keep this folder beside the Python scripts and hand_landmarker.task.

Install the libraries once:
py -m pip install mediapipe pandas numpy

Run the four processing stages:
py run_pipeline.py


## What the code does

- `extract_features.py` extracts 21 hand landmarks (63 values) per photograph.
- `data_cleaning.py` removes failed detections, exact duplicates and flagged outliers.
- `data_analysis.py` prints the dataset summary and per-letter counts.
- `feature_engineering.py` normalises landmarks and adds five fingertip-distance features.
- `run_pipeline.py` runs the four scripts in order.

The output files:
`features_raw.csv`: before data cleaning
`features_clean.csv`: after data cleaning
`features_final.csv`: The final dataset contains 68 numeric input features per usable photograph after feature eng
