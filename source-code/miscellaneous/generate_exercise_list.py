import os   
import pandas as pd
import matplotlib.pyplot as plt
import analytics
import numpy as np

sheet = "Exercises"
try:
    exercise_data = pd.read_excel(analytics.spreadsheet, sheet_name=sheet, \
                                  usecols=["Exercise", "Sets", "Reps", "Workout Type", "Active"])

except FileNotFoundError:
    print("File does not exist.")

exercise_data.loc[:, "Sets"] = exercise_data["Sets"].fillna(0)
exercise_data.loc[:, "Reps"] = exercise_data["Reps"].fillna("")
exercise_data.loc[:, "Workout Type"] = exercise_data["Workout Type"].fillna("")
exercise_data.loc[:, "Active"] = exercise_data["Active"].fillna("")

print("Exercise List")
print("-------------")
exercise_list = exercise_data["Exercise"].to_list()
for e in exercise_list:
    print(f'"{e}",')
print("")
print("Exercise Elements List")
print("----------------------")
exercise_elements_list = [tuple(row) for row in exercise_data.itertuples(index=False, name=None)]
for e in exercise_elements_list:
    print(e,",")