import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"
cases_path = os.path.join(base_path, "1.COVID-19_daily_number_of_new_cases_and_deaths.csv")
df_cases = pd.read_csv(cases_path, encoding='utf-8-sig')

mapping = df_cases[['countriesAndTerritories', 'geoId']].drop_duplicates().set_index('countriesAndTerritories')['geoId'].to_dict()
print("Country mapping from cases dataset:")
print(mapping)
