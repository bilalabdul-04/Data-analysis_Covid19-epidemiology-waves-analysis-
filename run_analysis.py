import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import pearsonr, wilcoxon

# Set up custom plot styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Liberation Sans']
plt.rcParams['axes.edgecolor'] = '#BDC3C7'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['xtick.color'] = '#2C3E50'
plt.rcParams['ytick.color'] = '#2C3E50'

# Configuration
base_path = os.path.join(os.path.dirname(__file__), "data")
plots_dir = os.path.join(os.path.dirname(__file__), "plots")
os.makedirs(plots_dir, exist_ok=True)

# Datasets
cases_file = os.path.join(base_path, "1.COVID-19_daily_number_of_new_cases_and_deaths.csv")
vacc_file = os.path.join(base_path, "2.COVID-19_vaccination.csv")
hosp_file = os.path.join(base_path, "3.COVID-19_hospital_and_ICU_admission_rates.csv")

# 1. Unified Country Mapping (from cases dataset)
df_cases_temp = pd.read_csv(cases_file, encoding='utf-8-sig')
country_map = df_cases_temp[['countriesAndTerritories', 'geoId']].drop_duplicates().set_index('countriesAndTerritories')['geoId'].to_dict()
# Standardize manual keys or spelling differences
country_map.update({
    'Czech Republic': 'CZ',
    'Czechia': 'CZ',
    'Greece': 'EL', # ECDC uses EL for Greece
    'Slovakia': 'SK',
})

# Hardcoded country coordinates for custom bubble maps (replaces heavy geopandas)
country_coords = {
    'AT': (47.5162, 14.5501), 'BE': (50.5039, 4.4699), 'BG': (42.7339, 25.4858),
    'CY': (35.1264, 33.4299), 'CZ': (49.8175, 15.4730), 'DE': (51.1657, 10.4515),
    'DK': (56.2639, 9.5018),  'EE': (58.5953, 25.0136), 'EL': (39.0742, 21.8243),
    'ES': (40.4637, -3.7492), 'FI': (61.9241, 25.7482), 'FR': (46.2276, 2.2137),
    'HR': (45.1000, 15.2000), 'HU': (47.1625, 19.5033), 'IE': (53.4129, -8.2439),
    'IS': (64.9631, -19.0208), 'IT': (41.8719, 12.5674), 'LI': (47.1660, 9.5554),
    'LT': (55.1694, 23.8813), 'LU': (49.8153, 6.1296),  'LV': (56.8796, 24.6032),
    'MT': (35.9375, 14.3754), 'NL': (52.1326, 5.2913),  'NO': (60.4720, 8.4689),
    'PL': (51.9194, 19.1451), 'PT': (39.3999, -8.2245), 'RO': (45.9432, 24.9668),
    'SE': (60.1282, 18.6435), 'SI': (46.1512, 14.9955), 'SK': (48.6690, 19.6990)
}

# Mapping vaccine codes to full brand names
vaccine_names = {
    'COM': 'Comirnaty (Pfizer/BioNTech)',
    'COMBA.1': 'Comirnaty Bivalent (Pfizer/BioNTech)',
    'COMBA.4-5': 'Comirnaty Bivalent (Pfizer/BioNTech)',
    'COMBIV': 'Comirnaty Bivalent (Pfizer/BioNTech)',
    'MOD': 'Spikevax (Moderna)',
    'MODBA.1': 'Spikevax Bivalent (Moderna)',
    'MODBA.4-5': 'Spikevax Bivalent (Moderna)',
    'MODBIV': 'Spikevax Bivalent (Moderna)',
    'AZ': 'Vaxzevria (AstraZeneca)',
    'JANSS': 'Jcovden (Janssen/J&J)',
    'NVXD': 'Nuvaxovid (Novavax)',
    'VLA': 'Valneva',
    'SPU': 'Sputnik V',
    'SIN': 'Sinopharm',
    'BECNBG': 'BBIBP-CorV (Sinopharm)',
    'BHACOV': 'Covaxin (Bharat Biotech)',
    'SGSK': 'Sanofi-GSK',
    'UNK': 'Unknown Vaccine'
}

# ----------------- INGEST AND CLEAN DATA -----------------
print("Ingesting datasets...")
df_cases = pd.read_csv(cases_file, encoding='utf-8-sig')
df_vacc = pd.read_csv(vacc_file, encoding='utf-8-sig')
df_hosp = pd.read_csv(hosp_file, encoding='utf-8-sig')

# Standardize cases dateRep
df_cases['date'] = pd.to_datetime(df_cases['dateRep'], format='%d/%m/%Y')
df_cases = df_cases[(df_cases['date'].dt.year >= 2020) & (df_cases['date'].dt.year <= 2022)]

# Clean vaccination country names and ensure national filter
# Region == ReportingCountry ensures no subnational double-counting
df_vacc_nat = df_vacc[df_vacc['Region'] == df_vacc['ReportingCountry']].copy()

# Add standardised ISO country codes to hospital dataset
df_hosp['geoId'] = df_hosp['country'].map(country_map)
# Exclude rows without coordinates or geoId mapping
df_hosp = df_hosp[df_hosp['geoId'].notna()]


# ----------------- SECTION 3.1: MANDATORY QUESTIONS -----------------

