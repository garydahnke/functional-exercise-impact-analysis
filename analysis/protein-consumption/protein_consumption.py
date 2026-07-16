"""
Script: monthly_protein_consumption.py
Purpose: This program generates Daily Protein Intake chart for one or more user selected months or 
         for all months for the same calendar year from fitness-log.ods spreadsheet - sheet 'Protein 
         Consumption'.
         User Set Variables:
         1. spreadsheet - fitness log spreadsheet
         2. month_name_list - a list of months to generate charts 
         3. output_type - a flag to define the type of output for the chart 
            options: file or online        
Author: Gary Dahnke
Date: July 2026
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import datetime

"""
User Set Variables - Start
"""
spreadsheet = "fitness-log.ods"
month_name_list = []
# month_name_list = ["May","June","July"]
# month_name_list = ["May","June"]
output_type = "file" # file or online
"""
User Set Variables - End
"""
# Retrieve all data from the 'Protein_Consumption' sheet and load into a dataframe
sheet = "Protein_Consumption"
try:
    protein_data = pd.read_excel(spreadsheet, sheet_name=sheet)
except FileNotFoundError:
    print("File does not exist.")

# Build a list of months to pull data from the protein_data dataframe
year = str(protein_data["Date"].dt.year.unique()[0])
if len(month_name_list) == 0:
    month_number_list = [datetime.datetime.strptime(month_name, "%B").month  \
                        for month_name in month_name_list]
if len(month_number_list) == 0:
    month_number_list = protein_data["Date"].dt.month.unique()    

# Process each month of data to create the charts as files
for month_number in month_number_list:
    month_name = calendar.month_name[month_number]
# Load all the data for the month select from the intial dataframe
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
            filename = f"protein-consumption-for-{year}-{month_name.lower()}.svg"
            print(f"Creating {filename}")
            plt.savefig(filename)
            filename = f"protein-consumption-for-{year}-{month_name.lower()}.pdf"
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
