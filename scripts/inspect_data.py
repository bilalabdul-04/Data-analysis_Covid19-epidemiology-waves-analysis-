import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"

files = {
    "cases_deaths": "1.COVID-19_daily_number_of_new_cases_and_deaths.csv",
    "vaccination": "2.COVID-19_vaccination.csv",
    "hospital_icu": "3.COVID-19_hospital_and_ICU_admission_rates.csv"
}

for name, file in files.items():
    path = os.path.join(base_path, file)
    print(f"\n==================== {name} ====================")
    if os.path.exists(path):
        df = pd.read_csv(path, nrows=5)
        print(f"Shape of entire dataset (rough estimate): {os.path.getsize(path)} bytes")
        print("Columns:", list(df.columns))
        print("First 2 rows:")
        print(df.head(2))
    else:
        print(f"File not found: {path}")