def run_q1():
    print("\n--- Solving Q1: Top 10 Countries and Quarterly Waves ---")
    # Identify top 10 countries overall (2020-2022) by total cases
    country_totals = df_cases.groupby('countriesAndTerritories')['cases'].sum()
    top_10_countries = country_totals.nlargest(10).index.tolist()
    print("Top 10 Countries by Total Cases:", top_10_countries)
    
    # Calculate cases by year-quarter
    df_cases['year_quarter'] = df_cases['date'].dt.to_period('Q').astype(str)
    
    # Filter for top 10
    df_top_10 = df_cases[df_cases['countriesAndTerritories'].isin(top_10_countries)]
    
    # Pivot cases by country and quarter
    q_cases = df_top_10.pivot_table(index='countriesAndTerritories', columns='year_quarter', values='cases', aggfunc='sum')
    q_cases.to_csv(os.path.join(plots_dir, "q1_quarterly_cases.csv"))
    
    # Calculate percentage of population infected
    # We will get population from popData2020
    pop_df = df_cases[df_cases['countriesAndTerritories'].isin(top_10_countries)][['countriesAndTerritories', 'popData2020']].drop_duplicates().set_index('countriesAndTerritories')
    total_cases = country_totals.loc[top_10_countries]
    
    pop_compare = pd.DataFrame({
        'Total_Cases': total_cases,
        'Population_2020': pop_df['popData2020'],
        'Infection_Rate_Pct': (total_cases / pop_df['popData2020']) * 100
    }).sort_values(by='Infection_Rate_Pct', ascending=False)
    
    print("\nInfection Rate as a Percentage of Country Population:")
    print(pop_compare)
    pop_compare.to_csv(os.path.join(plots_dir, "q1_population_infection_rates.csv"))
    
    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6.5))
    colors = ['#2C3E50', '#16A085', '#2980B9', '#8E44AD', '#D35400', '#C0392B', '#7F8C8D', '#1abc9c', '#3498db', '#9b59b6']
    
    for i, country in enumerate(top_10_countries):
        series = q_cases.loc[country]
        ax.plot(series.index, series.values / 1e6, label=country, color=colors[i], marker='o', linewidth=2.0, markersize=5)
        
    ax.set_title("Quarterly COVID-19 Cases for Top 10 EU/EEA Countries (2020-2022)", fontsize=14, fontweight='bold', pad=15, color='#2C3E50')
    ax.set_xlabel("Year & Quarter", fontsize=11, labelpad=10)
    ax.set_ylabel("New Cases (Millions)", fontsize=11, labelpad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['bottom'].set_color('#BDC3C7')
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#BDC3C7')
    ax.set_facecolor('white')
    ax.legend(frameon=False, loc='upper left', ncol=2, fontsize=9.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "q1_quarterly_cases_trends.png"), dpi=300)
    plt.close()


def run_q2():
    print("\n--- Solving Q2: Spatial Bubble Map of Cases and Deaths ---")
    # We will generate static high-end coordinate bubble plots (replaces interactive maps for the LaTeX report)
    # Group by country and year
    df_cases['year_str'] = df_cases['date'].dt.year.astype(str)
    
    # Map country name in cases to geoId
    df_cases['geoId'] = df_cases['countriesAndTerritories'].map(country_map)
    df_cases_filtered = df_cases[df_cases['geoId'].notna()].copy()
    
    for year in ['2020', '2021', '2022']:
        df_year = df_cases_filtered[df_cases_filtered['year_str'] == year]
        geo_agg = df_year.groupby('geoId').agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()
        
        # Add coordinates
        geo_agg['lat'] = geo_agg['geoId'].map(lambda x: country_coords[x][0] if x in country_coords else np.nan)
        geo_agg['lon'] = geo_agg['geoId'].map(lambda x: country_coords[x][1] if x in country_coords else np.nan)
        geo_agg = geo_agg.dropna()
        
        # Plot bubble map representing Europe geographically
        fig, axes = plt.subplots(1, 2, figsize=(15, 8.5), facecolor='white')
        
        # Subplot 1: Cases
        ax = axes[0]
        ax.set_facecolor('#F8F9FA')
        sc1 = ax.scatter(geo_agg['lon'], geo_agg['lat'], s=geo_agg['cases'] / 1e4 * 1.5 + 40,
                         c=geo_agg['cases'] / 1e6, cmap='Blues', alpha=0.8, edgecolors='#34495E', linewidths=0.8, zorder=2)
        ax.set_title(f"Cumulative COVID-19 Cases ({year})", fontsize=13, fontweight='bold', color='#2C3E50')
        
        # Annotate country initials
        for idx, row in geo_agg.iterrows():
            ax.annotate(row['geoId'], (row['lon'], row['lat']), fontsize=7, color='#2C3E50', weight='bold', ha='center', va='center')
            
        # Draw clean grid lines resembling map latitude/longitude lines
        ax.grid(True, linestyle='--', color='#E2E8F0', alpha=0.5)
        ax.set_xlim(-25, 35) # Longitude range covering EU/EEA
        ax.set_ylim(34, 72)  # Latitude range covering EU/EEA
        ax.set_xlabel("Longitude (°E)", fontsize=9, color='#7F8C8D')
        ax.set_ylabel("Latitude (°N)", fontsize=9, color='#7F8C8D')
        ax.spines['top'].set_color('#E2E8F0')
        ax.spines['right'].set_color('#E2E8F0')
        ax.spines['left'].set_color('#E2E8F0')
        ax.spines['bottom'].set_color('#E2E8F0')
        
        cbar1 = fig.colorbar(sc1, ax=ax, orientation='horizontal', pad=0.08, shrink=0.7)
        cbar1.set_label("Cases (Millions)", fontsize=9, color='#2C3E50')
        cbar1.ax.tick_params(labelsize=8)
        
        # Subplot 2: Deaths
        ax = axes[1]
        ax.set_facecolor('#F8F9FA')
        sc2 = ax.scatter(geo_agg['lon'], geo_agg['lat'], s=geo_agg['deaths'] / 1e2 * 1.5 + 40,
                         c=geo_agg['deaths'] / 1e3, cmap='Reds', alpha=0.8, edgecolors='#34495E', linewidths=0.8, zorder=2)
        ax.set_title(f"Cumulative COVID-19 Deaths ({year})", fontsize=13, fontweight='bold', color='#2C3E50')
        
        # Annotate country initials
        for idx, row in geo_agg.iterrows():
            ax.annotate(row['geoId'], (row['lon'], row['lat']), fontsize=7, color='#2C3E50', weight='bold', ha='center', va='center')
            
        ax.grid(True, linestyle='--', color='#E2E8F0', alpha=0.5)
        ax.set_xlim(-25, 35)
        ax.set_ylim(34, 72)
        ax.set_xlabel("Longitude (°E)", fontsize=9, color='#7F8C8D')
        ax.spines['top'].set_color('#E2E8F0')
        ax.spines['right'].set_color('#E2E8F0')
        ax.spines['left'].set_color('#E2E8F0')
        ax.spines['bottom'].set_color('#E2E8F0')
        
        cbar2 = fig.colorbar(sc2, ax=ax, orientation='horizontal', pad=0.08, shrink=0.7)
        cbar2.set_label("Deaths (Thousands)", fontsize=9, color='#2C3E50')
        cbar2.ax.tick_params(labelsize=8)
        
        plt.suptitle(f"Spatio-Temporal Distribution of COVID-19 Cases and Deaths across EU/EEA - {year}", fontsize=15, fontweight='bold', color='#2C3E50', y=0.98)
        plt.tight_layout()
        plt.savefig(os.path.join(plots_dir, f"q2_spatial_bubble_map_{year}.png"), dpi=300, bbox_inches='tight')
        plt.close()
        
        # Save geo agg data for mapping verification
        geo_agg.to_csv(os.path.join(plots_dir, f"q2_spatial_data_{year}.csv"), index=False)


