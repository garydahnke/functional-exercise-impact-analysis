"""
Script: flexibility-vs-soreness-heatmap.py
Purpose: This program generates side-by-side bar chart (Flexibility vs Soreness — Single-Joint 
         Snapshot) to compare the flexibility to soreness of a selected joint for seven days. All 
         data is extracted from the fitness-log.ods spreadsheet - sheet 'Daily_Health_Log'. Data 
         in the spreadsheet is for one calendar year. 
         User Set Variables:
         1. spreadsheet - fitness log spreadsheet
         2. month_name - name of month to generate charts; this value will override start_date
                         if this value is set
         3. start_date - starting date of the data to be extracted; leave mont_name empty
                         to use the start_date
         4. number_of_days - number of days from start_date use to define an end date;
                             max value is 31
         5. output_type - a flag to define the type of output for the chart 
            options: file or online          
Author: Gary Dahnke
Date: July 2026
"""
import os   
import pandas as pd
import matplotlib.pyplot as plt
import analytics
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import calendar

"""
User Set Variables - Start
"""
spreadsheet = "fitness-log.ods"
month_name = "July"
start_date = "2026-07-01" # YYYY-MM-DD format
number_of_days = 30 # max value of 31
output_type = "file" # file or online
"""
User Set Variables - End
"""
# Calculate values from User Set Variables
start_date_dt = datetime(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:]))
if len(month_name.strip()) == 0:
    if number_of_days <= 45:
        end_date = start_date_dt + timedelta(days=number_of_days)
    else:
        end_date = start_date_dt + timedelta(days=31)
else:
    month_number = datetime.strptime(month_name.strip(), "%B").month

# Retrieve all data from the 'Daily_Health_Log' sheet and load into a dataframe
sheet = "Daily_Health_Log"
try:
    daily_log_data = pd.read_excel(spreadsheet, sheet_name=sheet)
except FileNotFoundError:
    print("File does not exist.")

# Create a list of columns with flexibility and soreness values to be extracted from
# the dataframe daily_log_data
joints = ["Shoulder", "Elbow", "Wrist", "Hip", "Knee", "Ankle"]
joint_columns = [f"{joint} Flexibility" for joint in joints] + \
                [f"{joint} Soreness" for joint in joints]
for column in joint_columns:
    daily_log_data.loc[:, column] = daily_log_data[column].replace("N/A", 0)
    daily_log_data.loc[:, column] = daily_log_data[column].fillna(0)

# Keep the rows in the dataframe daily_log_data that are defined by the 'User Set Variables'
# for dates 
if (len(month_name.strip()) > 0):
    month_number = datetime.strptime(month_name, "%B").month
    daily_log_data = daily_log_data[daily_log_data["Date"].dt.month == month_number]
else:
    daily_log_data = daily_log_data[(daily_log_data["Date"] >= start_date) & (daily_log_data["Date"] <= end_date)]

# Reconstruct the dataframe so the columns in the dataframe (Flexibility and Soreness ratings)
# are now row values and the Date column value are now the first row in the data frame     
rows = []
for _, row in daily_log_data.iterrows():
    date = row["Date"]
    axis_date = row["Date"].strftime("%b-%d")
    for joint in joints:
        flexibility_column = f"{joint} Flexibility"
        soreness_column = f"{joint} Soreness"
        rows.append({
            "Date": date,
            "Axis Date": axis_date,
            "Joint": joint,
            "Flexibility": row[flexibility_column],
            "Soreness": row[soreness_column]
        })
chart_data = pd.DataFrame(rows)

# Calulate minimum date and maximum date in the dataframe to be used in title and file names
min_date = chart_data["Date"].min()
max_date = chart_data["Date"].max()
title_date_range = f"{min_date.strftime("%B %d, %Y")} - {max_date.strftime("%B %d, %Y")}"
file_date_range = f"{min_date.strftime("%Y-%B-%d")}-{max_date.strftime("%Y-%B-%d")}"

# Create heatmap chart for Joint Soreness
# Pivot for soreness
soreness_matrix = chart_data.pivot(index="Joint", columns="Axis Date", values="Soreness")

title = f"Joint Soreness for {title_date_range}\n" + \
        f"Scale: 1 = No Soreness, 10 = Severe Soreness**"

plt.figure(figsize=(14, 8))
sns.heatmap(soreness_matrix, annot=True, cmap="Reds")
plt.xticks(rotation=45) 
plt.title(title)

# Output chart to a file or online
if output_type == "file":
   # Save charts as *.svg and *.pdf files.    
    try:
        print("-" * 60)
        filename = f"{analytics.health_analysis_charts}soreness-heatmap-for-{file_date_range}.svg"
        print(f"Creating {filename}")
        plt.savefig(filename)
        filename = f"{analytics.health_analysis_charts}soreness-heatmap-for-{file_date_range}.pdf"
        print(f"Creating {filename}")
        plt.savefig(filename)
    except FileNotFoundError:
        print("Directory does not exist.")
    except PermissionError:
        print(f"No permission to write the {filename}.")
    except OSError as e:
        print(f"OS error occurred: {e}")
    finally:
        print(f"Files for {file_date_range} have been created.")
else:
    # Generate image for chart. 
    print("-" * 60) 
    print(f"Generating chart for {title_date_range}...")
    plt.show()

# Create heatmap chart for Joint Flexibility
# Pivot for flexibility
flexibility_matrix = chart_data.pivot(index="Joint", columns="Axis Date", values="Flexibility")

title = f"Joint Flexibility for {title_date_range}\n" + \
        f"Scale: 1 = Limited Mobility, 10 = High Mobility**"

plt.figure(figsize=(14, 8))
sns.heatmap(flexibility_matrix, annot=True, cmap="Greens")
plt.xticks(rotation=45) 
plt.title(title)

# Output chart to a file or online
if output_type == "file":
   # Save charts as *.svg and *.pdf files.    
    try:
        print("-" * 60)
        filename = f"{analytics.health_analysis_charts}flexbility-heatmap-for-{file_date_range}.svg"
        print(f"Creating {filename}")
        plt.savefig(filename)
        filename = f"{analytics.health_analysis_charts}flexbility-heatmap-for-{file_date_range}.pdf"
        print(f"Creating {filename}")
        plt.savefig(filename)
    except FileNotFoundError:
        print("Directory does not exist.")
    except PermissionError:
        print(f"No permission to write the {filename}.")
    except OSError as e:
        print(f"OS error occurred: {e}")
    finally:
        print(f"Files for {file_date_range} have been created.")
else:
    # Generate image for chart.
    print("-" * 60)  
    print(f"Generating chart for {title_date_range}...")
    plt.show()