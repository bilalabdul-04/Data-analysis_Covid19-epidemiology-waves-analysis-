import pandas as pd
import os

base_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\extracted\Assignment 2_datasets"
vacc_path = os.path.join(base_path, "2.COVID-19_vaccination.csv")
df_vacc = pd.read_csv(vacc_path, encoding='utf-8-sig')

df_nat = df_vacc[df_vacc['Region'] == df_vacc['ReportingCountry']]

results = []

for country in df_nat['ReportingCountry'].unique():
    sub = df_nat[df_nat['ReportingCountry'] == country]
    
    # Adult doses (ALL)
    adult_first = sub[sub['TargetGroup'] == 'ALL']['FirstDose'].sum()
    adult_second = sub[sub['TargetGroup'] == 'ALL']['SecondDose'].sum()
    
    # Under 18 groups
    sub18 = sub[sub['TargetGroup'].isin(['Age<18', 'Age15_17', 'Age10_14', 'Age5_9', 'Age0_4'])]
    # To avoid double counting, if 'Age<18' is present, use it. Otherwise, sum the specific ones.
    if 'Age<18' in sub['TargetGroup'].unique():
        child_first = sub[sub['TargetGroup'] == 'Age<18']['FirstDose'].sum()
        child_second = sub[sub['TargetGroup'] == 'Age<18']['SecondDose'].sum()
    else:
        # Sum specific under 18 groups
        child_first = sub[sub['TargetGroup'].isin(['Age15_17', 'Age10_14', 'Age5_9', 'Age0_4'])]['FirstDose'].sum()
        child_second = sub[sub['TargetGroup'].isin(['Age15_17', 'Age10_14', 'Age5_9', 'Age0_4'])]['SecondDose'].sum()
        
    total_first = adult_first + child_first
    total_second = adult_second + child_second
    
    pop = sub['Population'].max()
    
    first_rate = total_first / pop if pop > 0 else 0
    second_rate = total_second / pop if pop > 0 else 0
    
    results.append({
        'Country': country,
        'Population': pop,
        'Total_FirstDose': total_first,
        'Total_SecondDose': total_second,
        'FirstDose_Rate': first_rate,
        'SecondDose_Rate': second_rate
    })

df_res = pd.DataFrame(results).sort_values(by='FirstDose_Rate', ascending=True)
print("Vaccination Rates by Country (sorted by FirstDose_Rate ascending - most skeptical first):")
print(df_res.to_string(index=False))
