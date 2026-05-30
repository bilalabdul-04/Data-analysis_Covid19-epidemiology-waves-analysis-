import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"
vacc_path = os.path.join(base_path, "2.COVID-19_vaccination.csv")
df_vacc = pd.read_csv(vacc_path, encoding='utf-8-sig')

# Keep only national rows
df_nat = df_vacc[df_vacc['Region'] == df_vacc['ReportingCountry']]

# Print target groups per country
print("Target groups reported by each country:")
grouped = df_nat.groupby('ReportingCountry')['TargetGroup'].unique()
for country, groups in grouped.items():
    print(f"{country}: {list(groups)}")
