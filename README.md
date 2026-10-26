# Wind Turbine SCADA Condition Monitoring & Predictive Anomaly Detection
### Industrial Benchmark (CARE_To_Compare), Explainable AI (SHAP & LIME), and Decision Support Platform

[![R](https://img.shields.io/badge/Language-R%204.6.1-blue.svg)](https://www.r-project.org/)
[![Shiny](https://img.shields.io/badge/App-Shiny%20Dashboard-green.svg)](https://shiny.posit.co/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

An end-to-end industrial data science project for predictive condition monitoring and early fault detection in wind turbines, based on the **CARE_To_Compare** benchmark (89 years of SCADA time series across 36 wind turbines from EDP Open Data in Portugal and offshore wind farms in Germany).

---

## 🌟 Key Features

1. **Zero Artificial Values (Physics-First):**
   * Strictly avoids synthetic oversampling (no SMOTE) to prevent fabricating physically impossible thermodynamic states.
   * Purges post-trip operational status codes (`status_type_id == 3/4`) to eliminate look-ahead leakage and ensure genuine early detection.
2. **Physics-Grounded Feature Engineering:**
   * Thermodynamic Temperature Differentials ($\Delta T = T_{\text{component}} - T_{\text{ambient}}$) to remove seasonal weather bias.
   * Causal 6-hour backward moving averages to capture creeping thermal drift without future data leakage.
   * Electromechanical transmission ratio ($RPM_{\text{gen}} / RPM_{\text{rotor}}$) and Betz aerodynamic power proxies ($P / v^3$).
3. **Leave-One-Turbine-Out Group Cross-Validation:**
   * Models evaluated on strictly held-out unseen physical turbines (Group K-Fold by Asset ID) to prove generalizability.
4. **CARE Earliness Metric:**
   * Provides **8.0 to 34.2 days of lead time** before emergency shutdown across gearboxes, generator bearings, transformers, and hydraulic systems.
5. **Explainable AI (SHAP & LIME):**
   * Exact TreeSHAP attributions and LIME local surrogate rules verify that the model flags genuine physical components (e.g. gearbox bearing heat for gearbox failure, Drive-End bearing temperature for generator failure).
6. **Production Shiny Web Application:**
   * Real-time SCADA telemetry studio, model benchmarking tables, interactive SHAP/LIME explorer, and dynamic financial ROI calculator.

---

## 🚀 Quick Start

### Run the Master Script (`main.R`)
The entire project is controlled by a single master script, `main.R`.

```bash
# 1. Run live condition monitoring demo and launch the Shiny dashboard
Rscript main.R

# 2. Directly launch the interactive Shiny web dashboard (http://127.0.0.1:3838)
Rscript main.R --app

# 3. Run the standalone condition monitoring and XAI demo in terminal
Rscript main.R --demo

# 4. Optional: Retrain models or re-run the full data cleaning pipeline
Rscript main.R --train
Rscript main.R --clean
Rscript main.R --pipeline
```

### View the Humanized Case-Study Report & Presentation
* Open [`wind_turbine_ids_report.html`](wind_turbine_ids_report.html) in any browser for the complete interactive case study.
* Open [`presentation_wind_turbine_ids.pptx`](presentation_wind_turbine_ids.pptx) for the executive presentation slides (with speaker notes in [`presentation_slides.md`](presentation_slides.md)).

---

## 📁 Repository Structure

```
IDS-Windmill-Project/
├── main.R                          # Master project script (Pipeline, Demo, & Shiny Launcher)
├── shiny_app/
│   └── app.R                       # Complete Shiny dashboard application (bslib Darkly theme)
├── dataset_complete_details.md     # Exhaustive microscopic reference manual (for zero-knowledge readers)
├── presentation_wind_turbine_ids.pptx # Executive 10-slide minimalist presentation
├── presentation_slides.md          # Speaker notes and slide script
├── wind_turbine_ids_report.Rmd     # Humanized case-study report source
├── wind_turbine_ids_report.html    # Compiled interactive HTML case study
├── data_clean/
│   ├── clean_telemetry.rds         # Cleaned, physically verified SCADA telemetry
│   ├── clean_events.rds            # Pre-event feature summaries across monitored events
│   └── clean_events.csv            # Clean event catalog in CSV format
├── models/
│   ├── xgb_model.rds               # Production Extreme Gradient Boosting model
│   ├── rf_model.rds                # Production Random Forest (ranger) model
│   ├── glm_model.rds               # Production Logistic Regression (GLM) baseline
│   ├── benchmark_results.rds       # Cross-validation performance metrics
│   ├── care_earliness.rds          # Lead time (hours/days) before shutdown per event
│   ├── xai_global_shap.rds         # Global fleet-wide SHAP feature rankings
│   ├── xai_local_shap.rds          # Local SHAP attributions by failure mode
│   └── xai_lime_results.rds        # Local LIME surrogate rulebook and weights
└── .gitignore                      # Excludes raw multi-gigabyte archives (CARE_To_Compare)
```

---

## 📊 Benchmark Results

### A. Model Cross-Validation (Held-Out Unseen Turbine)
| Model Architecture | Training Time (100k rows) | Test ROC-AUC | Recall | Specificity | Precision | F1-Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (GLM)** | 1.61 sec | 0.7544 | 14.20% | 90.45% | 28.34% | 0.1892 |
| **Random Forest (`ranger`)** | 14.58 sec | 0.7735 | 9.99% | **95.33%** | 36.24% | 0.1566 |
| **XGBoost (`xgboost`)** | **0.67 sec** | **0.8297** | **15.69%** | 93.22% | **38.10%** | **0.2222** |

### B. CARE Earliness: Lead Time Before Catastrophic Breakdown
* **Gearbox Failures:** **14.0 to 16.6 days** in advance
* **Generator Bearing Failures:** **19.7 to 34.2 days** in advance
* **Transformer Failures:** **15.9 days** in advance
* **Hydraulic Group Failures:** **8.0 days** in advance

---

## 🛠️ Required R Packages

```r
install.packages(c(
  "data.table", "zoo", "ranger", "xgboost", "pROC",
  "lime", "shiny", "bslib", "bsicons", "DT",
  "ggplot2", "scales", "rmarkdown", "knitr"
))
```

---
*Developed under industrial wind turbine condition monitoring protocols.*
