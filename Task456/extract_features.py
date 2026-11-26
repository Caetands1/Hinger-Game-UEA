
"""
Hinger Project
Coursework 001 for: CMP-5058A Artificial Intelligence

Task 5 - Extract 21 hand landmarks using MediaPipe

@author: B26 (100457714, 100500854, 100464375, 100501057)
@date:   25/11/2026

Input: prepared 256 x 256 JPG photographs in processed/.
Output: features_raw.csv, containing the detected hand landmarks.
"""

# csv saves the hand landmarks in a table
import csv

# path finds the photographs and MediaPipe model
from pathlib import Path

# reduce optional startup messages from the hand landmark model
import os
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("GLOG_minloglevel", "2")
import mediapipe as mp


folder = Path(__file__).parent
processed_folder = folder / "processed"
model_file = folder / "hand_landmarker.task"
output_file = folder / "features_raw.csv"
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

if not processed_folder.is_dir():
    raise SystemExit("ERROR: processed/ is missing. Extract the prepared photographs beside these scripts.")

if not model_file.is_file():
    raise SystemExit("ERROR: hand_landmarker.task is missing from this folder.")

# these columns identify each photograph and whether a hand was detected
column_names = ["student", "filename", "label", "detected"]

# each of the 21 hand points has x, y and z coordinates (63 in total)
for number in range(21):
    column_names.extend([f"x{number}", f"y{number}", f"z{number}"])

total = 0
successes = 0
failures = 0

# load the model once to analyse all the photographs
with mp.tasks.vision.HandLandmarker.create_from_model_path(str(model_file)) as detector:
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(column_names)

        # check each student's A-Z photograph folders
        for student in sorted(processed_folder.iterdir()):
            if not student.is_dir():
                continue

            for letter_folder in sorted(student.iterdir()):
                if not letter_folder.is_dir() or letter_folder.name not in letters:
                    continue

                for photo in sorted(letter_folder.iterdir()):
                    if not photo.is_file() or photo.suffix.lower() != ".jpg":
                        continue

                    total += 1
                    detected = False

                    # save 63 zeros if MediaPipe cannot detect the hand
                    coordinates = [0.0] * 63

                    try:
                        # open the photograph with MediaPipe
                        image = mp.Image.create_from_file(str(photo))

                        # find the hand landmarks
                        result = detector.detect(image)

                        if result.hand_landmarks:
                            # take the first detected hand
                            hand = result.hand_landmarks[0]

                            # collect x, y and z values from each hand point
                            coordinates = []
                            for point in hand:
                                coordinates.extend([point.x, point.y, point.z])

                            detected = True
                            successes += 1
                        else:
                            failures += 1

                    except (OSError, RuntimeError, ValueError) as error:
                        # count unreadable images as failed detections
                        print("ERROR:", photo.name, error)
                        failures += 1

                    # save one row for each photograph
                    writer.writerow([
                        student.name,
                        photo.name,
                        letter_folder.name,
                        detected,
                    ] + coordinates)


# show the total number of successful and failed detections
if total == 0:
    raise SystemExit("ERROR: No JPG photographs were found inside processed/.")

print("MediaPipe extraction:")
print(f"  Photographs checked: {total}")
print("  Landmarks per detected hand: 21 (63 x/y/z values)")
print(f"  Successful detections: {successes} ({successes / total:.1%})")
print(f"  Failed detections: {failures} ({failures / total:.1%})")
print("  Output: features_raw.csv")
