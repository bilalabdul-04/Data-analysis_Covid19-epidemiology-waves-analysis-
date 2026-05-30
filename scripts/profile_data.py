import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"

# File paths
cases_path = os.path.join(base_path, "1.COVID-19_daily_number_of_new_cases_and_deaths.csv")
vacc_path = os.path.join(base_path, "2.COVID-19_vaccination.csv")
hosp_path = os.path.join(base_path, "3.COVID-19_hospital_and_ICU_admission_rates.csv")

print("--- PROFILING CASES AND DEATHS ---")
df_cases = pd.read_csv(cases_path, encoding='utf-8-sig')
print(f"Total Rows: {len(df_cases)}")
print("Columns:", list(df_cases.columns))
print("Countries and Territories (unique):", df_cases['countriesAndTerritories'].nunique())
print("Years represented:", df_cases['year'].unique())

print("\n--- PROFILING VACCINATION ---")
df_vacc = pd.read_csv(vacc_path, encoding='utf-8-sig')
print(f"Total Rows: {len(df_vacc)}")
print("Columns:", list(df_vacc.columns))
print("Vaccine Brands (unique):", list(df_vacc['Vaccine'].unique()))
print("Target Groups (unique):", list(df_vacc['TargetGroup'].unique()))

print("\n--- PROFILING HOSPITAL/ICU ---")
df_hosp = pd.read_csv(hosp_path, encoding='utf-8-sig')
print(f"Total Rows: {len(df_hosp)}")
print("Columns:", list(df_hosp.columns))
print("Indicators (unique):", list(df_hosp['indicator'].unique()))
print("Countries (unique):", df_hosp['country'].nunique(), list(df_hosp['country'].unique()))
