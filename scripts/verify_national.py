import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"
vacc_path = os.path.join(base_path, "2.COVID-19_vaccination.csv")
df_vacc = pd.read_csv(vacc_path, encoding='utf-8-sig')

# Check unique reporting countries
countries = df_vacc['ReportingCountry'].unique()
print(f"Total reporting countries in vaccination: {len(countries)}")

# For each country, see if there are rows where Region == ReportingCountry
has_national = []
missing_national = []
for c in countries:
    sub = df_vacc[df_vacc['ReportingCountry'] == c]
    has_nat = (sub['Region'] == c).any()
    if has_nat:
        has_national.append(c)
    else:
        missing_national.append(c)

print("Countries with national rows (Region == ReportingCountry):", len(has_national), has_national)
print("Countries missing national rows:", len(missing_national), missing_national)
