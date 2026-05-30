import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"
vacc_path = os.path.join(base_path, "2.COVID-19_vaccination.csv")
df_vacc = pd.read_csv(vacc_path, encoding='utf-8-sig')

# Check Sweden (SE) unique regions
print("SE unique regions:")
print(df_vacc[df_vacc['ReportingCountry'] == 'SE']['Region'].unique())

# Check Austria (AT) unique regions
print("\nAT unique regions:")
print(df_vacc[df_vacc['ReportingCountry'] == 'AT']['Region'].unique())

# Let's see if there is any row where Region is different from ReportingCountry.
# If so, do they sum up to the country code? Or is it that some countries report by region, and some report by country?
print("\nIs Region always equal to ReportingCountry?")
print("Count of rows where Region == ReportingCountry:", (df_vacc['Region'] == df_vacc['ReportingCountry']).sum())
print("Count of rows where Region != ReportingCountry:", (df_vacc['Region'] != df_vacc['ReportingCountry']).sum())

print("\nSample rows where Region != ReportingCountry:")
print(df_vacc[df_vacc['Region'] != df_vacc['ReportingCountry']][['ReportingCountry', 'Region', 'TargetGroup', 'Vaccine', 'FirstDose']].head())
