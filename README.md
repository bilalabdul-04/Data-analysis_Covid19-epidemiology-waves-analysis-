# COVID-19 Epidemiological Analysis — EU/EEA (2020–2022)

**Author:** Bilal Abdul  
**Institution:** Blekinge Institute of Technology (BTH), Sweden  
**Field:** Intelligent Data Analysis, Public Health Informatics

---

## Overview

This project is a full end-to-end epidemiological data study of COVID-19 across the 30 EU/EEA member states, covering the period from January 2020 through December 2022. It was developed as part of university-level coursework in intelligent data analysis and combines rigorous data engineering with statistical inference and unsupervised machine learning.

The analysis draws exclusively from datasets published by the European Centre for Disease Prevention and Control (ECDC) and covers infection wave dynamics, vaccine procurement portfolios, demographic vaccination patterns, and clinical capacity changes over time.

All code is written in Python. Outputs are generated programmatically from source data to ensure full reproducibility.

---

## Research Questions Addressed

- How did COVID-19 infection waves progress across EU/EEA countries between 2020 and 2022?
- Which countries experienced the highest infection and death rates relative to their population?
- How were vaccine brands distributed across the EU/EEA, and which countries deviated from the regional norm?
- Did vaccine skepticism correlate with higher clinical burden during the 2021 rollout period?
- Did the clinical severity of hospitalized patients change significantly between the pre-vaccine 2020 wave and the 2022 Omicron wave?
- Can countries be grouped into meaningful geopolitical clusters based on their vaccine procurement choices?

---

## Methods

**Data Preprocessing**  
ECDC datasets contain inconsistencies in subnational (NUTS-2) reporting. National-level figures were extracted by filtering entries where the reporting region matches the reporting country, avoiding double-counting of regional rows. A demographic fallback algorithm was implemented to handle inconsistent child age bracket reporting across national registries.

**Statistical Inference**  
Pearson correlation was used to measure the linear relationship between vaccine skepticism rates and peak weekly hospital admissions. A paired Wilcoxon Signed-Rank test evaluated whether ICU-to-hospital occupancy ratios differed significantly between 2020 and 2022.

**Unsupervised Learning**  
Principal Component Analysis (PCA) was applied to normalized vaccine brand share vectors for each country. K-Means clustering (K=3) was then run on the PCA-reduced space to identify geopolitical groupings in vaccine procurement behaviour.

---

## Key Results

**Vaccine Skepticism and Clinical Burden**  
Pearson r = 0.5414, p = 0.0166. Countries with lower first-dose uptake, such as Bulgaria and Romania, saw substantially higher peak hospital admissions per 100,000 residents during the 2021 rollout compared to high-uptake countries like Ireland and Portugal.

**Clinical Severity — 2020 vs. 2022**  
Wilcoxon W = 4.0, p = 0.0068. The ratio of ICU occupancy to total hospital occupancy dropped significantly across EU/EEA countries between 2020 and the 2022 Omicron wave, confirming a meaningful reduction in per-patient clinical severity despite higher case volumes.

**Vaccine Portfolio Clusters**  
Three distinct procurement clusters emerged from PCA + K-Means:
- 28 countries followed a standard integrated portfolio dominated by Pfizer/BioNTech (60.3% mean share)
- Liechtenstein procured primarily Moderna (65.5% share), forming its own cluster
- Germany's entire reported dose volume was recorded under an unknown vaccine code in the ECDC database, placing it in a separate reporting-anomaly cluster

---

## Repository Structure

```
covid19-epidemiology-portfolio/
├── README.md                               — Project documentation (this file)
├── requirements.txt                        — Python package dependencies
├── run_analysis.py                         — Main analysis pipeline
├── COVID19_Analysis_Pipeline.ipynb         — Jupyter Notebook (interactive walkthrough)
├── COVID19_Epidemiology_Report.pdf         — Full academic research report (LNCS format)
├── COVID19_Epidemiology_Presentation.pptx  — Presentation slides
├── data/
│   ├── 1.COVID-19_daily_number_of_new_cases_and_deaths.csv
│   ├── 2.COVID-19_vaccination.csv
│   └── 3.COVID-19_hospital_and_ICU_admission_rates.csv
└── plots/                                  — All generated figures and output CSVs
```

---

## Running the Project

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the full analysis pipeline (generates all figures and CSVs into `plots/`):
```bash
python run_analysis.py
```

Open the interactive notebook:
```bash
jupyter notebook COVID19_Analysis_Pipeline.ipynb
```

---

## Technical Stack

- Python 3.10+
- pandas, numpy — data processing
- matplotlib, seaborn — visualization
- scipy — statistical testing (Pearson, Wilcoxon)
- scikit-learn — PCA, K-Means clustering

---

## Data Sources

All datasets were retrieved from the ECDC open data portal:
- Daily reported cases and deaths by country
- COVID-19 vaccination data by target group and vaccine brand
- Hospital and ICU admission rates by country
