import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"
vacc_path = os.path.join(base_path, "2.COVID-19_vaccination.csv")
df_vacc = pd.read_csv(vacc_path, encoding='utf-8-sig')

df_nat = df_vacc[df_vacc['Region'] == df_vacc['ReportingCountry']]
at_all = df_nat[(df_nat['ReportingCountry'] == 'AT') & (df_nat['TargetGroup'] == 'ALL')]

# Sort by week and print the first 10 weeks
at_all_sorted = at_all.groupby('YearWeekISO')['FirstDose'].sum().reset_index()
print("Austria (AT) 'ALL' FirstDose by week (first 10 weeks):")
print(at_all_sorted.head(10))

print("\nAustria (AT) 'ALL' FirstDose by week (last 10 weeks):")
print(at_all_sorted.tail(10))

# Sum of all weekly doses
print("\nSum of all weekly 'ALL' FirstDose in Austria:", at_all_sorted['FirstDose'].sum())
