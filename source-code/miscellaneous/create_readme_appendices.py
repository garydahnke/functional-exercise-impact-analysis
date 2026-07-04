import os
import pandas as pd
import shutil

file = "fitness-log.ods"
sheets_to_report = [["Exercises","readme-exercises.txt","readme-exercises.md"],
                    ["Data_Dictionary","readme-data-dictionary.txt","readme-data-dictionary.md"]]
         
for sheet in sheets_to_report:
    if os.path.exists(sheet[1]):
        os.remove(sheet[1])
    with open(sheet[1], "w", encoding="utf-8") as f:
        try:
            df = pd.read_excel(file, sheet_name=sheet[0])
        except FileNotFoundError:
            print("File does not exist.")
        print(df)
        if sheet[0] == "Exercises":
            df["Sets"] = df["Sets"].astype(str)
            df["Sets"] = df["Sets"].str.replace(r"\.0$", "", regex=True)
            df.fillna({"Exercise":" ","Sets":" ","Reps":" ","Workout Type":" ","Active":" "},inplace=True)
            df["Sets"] = df["Sets"].replace(["Nan","nan"], "")
        print(df)
        markdown = df.to_markdown(index=False)
        f.write(f"## {sheet}\n")
        f.write(markdown)
        df = None

for sheet in sheets_to_report:
    with open(sheet[1], "r", encoding="utf-8") as txt_file:
        content = txt_file.read()
    with open(sheet[2], "w", encoding="utf-8") as md_file:
        md_file.write(content)
        md_file.write("\n\n[Return to README](../README.md)\n")