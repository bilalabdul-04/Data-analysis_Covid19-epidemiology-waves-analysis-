import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"

# File paths
cases_path = os.path.join(base_path, "1.COVID-19_daily_number_of_new_cases_and_deaths.csv")
vacc_path = os.path.join(base_path, "2.COVID-19_vaccination.csv")
hosp_path = os.path.join(base_path, "3.COVID-19_hospital_and_ICU_admission_rates.csv")

# Load datasets
df_cases = pd.read_csv(cases_path, encoding='utf-8-sig')
df_vacc = pd.read_csv(vacc_path, encoding='utf-8-sig')
df_hosp = pd.read_csv(hosp_path, encoding='utf-8-sig')

print("--- CHECKING FIRST DOSE REFUSED ---")
print("Non-null FirstDoseRefused count:", df_vacc['FirstDoseRefused'].notna().sum())
print("Unique FirstDoseRefused values:", df_vacc['FirstDoseRefused'].dropna().unique())
print("Sample rows where FirstDoseRefused is populated:")
print(df_vacc[df_vacc['FirstDoseRefused'].notna() & (df_vacc['FirstDoseRefused'] != '')].head())

print("\n--- CHECKING HOSPITAL/ICU REPORTING COUNTRIES ---")
hosp_by_country_ind = df_hosp.groupby(['country', 'indicator']).size().unstack(fill_value=0)
print(hosp_by_country_ind)

print("\n--- CHECKING VACCINATION UNDER AGE 18 ---")
sub18_df = df_vacc[df_vacc['TargetGroup'].isin(['Age<18', 'Age0_4', 'Age5_9', 'Age10_14', 'Age15_17'])]
print("Under 18 records target groups:", sub18_df['TargetGroup'].value_counts())
print("Does Age<18 cover all under 18? Or are they separate?")
print("Compare AT 'Age<18' sum of FirstDose vs specific groups:")
at_sub18 = df_vacc[df_vacc['ReportingCountry'] == 'AT']
print("AT TargetGroup counts:")
print(at_sub18.groupby('TargetGroup')['FirstDose'].sum())
