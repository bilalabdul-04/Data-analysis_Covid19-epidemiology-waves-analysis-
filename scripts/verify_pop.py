import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"
vacc_path = os.path.join(base_path, "2.COVID-19_vaccination.csv")
cases_path = os.path.join(base_path, "1.COVID-19_daily_number_of_new_cases_and_deaths.csv")

df_vacc = pd.read_csv(vacc_path, encoding='utf-8-sig')
df_cases = pd.read_csv(cases_path, encoding='utf-8-sig')

# Check Population in vacc
vacc_pop = df_vacc.groupby('ReportingCountry')['Population'].agg(['min', 'max', 'nunique'])
print("Vaccination population statistics by country:")
print(vacc_pop.head(10))

# Check popData2020 in cases
cases_pop = df_cases.groupby('countriesAndTerritories')['popData2020'].agg(['min', 'max', 'nunique'])
print("\nCases popData2020 statistics by country:")
print(cases_pop.head(10))