def run_q3():
    print("\n--- Solving Q3: Top 3 Vaccine Brands and Popularity Exceptions ---")
    # Identify popular vaccine brands by summing FirstDose + SecondDose + DoseAdditional1 + DoseAdditional2
    dose_cols = [c for c in df_vacc_nat.columns if 'Dose' in c and c != 'FirstDoseRefused' and c != 'UnknownDose']
    df_vacc_nat['Total_Doses_Administered'] = df_vacc_nat[dose_cols].sum(axis=1)
    
    # 1. Brand popularity overall (we look at ALL target groups to get totals)
    brand_agg = df_vacc_nat[df_vacc_nat['TargetGroup'] == 'ALL'].groupby('Vaccine')['Total_Doses_Administered'].sum()
    brand_shares = (brand_agg / brand_agg.sum()) * 100
    top_brands = brand_agg.nlargest(5)
    
    print("\nOverall Vaccine Brand Doses Administered in EU/EEA (ALL target groups):")
    for vaccine, doses in top_brands.items():
        name = vaccine_names.get(vaccine, vaccine)
        share = brand_shares.loc[vaccine]
        print(f"- {name} ({vaccine}): {doses:,.0f} doses ({share:.2f}%)")
        
    top_3_overall = top_brands.head(3).index.tolist()
    
    # 2. Country-level popularity analysis
    country_brand_agg = df_vacc_nat[df_vacc_nat['TargetGroup'] == 'ALL'].groupby(['ReportingCountry', 'Vaccine'])['Total_Doses_Administered'].sum().unstack(fill_value=0)
    
    # Find top 3 brands for each country
    exceptions = []
    print("\nCountry-Level Exceptions (Countries where the top 3 overall brands are not the top 3 in that country):")
    for country in country_brand_agg.index:
        country_doses = country_brand_agg.loc[country]
        top_3_country = country_doses.nlargest(3).index.tolist()
        
        # Check if country's top 3 is identical to top 3 overall
        # Top 3 overall are COM (Pfizer), MOD (Moderna), AZ (AstraZeneca)
        is_exception = not all(b in top_3_overall for b in top_3_country)
        if is_exception:
            country_shares = (country_doses / country_doses.sum()) * 100
            print(f"\nCountry: {country}")
            print("  Top 3 Brands & Shares in Country:")
            for b in top_3_country:
                name = vaccine_names.get(b, b)
                print(f"    - {name} ({b}): {country_doses[b]:,.0f} doses ({country_shares[b]:.2f}%)")
            exceptions.append(country)
            
    # Plotting Overall Brand Shares
    fig, ax = plt.subplots(figsize=(10, 6.5))
    brand_agg_sorted = brand_agg.sort_values(ascending=False)
    # Group small ones into Other
    main_brands = brand_agg_sorted.head(4)
    other_sum = brand_agg_sorted.iloc[4:].sum()
    main_brands['Other'] = other_sum
    
    labels = [vaccine_names.get(b, b) for b in main_brands.index]
    colors = ['#34495E', '#5C6BC0', '#26A69A', '#E74C3C', '#BDC3C7']
    
    wedges, texts, autotexts = ax.pie(main_brands.values, labels=labels, autopct='%1.1f%%',
                                      startangle=140, colors=colors, wedgeprops=dict(edgecolor='white', linewidth=1.5),
                                      textprops=dict(fontsize=10, color='#2C3E50'))
    plt.setp(autotexts, size=9.5, weight="bold")
    ax.set_title("COVID-19 Vaccine Brand Distribution across EU/EEA Countries (ALL Groups)", fontsize=13, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "q3_vaccine_brand_distribution.png"), dpi=300)
    plt.close()
    
    # Save datasets
    brand_agg.to_csv(os.path.join(plots_dir, "q3_brand_totals.csv"))
    country_brand_agg.to_csv(os.path.join(plots_dir, "q3_country_brand_totals.csv"))
    return top_3_overall


def run_q4(top_3_overall):
    print("\n--- Solving Q4: Target Groups for Top 3 Vaccine Brands ---")
    # Exclude aggregate target groups to focus on specific age groups and key demographic cohorts (HCW, LTCF)
    agg_groups = ['ALL', '1_Age60+', '1_Age<60', 'AgeUNK']
    specific_vacc_df = df_vacc_nat[~df_vacc_nat['TargetGroup'].isin(agg_groups)].copy()
    
    # Group by Vaccine and TargetGroup
    tg_vacc_agg = specific_vacc_df.groupby(['Vaccine', 'TargetGroup'])['Total_Doses_Administered'].sum().unstack(fill_value=0)
    
    print("\nDemographic Distribution of top 3 Vaccine Brands (Doses Administered):")
    for vaccine in top_3_overall:
        name = vaccine_names.get(vaccine, vaccine)
        print(f"\nVaccine: {name} ({vaccine})")
        shares = (tg_vacc_agg.loc[vaccine] / tg_vacc_agg.loc[vaccine].sum()) * 100
        top_groups = tg_vacc_agg.loc[vaccine].nlargest(5)
        for tg, doses in top_groups.items():
            print(f"  - {tg}: {doses:,.0f} doses ({shares[tg]:.2f}%)")
            
    # Visualize demographic comparison for the top 3 vaccines
    fig, axes = plt.subplots(3, 1, figsize=(11, 13), sharex=True)
    colors = ['#2C3E50', '#26A69A', '#E74C3C']
    
    for i, vaccine in enumerate(top_3_overall):
        ax = axes[i]
        shares = (tg_vacc_agg.loc[vaccine] / tg_vacc_agg.loc[vaccine].sum()) * 100
        shares.plot(kind='bar', ax=ax, color=colors[i], edgecolor='white', linewidth=0.5, alpha=0.9)
        ax.set_title(f"Target Group Distribution for {vaccine_names.get(vaccine, vaccine)}", fontsize=11, fontweight='bold', pad=10, color='#2C3E50')
        ax.set_ylabel("Share of Doses (%)", fontsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#BDC3C7')
        ax.spines['bottom'].set_color('#BDC3C7')
        ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#BDC3C7')
        ax.set_facecolor('white')
        
    plt.xlabel("Demographic/Occupational Target Groups", fontsize=11, labelpad=10)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "q4_vaccine_brand_demographics.png"), dpi=300)
    plt.close()
    
    tg_vacc_agg.to_csv(os.path.join(plots_dir, "q4_target_group_vaccine_matrix.csv"))


