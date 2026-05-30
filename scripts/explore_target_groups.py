import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"
vacc_path = os.path.join(base_path, "2.COVID-19_vaccination.csv")
df_vacc = pd.read_csv(vacc_path, encoding='utf-8-sig')

# Filter for a few countries and a specific week
for country in ['BE', 'BG', 'SE']:
    country_df = df_vacc[(df_vacc['ReportingCountry'] == country) & (df_vacc['YearWeekISO'] == '2021-W25') & (df_vacc['Vaccine'] == 'COM')]
    print(f"\n==================== {country} 2021-W25 ====================")
    cols = ['TargetGroup', 'FirstDose', 'SecondDose', 'Denominator']
    print(country_df[cols])
