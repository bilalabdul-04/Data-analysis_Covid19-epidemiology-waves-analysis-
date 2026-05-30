# Comparative Epidemiological Study of COVID-19 Waves & Vaccine Portfolios (EU/EEA, 2020–2022)

**Author:** Bilal Abdul (<abac23@student.bth.se>)  
**Institution:** Blekinge Institute of Technology (BTH), Sweden  
**Project Type:** University Data Science Research Project (Course: Intelligent Data Analysis)  

---

## 📊 Project Overview
This repository contains a comprehensive end-to-end data engineering and statistical modeling pipeline analyzing the COVID-19 pandemic across the 30 countries of the European Union (EU) and European Economic Area (EEA) from January 2020 through December 2022. 

Utilizing public health datasets curated by the **European Centre for Disease Prevention and Control (ECDC)**, this project applies advanced data preprocessing, statistical inference, and unsupervised learning to investigate spatio-temporal infection waves, vaccine brand allocations, clinical capacity burdens, and vaccine skepticism dynamics.

### Key Engineering & Analytical Highlights:
* **Dynamic Cohort Reconstruction**: Devised a demographic fallback algorithm to normalize inconsistent child age reporting across national health dashboards.
* **NUTS-2 Deduplication**: Implemented clean national-level filtering to eliminate subnational double-counting.
* **Socio-Epidemiological Modeling**: Built time-lagged Pearson correlation models to map therapeutic delay between vaccine rollout and mortality decline.
* **Paired Non-Parametric Inference**: Applied Wilcoxon Signed-Rank tests to prove clinical severity transitions across the EU.
* **Unsupervised Clustering**: Combined Principal Component Analysis (PCA) and $K$-Means clustering to map geopolitical brand portfolio structures.
* **Programmatic Slide Compilation**: Engineered a script using `python-pptx` to compile and format academic slides dynamically with embedded vector figures.

---

## 🛠️ Technical Stack
* **Language:** Python 3.10+
* **Data Processing & Manipulation:** `pandas`, `numpy`
* **Data Visualization:** `matplotlib`, `seaborn` (vector-grade static plots)
* **Statistical Modeling & Inference:** `scipy` (Pearson Correlation, Wilcoxon Signed-Rank)
* **Unsupervised Machine Learning:** `scikit-learn` (PCA, K-Means Clustering)
* **Report & Presentation:** Pre-compiled PDF Academic Report, High-End Professional Presentation Deck (.pptx)

---

## 📁 Repository Architecture
```
Assigment 2/
├── .gitignore                  # Keeps the repo clean of installers and local caches
├── README.md                   # Portfolio overview & instructions
├── requirements.txt            # PIP dependencies
├── run_analysis.py             # Main pipeline (cleans data, models statistics, generates plots)
├── generate_slides.py          # Programmatic slide deck compiler
├── COVID19_Analysis_Pipeline.ipynb     # Interactive Jupyter Notebook
├── COVID19_Epidemiology_Report.pdf     # Pre-compiled Academic Research Paper PDF (LNCS format)
├── COVID19_Epidemiology_Presentation.pptx # Original advanced and professional presentation slide deck
├── data/                       # ECDC source datasets
│   ├── 1.COVID-19_daily_number_of_new_cases_and_deaths.csv
│   ├── 2.COVID-19_vaccination.csv
│   └── 3.COVID-19_hospital_and_ICU_admission_rates.csv
├── plots/                      # Exported plots and aggregate CSV results
│   ├── q1_quarterly_cases_trends.png
│   ├── q2_spatial_bubble_map_2022.png
│   ├── ...
│   └── adv_q_vaccine_pca_clusters.png
└── scripts/                    # Archived utility and exploration scripts
    ├── calculate_skepticism.py
    └── ...
```

---

## 🔍 Core Findings & Statistical Results

### 1. Vaccine Skepticism vs. Peak Clinical Burden
By defining a national **Vaccine Skepticism Rate** ($1 - \text{First Dose Coverage}$) and comparing it to peak weekly hospital admissions per 100k during the 2021 rollout, the Pearson correlation test yielded:
$$r = 0.5414 \quad (p = 0.0166)$$
This statistically significant, positive correlation confirms that countries with higher vaccine skepticism (e.g., Bulgaria, Romania) experienced much higher peak clinical loads than highly vaccinated countries (e.g., Ireland, Portugal).

### 2. Clinical Severity Transitions (2020 vs. 2022)
Using a paired **Wilcoxon Signed-Rank Test** to evaluate average daily ICU-to-Hospital occupancy ratios across EU/EEA countries:
$$W = 4.0 \quad (p = 0.0068)$$
Since $p < 0.01$, we reject the null hypothesis. The clinical severity ratio decreased highly significantly (e.g., the Netherlands dropped from **33.9%** in 2020 to **10.2%** in 2022). This confirms that patients hospitalized during the 2022 Omicron wave required intensive care at a small fraction of the rate observed in the pre-vaccine 2020 wave.

### 3. Geopolitical Brand Portfolios (PCA & K-Means)
Projecting normalized brand shares onto a 2D PCA space partitioned the EU/EEA into three distinct geopolitical clusters ($K=3$):
* **Cluster 1 (Standard European Portfolio - 28 nations):** Integrated procurement dominated by Pfizer/BioNTech (**60.3%** mean share), Spikevax (**13.4%**), and AstraZeneca (**12.2%**).
* **Cluster 2 (Moderna Outlier - Liechtenstein [LI]):** Unique reliance on Spikevax as its primary brand (**65.5%** share).
* **Cluster 3 (Reporting Outlier - Germany [DE]):** Categorized all reported doses under the code `UNK` (Unknown Vaccine) in the ECDC database, highlighting major reporting disparities.

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install all dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run Data Analysis Pipeline
To clean the datasets, execute the statistical tests, export summary CSVs, and generate the figures, run:
```bash
python run_analysis.py
```
*All generated assets will be saved to the `plots/` folder.*

### 3. View Research Paper & Presentation
* **Research Paper:** Open and review the full academic-grade research paper: [COVID19_Epidemiology_Report.pdf](COVID19_Epidemiology_Report.pdf)
* **Presentation Slides:** Open the advanced, professionally styled presentation deck: [COVID19_Epidemiology_Presentation.pptx](COVID19_Epidemiology_Presentation.pptx)

### 4. Interactive Examination
To explore the analysis step-by-step through a pre-formatted Jupyter Notebook:
```bash
jupyter notebook COVID19_Analysis_Pipeline.ipynb
```
