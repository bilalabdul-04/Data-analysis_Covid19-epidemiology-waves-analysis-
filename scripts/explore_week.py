import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"
vacc_path = os.path.join(base_path, "2.COVID-19_vaccination.csv")
df_vacc = pd.read_csv(vacc_path, encoding='utf-8-sig')

# Look at AT for week 2021-W10
at_week = df_vacc[(df_vacc['ReportingCountry'] == 'AT') & (df_vacc['YearWeekISO'] == '2021-W10')]
print("Vaccine Brands present in AT 2021-W10:", at_week['Vaccine'].unique())
print("Columns of interest:")
cols = ['Vaccine', 'TargetGroup', 'FirstDose', 'SecondDose', 'Population', 'Denominator']
print(at_week[at_week['Vaccine'] == 'COM'][cols])