def run_q5():
    print("\n--- Solving Q5: Vaccine Skepticism and Hospitalization Burden ---")
    # 1. Calculate national-level first-dose rate (Skepticism = 1 - FirstDose_Rate)
    results = []
    for country in df_vacc_nat['ReportingCountry'].unique():
        sub = df_vacc_nat[df_vacc_nat['ReportingCountry'] == country]
        pop = sub['Population'].max()
        if pop == 0 or np.isnan(pop):
            continue
            
        adult_first = sub[sub['TargetGroup'] == 'ALL']['FirstDose'].sum()
        
        # Children first doses (avoiding double counting)
        if 'Age<18' in sub['TargetGroup'].unique():
            child_first = sub[sub['TargetGroup'] == 'Age<18']['FirstDose'].sum()
        else:
            child_first = sub[sub['TargetGroup'].isin(['Age15_17', 'Age10_14', 'Age5_9', 'Age0_4'])]['FirstDose'].sum()
            
        total_first = adult_first + child_first
        first_rate = total_first / pop
        skepticism_rate = 1.0 - first_rate
        
        results.append({
            'geoId': country,
            'Population': pop,
            'FirstDose_Rate': first_rate,
            'Skepticism_Rate': skepticism_rate
        })
        
    df_skep = pd.DataFrame(results)
    
    # 2. Extract country-level hospitalization burden in 2021 (when vaccination rolled out)
    # We will use 'Weekly new hospital admissions per 100k' as it is robust and standardized across countries
    df_hosp_filtered = df_hosp[df_hosp['indicator'] == 'Weekly new hospital admissions per 100k'].copy()
    df_hosp_filtered['date_dt'] = pd.to_datetime(df_hosp_filtered['date'])
    df_hosp_2021 = df_hosp_filtered[df_hosp_filtered['date_dt'].dt.year == 2021]
    
    # Calculate peak weekly hospital admissions per 100k in 2021
    hosp_burden = df_hosp_2021.groupby('geoId')['value'].max().reset_index()
    hosp_burden.rename(columns={'value': 'Peak_Weekly_Hosp_per_100k_2021'}, inplace=True)
    
    # Merge datasets
    merged = pd.merge(df_skep, hosp_burden, on='geoId')
    
    print("\nMerged Vaccine Skepticism and Peak Hospitalizations (2021):")
    print(merged.sort_values(by='Skepticism_Rate', ascending=False).to_string(index=False))
    merged.to_csv(os.path.join(plots_dir, "q5_skepticism_vs_hospitalization.csv"), index=False)
    
    # Perform Pearson Correlation test
    r_coeff, p_value = pearsonr(merged['Skepticism_Rate'], merged['Peak_Weekly_Hosp_per_100k_2021'])
    print(f"\nPearson Correlation (Skepticism vs. Peak Hospital Burden):")
    print(f"  - Correlation Coefficient (r): {r_coeff:.4f}")
    print(f"  - p-value: {p_value:.4f}")
    
    # Plotting Scatter with Regression line
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.regplot(data=merged, x='Skepticism_Rate', y='Peak_Weekly_Hosp_per_100k_2021',
                scatter_kws={'s': merged['Population'] / 5e5 + 40, 'color': '#2C3E50', 'alpha': 0.7, 'edgecolors': '#34495E', 'linewidths': 0.8},
                line_kws={'color': '#E74C3C', 'linewidth': 1.5, 'label': f'Regression Line (r={r_coeff:.2f}, p={p_value:.4f})'}, ax=ax)
    
    # Annotate country tags
    for idx, row in merged.iterrows():
        ax.annotate(row['geoId'], (row['Skepticism_Rate'], row['Peak_Weekly_Hosp_per_100k_2021']),
                    textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color='#34495E', weight='bold')
        
    ax.set_title("COVID-19 Vaccine Skepticism vs. Peak Weekly Hospitalizations (2021)", fontsize=13, fontweight='bold', color='#2C3E50', pad=15)
    ax.set_xlabel("Vaccine Skepticism Rate (1 - First Dose Coverage)", fontsize=11, labelpad=10)
    ax.set_ylabel("Peak Weekly Hospital Admissions per 100k (2021)", fontsize=11, labelpad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['bottom'].set_color('#BDC3C7')
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#BDC3C7')
    ax.set_facecolor('white')
    ax.legend(frameon=False, loc='upper left', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "q5_skepticism_vs_hospital_burden.png"), dpi=300)
    plt.close()


