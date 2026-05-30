# Comparative Epidemiological Study of COVID-19 Waves and Vaccine Portfolios (EU/EEA, 2020-2022)

**Author:** Bilal Abdul (abac23@student.bth.se)  
**Institution:** Blekinge Institute of Technology (BTH), Sweden  
**Project Type:** University Data Science Research Project (Intelligent Data Analysis)

---

## Introduction
This repository contains the end-to-end data engineering and statistical modeling pipeline for analyzing the COVID-19 pandemic across the 30 countries of the European Union (EU) and European Economic Area (EEA) from January 2020 through December 2022.

Using public health datasets curated by the European Centre for Disease Prevention and Control (ECDC), this project applies data preprocessing, statistical inference, and unsupervised learning to investigate spatio-temporal infection waves, vaccine brand allocations, clinical capacity burdens, and vaccine skepticism dynamics.

### Engineering and Analytical Highlights
* **Demographic Cohort Normalization**: Implemented a fallback algorithm to reconstruct child age distributions from inconsistent reporting metrics across national health registries.
* **Spatial Deduplication**: Filtered subnational (NUTS-2) regional entries to prevent double-counting of cases and deaths at the national scale.
* **Time-Lagged Correlation**: Computed time-lagged Pearson correlations to measure the delay between vaccine deployment and changes in Case Fatality Rate (CFR).
* **Clinical Severity Analysis**: Utilized Wilcoxon Signed-Rank tests to evaluate intensive care unit (ICU) occupancy transitions between the pre-vaccine and Omicron waves.
* **Unsupervised Learning**: Applied Principal Component Analysis (PCA) and K-Means clustering to identify groups of countries sharing similar vaccine procurement portfolios.

---

## Technical Stack
* **Language:** Python 3.10+
* **Data Processing:** pandas, numpy
* **Data Visualization:** matplotlib, seaborn (vector-grade static plots)
* **Statistical Modeling & Inference:** scipy (Pearson Correlation, Wilcoxon Signed-Rank)
* **Unsupervised Machine Learning:** scikit-learn (PCA, K-Means Clustering)
* **Report & Presentation:** LaTeX, PowerPoint

---

## Repository Architecture

```
covid19-epidemiology-portfolio/
├── .gitignore                          # Excludes local caches, virtual environments, and large files
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── run_analysis.py                     # Main data analysis and processing pipeline
├── generate_slides.py                  # PowerPoint presentation generation script
├── COVID19_Analysis_Pipeline.ipynb     # Interactive Jupyter Notebook with complete analysis
├── COVID19_Epidemiology_Report.pdf     # Pre-compiled academic research paper (LNCS format)
├── COVID19_Epidemiology_Presentation.pptx # Verified professional presentation slides
├── data/                               # Raw ECDC source datasets
└── plots/                              # Generated figures and aggregate CSV outputs
```

---

## Key Findings and Statistical Results

### 1. Vaccine Skepticism and Peak Clinical Burden
By defining a national Vaccine Skepticism Rate (1 - First Dose Coverage) and comparing it to peak weekly hospital admissions per 100,000 residents during the 2021 rollout, the Pearson correlation test yielded:
$$r = 0.5414 \quad (p = 0.0166)$$
This statistically significant, positive correlation confirms that countries with higher vaccine skepticism (such as Bulgaria and Romania) experienced substantially higher peak clinical loads than highly vaccinated countries (such as Ireland and Portugal).

### 2. Clinical Severity Transitions (2020 vs. 2022)
Using a paired Wilcoxon Signed-Rank Test to evaluate average daily ICU-to-Hospital occupancy ratios across EU/EEA countries:
$$W = 4.0 \quad (p = 0.0068)$$
Since $p < 0.01$, we reject the null hypothesis. The clinical severity ratio decreased highly significantly (for example, the Netherlands dropped from 33.9% in 2020 to 10.2% in 2022). This confirms that patients hospitalized during the 2022 Omicron wave required intensive care at a small fraction of the rate observed in the pre-vaccine 2020 wave.

### 3. Geopolitical Brand Portfolios (PCA & K-Means)
Projecting normalized brand shares onto a 2D PCA space partitioned the EU/EEA into three distinct geopolitical clusters (K=3):
* **Cluster 1 (Standard European Portfolio - 28 nations):** Integrated procurement dominated by Pfizer/BioNTech (60.3% mean share), Spikevax (13.4%), and AstraZeneca (12.2%).
* **Cluster 2 (Moderna Outlier - Liechtenstein [LI]):** Unique reliance on Spikevax as its primary brand (65.5% share).
* **Cluster 3 (Reporting Outlier - Germany [DE]):** Categorized all reported doses under the code `UNK` (Unknown Vaccine) in the ECDC database, highlighting major reporting disparities.

---

## Getting Started

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
All generated assets will be saved to the `plots/` folder.

### 3. View Research Paper and Presentation
* **Research Paper:** Open and review the full academic report: [COVID19_Epidemiology_Report.pdf](COVID19_Epidemiology_Report.pdf)
* **Presentation Slides:** Open the advanced presentation deck: [COVID19_Epidemiology_Presentation.pptx](COVID19_Epidemiology_Presentation.pptx)

### 4. Interactive Examination
To explore the analysis step-by-step through a pre-formatted Jupyter Notebook:
```bash
jupyter notebook COVID19_Analysis_Pipeline.ipynb
```
