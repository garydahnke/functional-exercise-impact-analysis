"""
Script: total_volume_for_one_exercise.py
Purpose: This program generates Daily Protein Intake report for a selected month based on data from
         data-log.ops spreadsheet - sheet 'Protein Consumption'.
Author: Gary Dahnke
Date: July 2026
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

month_name = "June"
month_number = datetime.strptime(month_name, "%B").month
output_type = "online" # file or online

print("month number:",month_number)

file = "fitness-log.ods"
protien_data = None
monthly_protein_data = None

# Retrieve all data from the 'Protein_Consumption' sheet and load into a dataframe.
sheet = "Protein_Consumption"
try:
    protein_data = pd.read_excel(file, sheet_name=sheet)
except FileNotFoundError:
    print("File does not exist.")

# Load all the data for the month select from the intial dataframe
year = str(protein_data["Date"].dt.year.unique()[0])
monthly_protein_data = protein_data[protein_data["Date"].dt.month == month_number] 

# Retrieve all the protein data that was below the threshold
low_protein_data = monthly_protein_data.loc[monthly_protein_data["Protein Grams"] < 90, ["Date","Protein Grams"]]
# print("Low Protein Data")
# print(low_protein_data)

# Retrieve all the protein data that exceeded the threshold
high_protein_data = monthly_protein_data.loc[monthly_protein_data["Protein Grams"] >= 90, ["Date","Protein Grams"]]
# print("High Protein Data")
# print(high_protein_data)

plt.figure(figsize=(12,6))
# Plot all Protein Intake data exlcuding plot points but draw line between points
# Note that 'marker=o' is excluded
plt.plot(monthly_protein_data["Date"], monthly_protein_data["Protein Grams"], label="Protein Intake")

# Plot all Low Protein Intake data
plt.scatter(low_protein_data["Date"], low_protein_data["Protein Grams"],
            c="red", label="Below 90g", marker="o")
# Plot all High Protein Intake data
plt.scatter(high_protein_data["Date"], high_protein_data["Protein Grams"],
            c="green", label="At/Above 90g", marker="o")

# Add threshold line
plt.axhline(90, color="gray", linestyle="--", label="90g Threshold")

for date, grams in zip(low_protein_data["Date"], low_protein_data["Protein Grams"]):
    plt.annotate(f"{grams}g",
                 xy=(date, grams),
                 xytext=(0,-15),  # offset text upward
                 textcoords="offset points",
                 ha="center",
                 color="red")

plt.title("Daily Protein Intake")
plt.xlabel("Date")
plt.ylabel("Protein (grams)")
plt.tight_layout()
plt.legend()
plt.xticks(rotation=30)

# Output chart to a file or online
if output_type == "file":
    # Save charts as *.svg and *.pdf files.    
    try:
        filename = f"protein-intake-for-{month_name.lower()-{year}}.svg"
        print(f"Creating {filename}")
        plt.savefig(filename)
        filename = f"protein-intake-for-{month_name.lower()}-{year}.pdf"
        print(f"Creating {filename}")
        plt.savefig(filename)
    except FileNotFoundError:
        print("Directory does not exist.")
    except PermissionError:
        print(f"No permission to write the {filename}.")
    except OSError as e:
        print(f"OS error occurred: {e}")
    finally:
        print(f"Files for {month_name} of {year} have been created.")
else:
    # Generate image for chart.  
    print(f"Generating chart for {month_name} of {year}...")
    plt.show()