def run_q6():
    print("\n--- Solving Q6: Under-18 First-Dose Vaccination Ranks ---")
    results = []
    for country in df_vacc_nat['ReportingCountry'].unique():
        sub = df_vacc_nat[df_vacc_nat['ReportingCountry'] == country]
        pop = sub['Population'].max()
        if pop == 0 or np.isnan(pop):
            continue
            
        # Children first doses
        if 'Age<18' in sub['TargetGroup'].unique():
            child_first = sub[sub['TargetGroup'] == 'Age<18']['FirstDose'].sum()
        else:
            child_first = sub[sub['TargetGroup'].isin(['Age15_17', 'Age10_14', 'Age5_9', 'Age0_4'])]['FirstDose'].sum()
            
        rate_of_total_pop = child_first / pop
        
        results.append({
            'geoId': country,
            'Total_Population': pop,
            'Under18_FirstDose': child_first,
            'Under18_Rate_of_Total_Pop': rate_of_total_pop
        })
        
    df_u18 = pd.DataFrame(results).sort_values(by='Under18_Rate_of_Total_Pop', ascending=False)
    print("\nRankings of Under-18 First Dose Vaccination Rates (Relative to Country Total Population):")
    print(df_u18.to_string(index=False))
    df_u18.to_csv(os.path.join(plots_dir, "q6_under18_vaccination_ranks.csv"), index=False)
    
    # Plotting rankings
    fig, ax = plt.subplots(figsize=(11, 7.5))
    colors = ['#16A085' if x >= 0.10 else '#7F8C8D' for x in df_u18['Under18_Rate_of_Total_Pop']]
    # Highlight top 3 and bottom 3
    for i in range(len(colors)):
        if i < 3:
            colors[i] = '#2E7D32' # Strong green
        elif i >= len(colors) - 3:
            colors[i] = '#C62828' # Strong red
            
    bars = ax.bar(df_u18['geoId'], df_u18['Under18_Rate_of_Total_Pop'] * 100, color=colors, edgecolor='white', linewidth=0.5, alpha=0.9)
    
    # Annotate heights
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=7, color='#34495E', weight='bold')
        
    ax.set_title("First-Dose COVID-19 Vaccinations under Age 18 (Relative to Total Country Population)", fontsize=13, fontweight='bold', color='#2C3E50', pad=15)
    ax.set_ylabel("Vaccinated Under-18 Population Share (%)", fontsize=11, labelpad=10)
    ax.set_xlabel("Country Code (ISO)", fontsize=11, labelpad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['bottom'].set_color('#BDC3C7')
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#BDC3C7')
    ax.set_facecolor('white')
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "q6_under18_vaccination_ranks.png"), dpi=300)
    plt.close()


def run_q7():
    print("\n--- Solving Q7: Oldest Second-Dose Vaccinated Population ---")
    # Define Midpoint ages for age cohorts
    age_midpoints = {
        'Age0_4': 2.5, 'Age5_9': 7.0, 'Age10_14': 12.0, 'Age15_17': 16.0,
        'Age<18': 9.0, 'Age18_24': 21.0, 'Age25_49': 37.0, 'Age50_59': 54.5,
        'Age60_69': 64.5, 'Age70_79': 74.5, 'Age80+': 85.0
    }
    
    # Exclude occupational/aggregate groups
    non_age_groups = ['ALL', '1_Age60+', '1_Age<60', 'HCW', 'LTCF', 'AgeUNK']
    age_vacc = df_vacc_nat[~df_vacc_nat['TargetGroup'].isin(non_age_groups)].copy()
    
    # Check that the country has age categories mapped
    age_vacc = age_vacc[age_vacc['TargetGroup'].isin(age_midpoints.keys())]
    age_vacc['Midpoint'] = age_vacc['TargetGroup'].map(age_midpoints)
    
    # Calculate weighted second dose recipient age per country
    country_ages = []
    for country in df_vacc_nat['ReportingCountry'].unique():
        country_data = df_vacc_nat[df_vacc_nat['ReportingCountry'] == country]
        unique_groups = country_data['TargetGroup'].unique()
        
        has_granular = any(g in unique_groups for g in ['Age18_24', 'Age25_49', 'Age50_59', 'Age80+'])
        
        if has_granular:
            sub = age_vacc[age_vacc['ReportingCountry'] == country]
            weighted_sum = (sub['SecondDose'] * sub['Midpoint']).sum()
            total_second = sub['SecondDose'].sum()
        else:
            # Fallback for countries like Germany that do not report granular age groups
            coarse_midpoints = {
                'Age<18': 9.0,
                '1_Age<60': 39.0,
                '1_Age60+': 72.5
            }
            sub = country_data[country_data['TargetGroup'].isin(coarse_midpoints.keys())].copy()
            sub['Midpoint'] = sub['TargetGroup'].map(coarse_midpoints)
            weighted_sum = (sub['SecondDose'] * sub['Midpoint']).sum()
            total_second = sub['SecondDose'].sum()
            
        if total_second == 0:
            continue
            
        weighted_avg_age = weighted_sum / total_second
        pop = country_data['Population'].max()
        
        country_ages.append({
            'geoId': country,
            'Total_Population': pop,
            'Total_SecondDoses_Sum': total_second,
            'Weighted_Average_Age': weighted_avg_age
        })
        
    df_ages = pd.DataFrame(country_ages).sort_values(by='Weighted_Average_Age', ascending=False)
    print("\nRankings of Country Weighted Average Age of Second Dose Recipients:")
    print(df_ages.to_string(index=False))
    df_ages.to_csv(os.path.join(plots_dir, "q7_weighted_average_age_ranks.csv"), index=False)
    
    # Plotting rankings
    fig, ax = plt.subplots(figsize=(11, 7.5))
    colors = ['#8E44AD' if x >= 55.0 else '#7F8C8D' for x in df_ages['Weighted_Average_Age']]
    for i in range(len(colors)):
        if i < 3:
            colors[i] = '#4A148C' # Oldest (Deep purple)
        elif i >= len(colors) - 3:
            colors[i] = '#D1C4E9' # Youngest (Light lavender)
            
    bars = ax.bar(df_ages['geoId'], df_ages['Weighted_Average_Age'], color=colors, edgecolor='white', linewidth=0.5, alpha=0.9)
    
    # Annotate heights
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.1f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=7.5, color='#34495E', weight='bold')
        
    ax.set_title("Weighted Average Age of Second-Dose COVID-19 Vaccine Recipients across EU/EEA", fontsize=13, fontweight='bold', color='#2C3E50', pad=15)
    ax.set_ylabel("Weighted Average Age (Years)", fontsize=11, labelpad=10)
    ax.set_xlabel("Country Code (ISO)", fontsize=11, labelpad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['bottom'].set_color('#BDC3C7')
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#BDC3C7')
    ax.set_facecolor('white')
    ax.set_ylim(0, 75)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "q7_weighted_average_age_ranks.png"), dpi=300)
    plt.close()


