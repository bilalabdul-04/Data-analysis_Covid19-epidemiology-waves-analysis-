import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"
vacc_path = os.path.join(base_path, "2.COVID-19_vaccination.csv")
df_vacc = pd.read_csv(vacc_path, encoding='utf-8-sig')

df_nat = df_vacc[df_vacc['Region'] == df_vacc['ReportingCountry']]

for country in ['AT', 'BE', 'DE', 'FR', 'SE']:
    sub = df_nat[df_nat['ReportingCountry'] == country]
    print(f"\n==================== {country} ====================")
    print("Unique target groups:", list(sub['TargetGroup'].unique()))
    all_rows = sub[sub['TargetGroup'] == 'ALL']
    print("ALL target group total FirstDose:", all_rows['FirstDose'].sum())
    print("ALL target group Max Denominator:", all_rows['Denominator'].max())
    print("ALL target group Max Population:", all_rows['Population'].max())
    
    # Let's sum specific age groups
    specific_groups = [g for g in sub['TargetGroup'].unique() if g not in ['ALL', 'AgeUNK', '1_Age60+', '1_Age<60', 'HCW', 'LTCF']]
    specific_sum = sub[sub['TargetGroup'].isin(specific_groups)]['FirstDose'].sum()
    print("Sum of specific age groups FirstDose:", specific_sum)
