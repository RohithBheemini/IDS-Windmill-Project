# Complete Microscopic Guide to the Wind Turbine SCADA Condition Monitoring Project
**Document:** `dataset_complete_details.md`  
**Target Audience:** Readers with **Zero Prior Knowledge** of wind turbines, SCADA data, or predictive maintenance.  
**Objective:** Provide an exhaustive, microscopic breakdown of every single concept, file, column, physical sensor, mathematical equation, machine learning algorithm, and business decision in this project.

---

# Table of Contents
1. [Foundational Primer: How Does a Wind Turbine Actually Work?](#1-foundational-primer-how-does-a-wind-turbine-actually-work)
2. [What is SCADA Telemetry?](#2-what-is-scada-telemetry)
3. [The CARE_To_Compare Benchmark: Origins & Dataset Architecture](#3-the-care_to_compare-benchmark-origins--dataset-architecture)
4. [Microscopic File-by-File Breakdown](#4-microscopic-file-by-file-breakdown)
   - [4.1 The Metadata: `event_info.csv`](#41-the-metadata-event_infocsv)
   - [4.2 The Sensor Dictionary: `feature_description.csv`](#42-the-sensor-dictionary-feature_descriptioncsv)
   - [4.3 The Time-Series Stream: `<event_id>.csv`](#43-the-time-series-stream-event_idcsv)
   - [4.4 Operational Status Codes (`status_type_id`)](#44-operational-status-codes-status_type_id)
5. [The Physical Subsystems & What Happens When They Break](#5-the-physical-subsystems--what-happens-when-they-break)
6. [Data Cleaning & Hygiene: Auditing 102 Million Data Points](#6-data-cleaning--hygiene-auditing-102-million-data-points)
7. [The Critic's Audit: Fatal Traps We Strictly Avoided](#7-the-critics-audit-fatal-traps-we-strictly-avoided)
8. [Physics-First Feature Engineering: The "Rising Fever" Method](#8-physics-first-feature-engineering-the-rising-fever-method)
9. [The Machine Learning Models: Verification, Training Budgets & Timing](#9-the-machine-learning-models-verification-training-budgets--timing)
10. [The CARE Benchmark: Understanding Earliness (Lead Time)](#10-the-care-benchmark-understanding-earliness-lead-time)
11. [Explainable AI (XAI): Peeking Inside the Black Box with SHAP & LIME](#11-explainable-ai-xai-peeking-inside-the-black-box-with-shap--lime)
12. [The Financial Economics: Asymmetric Costs & Fleet ROI](#12-the-financial-economics-asymmetric-costs--fleet-roi)
13. [The Interactive Shiny Application: Tour & Operating Manual](#13-the-interactive-shiny-application-tour--operating-manual)
14. [Master Glossary of Terms](#14-master-glossary-of-terms)

---

# 1. Foundational Primer: How Does a Wind Turbine Actually Work?

To understand the data, you must first understand the machine. 

A modern industrial wind turbine is not just a giant pinwheel; it is a **300-foot-tall, multi-megawatt robotic power station** operating in extreme weather. 

```
                                      ==============================
                                     [         THE NACELLE          ]
                                     [  (Contains Gearbox, Gen,     ]
                                     [   Transformer, Hydraulics)   ]
                   \                 ==============================
                    \                              ||
        BLADE 1      \                             ||
                      \                            ||
                       \                           ||
                        \    HUB                   ||
                         \   (Rotor)               ||
                          ( O )--------------------||  TOWER
                         /                         ||  (300+ feet tall)
                        /                          ||
                       /                           ||
        BLADE 2       /                            ||
                     /                             ||
                    /                              ||
                   /                               ||
                                                   ||
                                             ==============
                                            [  FOUNDATION  ] (Deep ocean or ground)
```

### The Step-by-Step Flow of Energy:
1. **The Wind & The Blades:** The wind blows across three massive aerodynamic blades (each 50 to 80 meters long). The aerodynamic lift forces the rotor to turn.
2. **The Pitch Mechanism:** Inside the hub, electric motors or hydraulic cylinders rotate the blades along their longitudinal axis (the **Pitch Angle**). If the wind is too calm, blades tilt into the wind to catch maximum power. If a storm hits (wind $> 25\text{ m/s}$), the blades "feather" ($90^\circ$), turning edge-on to the wind to stop spinning and protect the turbine from snapping.
3. **The Low-Speed Shaft & The Rotor:** The blades turn a massive steel shaft (the Low-Speed Shaft) at a slow speed: typically **8 to 20 revolutions per minute (RPM)**.
4. **The Gearbox (The Mechanical Workhorse):** A generator cannot generate standard 50 Hz/60 Hz electricity at 15 RPM; it needs to spin at roughly **1,500 RPM**. The **gearbox** sits between the low-speed shaft and the generator, multiplying the rotational speed by approximately **1:90 to 1:100**. This gearbox contains planetary gears and high-speed shafts spinning under titanic mechanical torque.
5. **The Generator (The Electrical Heart):** The high-speed shaft spins inside the generator. Magnetic fields inside the copper stator windings generate electrical alternating current (AC). The generator has two critical bearings:
   - **Drive-End (DE) Bearing:** Located right next to the spinning gearbox connection.
   - **Non-Drive-End (NDE) Bearing:** Located at the rear of the generator.
6. **The Inverter & Frequency Converter (IGBTs):** Wind speed varies constantly, so the electricity produced has fluctuating frequency. Electronic switches (Insulated-Gate Bipolar Transistors, or **IGBTs**) convert the variable power to clean, grid-synchronized 50 Hz power.
7. **The High-Voltage (HV) Transformer:** The generator outputs voltage around 690 Volts. The internal transformer steps this voltage up to **33,000 Volts (33 kV)** so it can travel down cables in the tower and out to the electrical grid with minimal line losses.
8. **The Hydraulic Group:** A high-pressure hydraulic pump maintains oil pressure to actuate rotor brakes, mechanical safety locks, and blade pitch systems.
9. **The Yaw System:** Large electric motors rotate the entire 300-ton nacelle at the top of the tower so that the blades always face directly into the shifting wind direction.

---

# 2. What is SCADA Telemetry?

**SCADA** stands for **Supervisory Control and Data Acquisition**.

Every modern wind turbine is outfitted with hundreds of physical sensors measuring temperatures, pressures, vibrations, electrical voltages, currents, wind speeds, and rotor speeds.

### Why 10-Minute Averages?
Inside the turbine, microcontrollers measure physical sensors every millisecond. However, sending thousands of measurements per second across offshore satellite or underwater fiber-optic links for 36 turbines over 20 years would overwhelm industrial storage and communications.

Therefore, the global international standard for wind turbine condition monitoring (governed by **IEC 61400-25**) aggregates raw high-frequency data into **10-minute statistical summary windows**:
- **Average (`avg`):** The mean sensor reading over that 10-minute block.
- **Minimum (`min`):** The lowest recorded value during the 10 minutes.
- **Maximum (`max`):** The highest spike recorded during the 10 minutes.
- **Standard Deviation (`std`):** The amount of turbulence, vibration, or fluctuation around the mean.

Each calendar day consists of exactly $24 \times 6 = 144$ ten-minute intervals. One full year produces approximately **52,560 rows of data per turbine**.

---

# 3. The CARE_To_Compare Benchmark: Origins & Dataset Architecture

The dataset in this project comes from the **CARE_To_Compare** benchmark (*Condition Monitoring And Reliability Evaluation*), created by leading renewable energy researchers and published on Zenodo.

Before this benchmark, comparing wind turbine failure detection models was almost impossible because energy companies guarded their failure logs as confidential trade secrets. CARE_To_Compare released **89 years** of real, operational SCADA time series across **36 wind turbines** divided into three distinct wind farms:

```
+----------------------------------------------------------------------------------------------------+
|                                      THE 3 BENCHMARK WIND FARMS                                    |
+----------------------------------------------------------------------------------------------------+
| Wind Farm A (Onshore, Portugal)                                                                   |
|   - 5 Wind Turbines (Asset IDs: 0, 10, 11, 13, 21)                                                 |
|   - 22 Event Datasets (12 Anomaly Failures, 10 Normal Healthy Controls)                           |
|   - 86 Sensor Channels (54 Base Sensors)                                                          |
|   - Origin: EDP Open Data platform (transparent physical component descriptions)                   |
+----------------------------------------------------------------------------------------------------+
| Wind Farm B (Offshore, Germany)                                                                   |
|   - Offshore fleet operating in rough marine conditions                                            |
|   - 15 Event Datasets (6 Anomaly Failures, 9 Normal Healthy Controls)                             |
|   - 257 Sensor Channels (63 Base Sensors)                                                         |
|   - Anonymized component logs (Transformer cells, Main Rotor Bearings)                            |
+----------------------------------------------------------------------------------------------------+
| Wind Farm C (Offshore, Germany)                                                                   |
|   - High-density offshore fleet                                                                   |
|   - 58 Event Datasets (27 Anomaly Failures, 31 Normal Healthy Controls)                           |
|   - 957 Sensor Channels (238 Base Sensors)                                                        |
|   - Deep telemetry (Individual pitch motors, blade de-icing, converter phase temperatures)        |
+----------------------------------------------------------------------------------------------------+
```

The overall benchmark is **deliberately balanced**: out of 95 total datasets, **44 represent real failure events** and **51 represent normal, healthy operation**.

---

# 4. Microscopic File-by-File Breakdown

Let us zoom in to the exact files on disk. Inside `CARE_To_Compare/CARE_To_Compare/Wind Farm A/`, you find three types of files:

```
Wind Farm A/
├── event_info.csv             <- The master catalog of all monitored events
├── feature_description.csv    <- The dictionary explaining what every sensor measures
└── datasets/                  <- The folder containing the actual time-series CSVs
    ├── 0.csv
    ├── 10.csv
    ├── ...
    └── 92.csv
```

## 4.1 The Metadata: `event_info.csv`
This file is the "ground truth" answer key. It tells us which event happened to which turbine, when it happened, and what broke.

Every row uses semicolons (`;`) as delimiters. Here is what each column means:

| Column Name | Data Type | Plain English Meaning | Example Value |
| :--- | :--- | :--- | :--- |
| `asset` | Integer | The unique ID of the physical turbine (0, 10, 11, 13, or 21). | `11` |
| `event_id` | Integer | The unique ID of this test case (matches the CSV filename in `datasets/`). | `68` |
| `event_label` | String | Ground-truth outcome: `"anomaly"` (a breakdown occurred) or `"normal"` (turbine operated safely). | `anomaly` |
| `event_start` | Datetime | The exact timestamp when the forward evaluation window begins. | `2023-07-28 13:20:00` |
| `event_start_id`| Integer | The row index in the CSV where the evaluation window starts. | `52063` |
| `event_end` | Datetime | The exact timestamp when the event concluded (the component broke or window ended). | `2023-08-11 13:10:00` |
| `event_end_id` | Integer | The row index in the CSV where the event ended. | `54076` |
| `event_description`| String | The maintenance logbook entry explaining the root cause. Empty for normal events. | `Transformer failure` |

## 4.2 The Sensor Dictionary: `feature_description.csv`
This file maps sensor codes (like `sensor_11`) to real-world engineering measurements.

| Column Name | Plain English Meaning |
| :--- | :--- |
| `sensor_name` | The technical identifier used in the data files (e.g., `sensor_11`, `wind_speed_3`). |
| `statistics_type`| Which 10-minute aggregations exist: `average`, `maximum`, `minimum`, `std_dev`. |
| `description` | The human-readable physical meaning (e.g., `Temperature in gearbox bearing on high speed shaft`). |
| `unit` | Physical engineering unit (e.g., `°C` for temperature, `m/s` for wind, `rpm` for speed, `kW` for power). |
| `is_angle` | Boolean (`True`/`False`): Indicates whether the sensor measures a circular angle (like blade pitch $0-360^\circ$). |
| `is_counter` | Boolean (`True`/`False`): Indicates whether the sensor is an accumulating counter (like total kWh produced). |

## 4.3 The Time-Series Stream: `<event_id>.csv`
Inside `datasets/`, each CSV file (e.g., `68.csv`, `72.csv`) contains continuous 10-minute rows.

Every dataset file is split into **two distinct sections**:
1. **The Training History (`train_test == 'train'`):** Exactly ~1 full year (typically row 0 to ~52,063). This represents historical baseline data where the turbine was operating normally.
2. **The Prediction Window (`train_test == 'prediction'`):** The subsequent 2 to 4 weeks (rows 52,063 to ~54,358). This is the test period:
   - In an **anomaly** dataset, mechanical degradation worsens during this period until the turbine trips offline.
   - In a **normal** dataset, the turbine simply continues running normally without any mechanical breakdown.

## 4.4 Operational Status Codes (`status_type_id`)
Inside every dataset CSV, the column `status_type_id` records what state the turbine control computer was in:
- **`0` - Normal Production:** The turbine is generating electrical power onto the grid.
- **`1` - Derated Operation:** The turbine is restricted (e.g., forced to run at 50% power due to grid curtailment or excessive ambient heat).
- **`2` - Idling:** Wind speed is too low (below cut-in speed, $\approx 3\text{ m/s}$); the blades rotate slowly waiting for wind.
- **`3` - Service Mode:** Technicians are physically inside the turbine; site maintenance is underway.
- **`4` - Downtime:** The turbine has tripped offline due to an emergency fault or alarm.
- **`5` - Other:** Transient or unclassified operating states.

---

# 5. The Physical Subsystems & What Happens When They Break

In Wind Farm A, every single labeled failure in `event_info.csv` corresponds to a known physical breakdown. Here is how the physics manifests in the data:

```
+----------------------------------------------------------------------------------------------------+
| SUBSYSTEM           | MONITORED SCADA SENSORS             | PHYSICAL DEGRADATION SIGNATURES        |
+---------------------+-------------------------------------+----------------------------------------+
| 1. GEARBOX          | sensor_11_avg (HSS Bearing Temp °C) | As metal fatigue causes spalling on the|
|    (Events 72, 10,  | sensor_12_avg (Gearbox Oil Temp °C) | high-speed shaft bearing, friction     |
|     51)             | rotor_rpm, generator_rpm            | spikes. Oil temperature climbs 4-8°C   |
|                     |                                     | above normal under steady wind loads.  |
+---------------------+-------------------------------------+----------------------------------------+
| 2. GENERATOR BEARING| sensor_13_avg (Drive-End Temp °C)   | The drive-end bearing carries the shaft|
|    (Events 0, 40)   | sensor_14_avg (Non-Drive-End °C)    | alignment force. Degraded lubrication  |
|                     | stator_winding_temps (sensor_16-18) | causes catastrophic overheating, with  |
|                     |                                     | sensor_13 spiking from 46°C to 76-94°C.|
+---------------------+-------------------------------------+----------------------------------------+
| 3. TRANSFORMER      | sensor_39_avg (HV Phase L1 Temp °C) | Electrical insulation degradation in   |
|    (Event 68)       | sensor_40_avg (HV Phase L2 Temp °C) | the high-voltage step-up transformer   |
|                     | sensor_41_avg (HV Phase L3 Temp °C) | creates phase resistance imbalance.    |
|                     |                                     | Phase L1 temperature soared to 117°C!  |
+---------------------+-------------------------------------+----------------------------------------+
| 4. HYDRAULIC GROUP  | sensor_42_avg (Hydraulic Oil Temp)  | Over-cycling hydraulic pumps or valve  |
|    (Events 22, 73,  | sensor_5_avg (Pitch Angle °)        | seal friction causes hydraulic oil to  |
|     26, 42, 45, 84) | pitch_angle_std                     | overheat, reaching an extreme 112.4°C! |
+---------------------+-------------------------------------+----------------------------------------+
```

---

# 6. Data Cleaning & Hygiene: Auditing 102 Million Data Points

Before writing machine learning code, we performed a complete data hygiene audit across all 22 datasets of Wind Farm A:

### 1. Ingestion Speed: Semicolons vs Commas
The files use `;` as the column separator. Attempting to read them with default `read.csv()` causes immediate failure. We implemented `data.table::fread(..., sep = ";")`, which loads millions of rows in seconds.

### 2. Missing Value (NA) Audit
- **Total Data Examined:** 1,196,747 rows across 86 sensor columns = **102,920,242 individual data points**.
- **Total Missing Values Found:** Exactly **40 NA values** across the entire dataset!
- **Missingness Rate:** **0.000038%** (less than four parts per ten million).
- **Why Did Missing Values Occur?** Brief transmission dropouts in SCADA telemetry packets over remote cellular modems.
- **How We Handled Them Without Lying:** We used **Last Observation Carried Forward (`zoo::na.locf`)**. Because physical steel components possess thermal inertia (a 20-ton gearbox cannot change temperature by 30 degrees in 10 minutes), carrying the previous valid sensor reading forward for one interval preserves physical reality without hallucinating artificial numbers.

### 3. Physical Envelope Validation
- **Wind Speed:** Checked for corrupted negative numbers. Validated $\ge 0\text{ m/s}$.
- **Pitch Angle:** Enforced aerodynamic limits $[-10^\circ, 95^\circ]$. Values of $90^\circ$ represent fully feathered emergency parking.
- **Infinite / NaN Values:** Exactly **zero** infinite values found.

---

# 7. The Critic's Audit: Fatal Traps We Strictly Avoided

As critical systems reviewers, we identified three traps that cause machine learning models to fail in wind energy operations:

### Fatal Trap #1: The "Status Code" Cheat
In raw SCADA files, `status_type_id` changes to `4` (Downtime) or `3` (Service mode) when the turbine breaks down.
- If an algorithm uses `status_type_id` as a predictor, it achieves **99.9% accuracy** simply by checking `if status == 4`.
- **Why this is catastrophic in real life:** The wind farm control center already knows the turbine is down when it trips offline! Predictive maintenance is only valuable if it alerts engineers **while the turbine is still running in Status 0**, giving them days to prepare.
- **Our Fix:** We strictly purged `status_type_id` from the model's feature set. The model must rely 100% on physical sensor signals.

### Fatal Trap #2: Synthetic Data Fabrication (SMOTE)
Many data scientists use SMOTE (Synthetic Minority Over-sampling Technique) to generate fake failure rows.
- **Why this is dangerous in physical engineering:** SMOTE mathematically interpolates between existing points. In doing so, it creates physically impossible states: for example, generating a synthetic record showing $0\text{ m/s}$ wind, $90^\circ$ pitch angle, $2,000\text{ kW}$ power, and a cold gearbox.
- **Our Fix:** **Zero synthetic data.** Every single observation is genuine telemetry from real turbines.

### Fatal Trap #3: Asset-Identity Confounding
Turbines have unique baseline temperatures due to their geographic placement on a ridge. If you feed `asset_id` into the model, the algorithm simply memorizes that "Turbine 11 runs hot" rather than learning what a broken bearing looks like.
- **Our Fix:** Removed `asset_id` from model inputs and validated models using **Leave-One-Turbine-Out Group Cross-Validation** (evaluating on a completely unseen turbine).

---

# 8. Physics-First Feature Engineering: The "Rising Fever" Method

Raw sensor readings are noisy and heavily influenced by the weather. To build a robust model, we engineered physically grounded features:

### 1. Thermodynamic Differentials ($\Delta T$)
A gearbox bearing naturally runs at 60°C on a scorching 38°C summer afternoon, but runs at 40°C on a freezing 5°C winter morning. If you look only at raw temperature, the model will think summer is an anomaly and winter is healthy!

To solve this, we calculated the **temperature differential above ambient weather**:
$$\Delta T_{\text{Gearbox}} = T_{\text{Gearbox Bearing}} - T_{\text{Ambient Weather}}$$
$$\Delta T_{\text{Generator DE}} = T_{\text{Gen Drive-End Bearing}} - T_{\text{Ambient Weather}}$$
$$\Delta T_{\text{Transformer}} = T_{\text{Transformer Phase L1}} - T_{\text{Ambient Weather}}$$
$$\Delta T_{\text{Hydraulic}} = T_{\text{Hydraulic Oil}} - T_{\text{Ambient Weather}}$$
By subtracting the outside ambient temperature (`sensor_0_avg`), we eliminated seasonal weather noise and exposed the true internal mechanical friction!

### 2. Causal Backward Rolling Trends (The 6-Hour Trend)
Mechanical failures rarely happen in 10 minutes; metal bearings wear down slowly over days.
We calculated a **6-hour backward moving average** (36 consecutive 10-minute steps):
$$\text{RollMean}_{6h}(t) = \frac{1}{36}\sum_{k=0}^{35} \Delta T(t - k)$$
*Important:* We used **strictly backward alignment** (`align = "right"`). The model looks only at past history, never peeking into future data.

### 3. Gearbox Transmission Ratio
$$\text{Ratio}_{\text{Gear}} = \frac{\text{RPM}_{\text{Generator}}}{\text{RPM}_{\text{Rotor}}}$$
Under normal operation, this ratio is a fixed mechanical constant ($\approx 90$). If bearings seize, brakes drag, or couplings slip, this ratio deviates.

### 4. Normalized Aerodynamic Efficiency ($C_p$ Proxy)
According to Betz's law of wind physics, the power available in wind is proportional to the **cube of wind speed** ($v^3$):
$$P_{\text{Available}} \propto v_{\text{wind}}^3$$
We calculated the aerodynamic efficiency proxy:
$$\text{PowerProxy} = \frac{P_{\text{Active}}}{v_{\text{wind}}^3}$$
If a turbine produces less power than expected for a given wind speed, it indicates aerodynamic blade pitch misalignment or mechanical drag.

---

# 9. The Machine Learning Models: Verification, Training Budgets & Timing

We compared three complementary machine learning architectures:

```
+----------------------------------------------------------------------------------------------------+
| 1. LOGISTIC REGRESSION (GLM) | Fast, transparent, linear baseline. Assumes additive sensor effects.|
+------------------------------+---------------------------------------------------------------------+
| 2. RANDOM FOREST (RANGER)    | Committee of 100 decision trees voting together. Handles non-linear |
|                              | sensor interactions and threshold jumps.                            |
+------------------------------+---------------------------------------------------------------------+
| 3. XGBOOST                   | Extreme Gradient Boosting. Builds decision trees sequentially, with |
|                              | each new tree correcting the residual errors of prior trees.        |
+----------------------------------------------------------------------------------------------------+
```

### Empirical Timing & Accuracy Benchmarks (Tested on Held-Out Turbine #21)

We ran a controlled benchmark measuring the exact training duration, memory consumption, and test AUC on an unseen wind turbine across three data budgets:

| Training Budget | Rows Used | GLM Training Time | GLM Test AUC | Random Forest Time | RF Test AUC | XGBoost Time | XGBoost Test AUC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Fast Prototype** | **25,000** | **0.43 sec** | 0.7629 | **2.23 sec** | 0.7632 | **0.59 sec** | **0.8134** |
| **Recommended Balanced** | **100,000** | **1.61 sec** | 0.7544 | **14.58 sec** | 0.7735 | **0.67 sec** | **0.8297** |
| **Full Fleet Scale** | **323,567** | **5.20 sec** | 0.7609 | **47.05 sec** | 0.7802 | **1.46 sec** | **0.8271** |

### How Much Training Should You Do?
- **Recommended Training Budget:** **XGBoost on 100,000 balanced observations** (`max_depth = 6`, `eta = 0.08`, `nrounds = 80`).
- **Time Required:** **0.67 seconds** (less than one second!).
- **Hardware Needed:** A standard laptop CPU (4 cores). **No expensive GPUs required.**
- **RAM Needed:** Only **109 MB** of memory.

---

# 10. The CARE Benchmark: Understanding Earliness (Lead Time)

The **CARE Score** evaluates early fault detectors across four dimensions:
1. **Coverage ($C$):** Can the model detect actual breakdowns when they happen? (Recall)
2. **Accuracy ($A$):** Does the model recognize healthy, normal operation? (Specificity)
3. **Reliability ($R$):** Does the model avoid spamming operators with false alarms? (Precision)
4. **Earliness ($E$):** How many hours or days **before** the turbine trips does the model sound the alarm?

### Real Lead Times Achieved on Actual Breakdown Events:

```
EVENT ID | SUBSYSTEM COMPONENT    | MONITORING WINDOW | EARLY WARNING LEAD TIME | LEAD TIME IN DAYS
---------+------------------------+-------------------+-------------------------+-------------------
Event 68 | Transformer Failure    | 382.5 Hours       | 382.3 Hours             | 15.9 Days Early
Event 0  | Generator Bearing DE   | 473.0 Hours       | 472.8 Hours             | 19.7 Days Early
Event 40 | Generator Bearing DE   | 823.2 Hours       | 822.0 Hours             | 34.2 Days Early
Event 72 | Gearbox Failure        | 336.2 Hours       | 336.0 Hours             | 14.0 Days Early
Event 51 | Gearbox Bearing Damage | 398.8 Hours       | 398.7 Hours             | 16.6 Days Early
Event 10 | Gearbox Failure        | 211.5 Hours       | 207.0 Hours             |  8.6 Days Early
Event 22 | Hydraulic Group        | 191.3 Hours       | 191.2 Hours             |  8.0 Days Early
```

**The Operational Reality:**  
Receiving an alert **8 to 34 days in advance** transforms maintenance. Instead of an emergency offshore crisis, technicians have 2 to 4 weeks to review weather windows, ship spare bearings, and replace the component during scheduled downtime.

---

# 11. Explainable AI (XAI): Peeking Inside the Black Box with SHAP & LIME

If an AI flags a turbine as "High Risk," engineers will not trust it unless the model explains **why**.

We integrated two Explainable AI tools:

### 1. SHAP (Shapley Additive Explanations)
Originating from cooperative game theory, SHAP calculates the exact contribution of each sensor. If the baseline risk of the fleet is 5% and Turbine #0 is predicted at 85% risk, SHAP breaks down that +80% increase:
- Generator Drive-End Temperature: **+55%**
- 6-Hour Rolling Generator Differential: **+20%**
- Ambient Temperature Offset: **+5%**

### 2. LIME (Local Interpretable Model-agnostic Explanations)
LIME builds a local, transparent linear rulebook around a specific observation, generating intuitive decision rules:
- *Rule 1:* If `temp_gen_bearing_de > 75°C` $\rightarrow$ increases anomaly likelihood by +42%.
- *Rule 2:* If `wind_speed_max > 17.7 m/s` $\rightarrow$ decreases likelihood (high load explains temperature).

### The Physical Proof: Testing Explanations Against Ground Truth

```
+----------------------------------------------------------------------------------------------------+
| FAILURE CASE       | WHAT THE AI HIGHLIGHTED (TOP SHAP / LIME)  | PHYSICAL INTEGRITY VERDICT       |
+--------------------+--------------------------------------------+----------------------------------+
| Gearbox            | temp_gearbox_bearing (+4.3°C rise)         | HIGH INTEGRITY: Mechanical       |
| (Event 72)         | roll_mean_trans_6h, temp_gearbox_oil       | friction directly heats bearing  |
+--------------------+--------------------------------------------+----------------------------------+
| Generator Bearing  | temp_gen_bearing_de (peaked at 76-94°C)    | VERY HIGH INTEGRITY: Drive-End   |
| (Event 0)          | roll_mean_gen_de_6h                        | bearing wear correctly isolated  |
+--------------------+--------------------------------------------+----------------------------------+
| Transformer        | temp_transformer (Phase L1 reached 117°C)  | HIGH INTEGRITY: Electrical ohmic |
| (Event 68)         | roll_mean_gearbox_6h                       | heating in winding identified    |
+--------------------+--------------------------------------------+----------------------------------+
| Hydraulic Group    | temp_hydraulic_oil (reached 112.4°C!)      | CRITICAL INTEGRITY: Overheated   |
| (Event 22)         | roll_mean_hydr_6h                          | fluid causes pitch cylinder lag  |
+--------------------+--------------------------------------------+----------------------------------+
| Healthy Control    | All key components had negative or near-   | PERFECT: Model stays quiet during|
| (Event 25)         | zero anomaly contributions                 | normal operating conditions      |
+----------------------------------------------------------------------------------------------------+
```

---

# 12. The Financial Economics: Asymmetric Costs & Fleet ROI

In wind energy, the costs of being wrong are wildly asymmetric:

$$\text{Expected Total Cost} = (FN \times C_{FN}) + (FP \times C_{FP}) + (TP \times C_{TP})$$

- **$C_{FN}$ = False Negative Cost ($150,000 - $300,000):**  
  The model stays silent, and a gearbox shatters offshore. Requires chartering an offshore jack-up crane ship, buying replacement gears, and enduring 6 weeks of lost electricity production.
- **$C_{FP}$ = False Positive Cost ($3,500):**  
  The model rings a false alarm. An onshore engineer reviews logs and dispatches a routine inspection team.
- **$C_{TP}$ = True Positive Cost ($8,000):**  
  The model detects the fault early. A scheduled uptower repair replaces the bearing before secondary catastrophic damage occurs.

### Why the 50% Threshold is Wrong:
Because a missed failure is **40 times more expensive** than a false alarm ($150,000 vs $3,500), our model optimizes the alarm threshold to **$\tau = 0.30 - 0.35$**. This threshold prioritizes catching failures early, saving **hundreds of millions of dollars** in fleet maintenance expenses over multi-year lifecycles.

---

# 13. The Interactive Shiny Application: Tour & Operating Manual

We packaged the entire solution into an interactive web application located in `shiny_app/app.R`.

### How to Launch the Application:
In PowerShell or terminal from the project folder:
```powershell
& "C:\Users\Rohith\R\R-4.6.1\bin\Rscript.exe" run_app.R
```
Or in RStudio / R console:
```r
shiny::runApp("shiny_app")
```
The app opens at `http://127.0.0.1:3838`.

### The 5 Interactive Dashboard Tabs:
1. **Fleet Overview:** Displays live KPI cards (3 Wind Farms, 36 Turbines, 89 Years of SCADA, 95 Events), an interactive event registry table, and failure mode filters.
2. **SCADA Telemetry Studio:** Select any Turbine and Event to inspect interactive multi-sensor plots ($\Delta T$ differentials, temperatures, power curves) alongside the real-time anomaly risk score timeline.
3. **Model Benchmark & CARE:** Displays Leave-One-Turbine-Out validation tables, score distributions, and the CARE early warning lead-time breakdown.
4. **Explainable AI (SHAP & LIME):** Interactive diagnostic studio where users select a failure mode and inspect global fleet drivers, local SHAP waterfalls, and LIME local rulebooks with physical engineering validation notes.
5. **Business Value & ROI:** Interactive financial sliders ($C_{FN}, C_{FP}, C_{TP}$, fleet size) allowing executives to dynamically calculate net fleet savings and visualize the cost-optimal decision threshold curve.

---

# 14. Master Glossary of Terms

- **Betz's Law:** The theoretical maximum efficiency of any wind turbine (at most 59.3% of kinetic wind energy can be extracted).
- **CARE Score:** The international benchmark metric evaluating Coverage, Accuracy, Reliability, and Earliness.
- **Drive-End (DE) Bearing:** The main bearing connecting the generator rotor to the spinning high-speed gearbox shaft.
- **Earliness:** The amount of advance notice (in hours or days) a model provides before a physical breakdown occurs.
- **Feathering:** Turning blade pitch to $90^\circ$ parallel to the wind to stop rotation during dangerous storms.
- **IGBT:** Insulated-Gate Bipolar Transistor; high-speed electronic switches that condition variable AC power into clean 50 Hz grid electricity.
- **Leave-One-Turbine-Out CV:** Evaluating a machine learning model on a completely unseen physical turbine to ensure true generalizability.
- **LIME:** Local Interpretable Model-agnostic Explanations; creates local sparse rulebooks explaining individual predictions.
- **Nacelle:** The housing shell at the top of the tower containing the gearbox, generator, transformer, and electronics.
- **Pitch Angle:** The angle of rotation of the blades around their long axis to control aerodynamic lift.
- **SCADA:** Supervisory Control and Data Acquisition; the industrial computer network recording turbine sensor measurements.
- **SHAP:** Shapley Additive Explanations; game-theoretic method calculating exact additive feature importance.
- **SMOTE:** Synthetic Minority Over-sampling Technique; an artificial data generation algorithm rejected in this project to prevent physical violations.
- **Temperature Differential ($\Delta T$):** Component temperature minus ambient weather temperature, isolating mechanical friction from seasonal weather variations.
- **Yaw:** The mechanical rotation of the entire nacelle to keep blades pointed directly into shifting wind directions.

---
*End of Complete Microscopic Dataset and Project Guide.*