def run_q8():
    print("\n--- Solving Q8: Healthcare Burden Comparison (2020 vs 2022) ---")
    # Clean indicator and dates
    df_hosp['date_dt'] = pd.to_datetime(df_hosp['date'])
    df_hosp['year_str'] = df_hosp['date_dt'].dt.year.astype(str)
    
    # Hospital/ICU indicators of interest:
    # 1. Daily hospital occupancy (normalized per country population if possible, or total)
    # ECDC lists:
    # - 'Daily hospital occupancy'
    # - 'Daily ICU occupancy'
    # - 'Weekly new hospital admissions per 100k'
    # - 'Weekly new ICU admissions per 100k'
    #
    # We will use 'Daily hospital occupancy' and 'Daily ICU occupancy' and normalize them by popData2020 to get rates.
    # To check who is affected, we calculate the peak daily hospital and ICU occupancy per 100k.
    # Standardise full country names to ISO-2 codes to fetch popData2020
    pop_mapping = df_cases[['geoId', 'popData2020']].drop_duplicates().set_index('geoId')['popData2020'].to_dict()
    
    hosp_occ = df_hosp[df_hosp['indicator'].isin(['Daily hospital occupancy', 'Daily ICU occupancy'])].copy()
    hosp_occ['Population'] = hosp_occ['geoId'].map(pop_mapping)
    hosp_occ = hosp_occ.dropna(subset=['Population'])
    
    # Calculate occupancy per 100k
    hosp_occ['value_per_100k'] = (hosp_occ['value'] / hosp_occ['Population']) * 1e5
    
    # Peak occupancy in 2020 vs 2022
    occ_agg = hosp_occ.groupby(['geoId', 'indicator', 'year_str'])['value_per_100k'].max().unstack(fill_value=np.nan)
    occ_agg = occ_agg[['2020', '2022']].dropna().reset_index()
    
    print("\nHealthcare Burden: Peak Occupancy per 100k (2020 vs 2022):")
    print(occ_agg.sort_values(by=['indicator', '2020'], ascending=[True, False]).to_string(index=False))
    occ_agg.to_csv(os.path.join(plots_dir, "q8_healthcare_burden_comparison.csv"), index=False)
    
    # Separate plots for Hospital and ICU Occupancy
    for indicator in ['Daily hospital occupancy', 'Daily ICU occupancy']:
        sub = occ_agg[occ_agg['indicator'] == indicator].sort_values(by='2020', ascending=False)
        if len(sub) == 0:
            continue
            
        fig, ax = plt.subplots(figsize=(11, 6.5))
        
        # Set up side-by-side bars
        x = np.arange(len(sub))
        width = 0.35
        
        rects1 = ax.bar(x - width/2, sub['2020'], width, label='2020 (Pre-vaccine / Wild Type)', color='#34495E', edgecolor='white', alpha=0.9)
        rects2 = ax.bar(x + width/2, sub['2022'], width, label='2022 (Post-vaccine / Omicron)', color='#26A69A', edgecolor='white', alpha=0.9)
        
        ax.set_title(f"Peak {indicator} per 100k Population (2020 vs. 2022)", fontsize=13, fontweight='bold', color='#2C3E50', pad=15)
        ax.set_ylabel("Occupancy per 100k Population", fontsize=11, labelpad=10)
        ax.set_xlabel("Country Code (ISO)", fontsize=11, labelpad=10)
        ax.set_xticks(x)
        ax.set_xticklabels(sub['geoId'], fontsize=9, fontweight='bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#BDC3C7')
        ax.spines['bottom'].set_color('#BDC3C7')
        ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#BDC3C7')
        ax.set_facecolor('white')
        ax.legend(frameon=False, loc='upper right', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(os.path.join(plots_dir, f"q8_{indicator.lower().replace(' ', '_')}_comparison.png"), dpi=300)
        plt.close()


# ----------------- SECTION 3.2: ADVANCED QUESTIONS FOR GRADES A & B -----------------

def run_advanced_a():
    print("\n--- Solving Advanced Q1 (Question A): Lagged Vaccination vs. CFR ---")
    # We will study Germany (DE) as it has consistent case, death, and vaccination reporting
    de_cases = df_cases[df_cases['geoId'] == 'DE'].sort_values(by='date').copy()
    de_vacc = df_vacc_nat[(df_vacc_nat['ReportingCountry'] == 'DE') & (df_vacc_nat['TargetGroup'] == 'ALL')].copy()
    
    # Standardise ISO weeks in vaccination to dateRep
    # Let's aggregate cases and deaths by week to align with vaccination
    de_cases['year_week'] = de_cases['date'].dt.strftime('%Y-W%V') # ECDC week format
    # Note: %V is ISO week. ECDC's YearWeekISO matches '%G-W%V'
    de_cases['year_week_iso'] = de_cases['date'].dt.strftime('%G-W%V')
    
    cases_weekly = de_cases.groupby('year_week_iso').agg({'cases': 'sum', 'deaths': 'sum'}).reset_index()
    vacc_weekly = de_vacc.groupby('YearWeekISO').agg({'FirstDose': 'sum', 'SecondDose': 'sum'}).reset_index()
    
    # Merge on week
    weekly = pd.merge(cases_weekly, vacc_weekly, left_on='year_week_iso', right_on='YearWeekISO')
    weekly = weekly.sort_values(by='year_week_iso').reset_index(drop=True)
    
    # Cumulative vaccination
    weekly['Cum_FirstDose'] = weekly['FirstDose'].cumsum()
    weekly['Cum_SecondDose'] = weekly['SecondDose'].cumsum()
    de_pop = 83237124 # Germany pop
    weekly['FirstDose_Rate'] = weekly['Cum_FirstDose'] / de_pop
    weekly['SecondDose_Rate'] = weekly['Cum_SecondDose'] / de_pop
    
    # Calculate rolling Case Fatality Rate (CFR)
    # Since deaths lag cases by ~2-3 weeks, rolling CFR is rolling_deaths / rolling_cases
    weekly['rolling_cases'] = weekly['cases'].rolling(4, min_periods=1).sum()
    weekly['rolling_deaths'] = weekly['deaths'].rolling(4, min_periods=1).sum()
    weekly['CFR'] = (weekly['rolling_deaths'] / weekly['rolling_cases']) * 100
    weekly['CFR'] = weekly['CFR'].fillna(0)
    
    # Lagged correlation analysis
    lags = [0, 1, 2, 3, 4, 5, 6, 8]
    print("\nLagged Correlation between Cumulative Vaccination Coverage and CFR in Germany:")
    for lag in lags:
        # Shift CFR back to test if vaccination precedes CFR drop
        shifted_cfr = weekly['CFR'].shift(-lag)
        # Drop NaNs
        mask = weekly['SecondDose_Rate'].notna() & shifted_cfr.notna()
        if mask.sum() > 5:
            r, p = pearsonr(weekly.loc[mask, 'SecondDose_Rate'], shifted_cfr[mask])
            print(f"  - Lag {lag} Weeks: Correlation Coefficient (r) = {r:.4f}, p-value = {p:.4f}")
            
    weekly.to_csv(os.path.join(plots_dir, "adv_a_weekly_cfr_vaccination.csv"), index=False)
    
    # Visualisation
    fig, ax1 = plt.subplots(figsize=(11, 6))
    
    # Plot CFR on y1
    color = '#C62828'
    ax1.set_xlabel('ISO Week (Germany)', fontsize=11, labelpad=10)
    ax1.set_ylabel('Weekly Case Fatality Rate (CFR, %)', color=color, fontsize=11)
    line1 = ax1.plot(weekly['year_week_iso'], weekly['CFR'], color=color, linewidth=2, label='Rolling CFR (%)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.spines['top'].set_visible(False)
    ax1.yaxis.grid(True, linestyle='--', alpha=0.3, color='#BDC3C7')
    
    # Set xticks intervals
    ax1.set_xticks(weekly['year_week_iso'][::10])
    ax1.set_xticklabels(weekly['year_week_iso'][::10], rotation=45)
    
    # Plot Vaccination Rate on y2
    ax2 = ax1.twinx()  
    color = '#1E88E5'
    ax2.set_ylabel('Second Dose Vaccination Coverage (%)', color=color, fontsize=11)
    line2 = ax2.plot(weekly['year_week_iso'], weekly['SecondDose_Rate'] * 100, color=color, linewidth=2, linestyle='--', label='Vaccination Coverage (%)')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.spines['top'].set_visible(False)
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right', frameon=False)
    
    plt.title("Socio-Epidemiological Coupling: Case Fatality Rate vs. Vaccine Coverage (Germany)", fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "adv_q_cfr_vs_vaccination_lag.png"), dpi=300)
    plt.close()


def run_advanced_b():
    print("\n--- Solving Advanced Q2 (Question B): Clinical Severity Transitions ---")
    # Severity ratio = Daily ICU Occupancy / Daily Hospital Occupancy
    df_icu = df_hosp[df_hosp['indicator'] == 'Daily ICU occupancy'][['geoId', 'date', 'value']].rename(columns={'value': 'icu'})
    df_h = df_hosp[df_hosp['indicator'] == 'Daily hospital occupancy'][['geoId', 'date', 'value']].rename(columns={'value': 'hosp'})
    
    # Merge daily ICU and hospital occupancy
    df_sev = pd.merge(df_icu, df_h, on=['geoId', 'date'])
    df_sev['date_dt'] = pd.to_datetime(df_sev['date'])
    df_sev['year_str'] = df_sev['date_dt'].dt.year.astype(str)
    
    # Filter for 2020 and 2022
    df_sev_filtered = df_sev[df_sev['year_str'].isin(['2020', '2022'])].copy()
    
    # Calculate average daily severity ratio (ICU / Hosp) for each country and year
    # Prevent division by zero
    df_sev_filtered = df_sev_filtered[df_sev_filtered['hosp'] > 0]
    df_sev_filtered['severity_ratio'] = df_sev_filtered['icu'] / df_sev_filtered['hosp']
    
    country_sev = df_sev_filtered.groupby(['geoId', 'year_str'])['severity_ratio'].mean().unstack(fill_value=np.nan).dropna()
    
    print("\nClinical Severity Ratio: Average Daily ICU Occupancy / Daily Hospital Occupancy:")
    print(country_sev)
    country_sev.to_csv(os.path.join(plots_dir, "adv_b_severity_comparison.csv"))
    
    # Wilcoxon Signed-Rank Test (paired, non-parametric as N is small and ratios are bounded)
    stat, p_val = wilcoxon(country_sev['2020'], country_sev['2022'])
    print(f"\nWilcoxon Signed-Rank Test (Severity Ratio 2020 vs. 2022):")
    print(f"  - Test Statistic: {stat:.4f}")
    print(f"  - p-value: {p_val:.4f}")
    
    # Plotting paired profile plot (slope graph)
    fig, ax = plt.subplots(figsize=(8, 6.5))
    
    for country in country_sev.index:
        y2020 = country_sev.loc[country, '2020'] * 100 # Convert to percentage
        y2022 = country_sev.loc[country, '2022'] * 100
        
        # Color line based on decrease/increase
        color = '#2E7D32' if y2022 < y2020 else '#C62828'
        ax.plot(['2020 (Wild Type)', '2022 (Omicron)'], [y2020, y2022], marker='o', linewidth=2.0, color=color, alpha=0.7)
        ax.annotate(country, xy=('2020 (Wild Type)', y2020), xytext=(-15, 0), textcoords='offset points', ha='right', va='center', fontsize=8.5, weight='bold', color='#34495E')
        ax.annotate(f"{y2022:.1f}%", xy=('2022 (Omicron)', y2022), xytext=(8, 0), textcoords='offset points', ha='left', va='center', fontsize=8, color='#34495E')
        
    ax.set_title("Shift in Clinical ICU Intensity: 2020 vs. 2022", fontsize=13, fontweight='bold', color='#2C3E50', pad=15)
    ax.set_ylabel("ICU Share of Hospitalised Patients (%)", fontsize=11, labelpad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['bottom'].set_color('#BDC3C7')
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#BDC3C7')
    ax.set_facecolor('white')
    ax.set_xlim(-0.15, 1.15)
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "adv_q_severity_shift_wilcoxon.png"), dpi=300)
    plt.close()


def run_advanced_c():
    print("\n--- Solving Advanced Q3 (Question C): Geopolitical Vaccine Portfolios ---")
    # Brand portfolio proportions at national level (using ALL groups)
    country_brand_agg = df_vacc_nat[df_vacc_nat['TargetGroup'] == 'ALL'].groupby(['ReportingCountry', 'Vaccine'])['Total_Doses_Administered'].sum().unstack(fill_value=0)
    
    # Normalize rows to sum to 1.0 (shares)
    country_brand_shares = country_brand_agg.div(country_brand_agg.sum(axis=1), axis=0)
    
    # Dimensionality Reduction using PCA (to visualise multidimensional brand portfolios in 2D)
    from sklearn.decomposition import PCA
    from sklearn.cluster import KMeans
    
    pca = PCA(n_components=2)
    pca_res = pca.fit_transform(country_brand_shares)
    
    # Cluster countries using K-Means (K=3)
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(country_brand_shares)
    
    df_cluster = pd.DataFrame({
        'geoId': country_brand_shares.index,
        'PC1': pca_res[:, 0],
        'PC2': pca_res[:, 1],
        'Cluster': clusters
    })
    
    # Map PCA loading vectors
    loadings = pca.components_
    features = country_brand_shares.columns
    
    print("\nPCA Loading Vectors (PC1 and PC2 explain which vaccines drive country groupings):")
    for f, pc1, pc2 in zip(features, loadings[0], loadings[1]):
        if abs(pc1) > 0.1 or abs(pc2) > 0.1:
            print(f"  - {vaccine_names.get(f, f)} ({f}): PC1={pc1:.3f}, PC2={pc2:.3f}")
    country_brand_shares_reset = country_brand_shares.reset_index().rename(columns={'ReportingCountry': 'geoId'})
    df_cluster = pd.merge(df_cluster, country_brand_shares_reset, on='geoId')
    print("\nGeopolitical Clusters of Vaccine Portfolios:")
    for cluster_id in range(3):
        sub = df_cluster[df_cluster['Cluster'] == cluster_id]
        print(f"\nCluster {cluster_id + 1}: Countries: {sub['geoId'].tolist()}")
        # Calculate mean vaccine brand composition
        mean_composition = sub[features].mean()
        print("  Mean Composition:")
        for v, share in mean_composition.nlargest(3).items():
            print(f"    - {vaccine_names.get(v, v)}: {share*100:.1f}%")
            
    df_cluster.to_csv(os.path.join(plots_dir, "adv_c_vaccine_clusters.csv"), index=False)
    
    # Visualise PCA Projection & Clustering
    fig, ax = plt.subplots(figsize=(9.5, 7))
    colors = ['#2980B9', '#27AE60', '#C0392B']
    
    for cluster_id in range(3):
        sub = df_cluster[df_cluster['Cluster'] == cluster_id]
        ax.scatter(sub['PC1'], sub['PC2'], s=150, color=colors[cluster_id], label=f'Portfolio Cluster {cluster_id + 1}', alpha=0.85, edgecolors='#34495E', linewidths=1.0)
        
    for idx, row in df_cluster.iterrows():
        ax.annotate(row['geoId'], (row['PC1'], row['PC2']), textcoords="offset points", xytext=(0, 6), ha='center', fontsize=9, color='#2C3E50', weight='bold')
        
    # Draw loading arrows for top driving vaccines
    arrow_scale = 0.5
    for i, f in enumerate(features):
        pc1_val = loadings[0, i] * arrow_scale
        pc2_val = loadings[1, i] * arrow_scale
        if abs(pc1_val) > 0.15 or abs(pc2_val) > 0.15:
            ax.arrow(0, 0, pc1_val, pc2_val, head_width=0.015, color='#7F8C8D', alpha=0.5, linewidth=1.2)
            ax.text(pc1_val * 1.15, pc2_val * 1.15, f, color='#7F8C8D', fontsize=8.5, weight='bold', ha='center', va='center')
            
    ax.set_title("Geopolitical Grouping: PCA and K-Means Clustering of Vaccine Brand Portfolios", fontsize=13, fontweight='bold', color='#2C3E50', pad=15)
    ax.set_xlabel(f"Principal Component 1 (Explains {pca.explained_variance_ratio_[0]*100:.1f}% Variance)", fontsize=11, labelpad=10)
    ax.set_ylabel(f"Principal Component 2 (Explains {pca.explained_variance_ratio_[1]*100:.1f}% Variance)", fontsize=11, labelpad=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#BDC3C7')
    ax.spines['bottom'].set_color('#BDC3C7')
    ax.xaxis.grid(True, linestyle='--', alpha=0.2, color='#BDC3C7')
    ax.yaxis.grid(True, linestyle='--', alpha=0.2, color='#BDC3C7')
    ax.axhline(0, color='#BDC3C7', linestyle='-', linewidth=0.5)
    ax.axvline(0, color='#BDC3C7', linestyle='-', linewidth=0.5)
    ax.set_facecolor('white')
    ax.legend(frameon=False, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "adv_q_vaccine_pca_clusters.png"), dpi=300)
    plt.close()


# ----------------- MAIN EXECUTION LOOP -----------------
if __name__ == "__main__":
    print("\n" + "="*40)
    print("   RUNNING ECDC COVID-19 EDA BACKEND   ")
    print("="*40)
    
    run_q1()
    run_q2()
    top_3 = run_q3()
    run_q4(top_3)
    run_q5()
    run_q6()
    run_q7()
    run_q8()
    
    run_advanced_a()
    run_advanced_b()
    run_advanced_c()
    
    print("\n" + "="*40)
    print("      BACKEND ANALYSIS COMPLETED       ")
    print("="*40)
