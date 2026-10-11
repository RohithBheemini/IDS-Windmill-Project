# Wind Turbine SCADA Condition Monitoring & Anomaly Detection
## Presentation Slide Deck & Speaker Notes
**File:** `presentation_wind_turbine_ids.pptx`  
**Layout:** 16:9 Widescreen | Minimalist Modern Design | Large High-Readability Typography  

---

### Slide 1: Title Slide
* **Category:** WIND TURBINE CONDITION MONITORING
* **Title:** Saving Millions in the Wind
* **Subtitle:** How Physics, Machine Learning & Explainable AI Spot Failures Weeks in Advance
* **Footer:** A Simplified Case Study: Foundations, Realized Approaches & Alternative Paths
* **Speaker Cue:** "Good morning/afternoon. Today I am going to share a case study on wind turbine predictive maintenance. We will look at how we took real sensor data from offshore turbines, rejected common machine learning shortcuts, used basic physics to spot breakdowns weeks before they happen, and proved that everything makes mechanical sense using Explainable AI."

---

### Slide 2: The Real-World Problem (Operational Reality)
* **Header:** Operational Reality — The High Stakes of Wind Turbine Breakdowns
* **Subtitle:** Why traditional reactive maintenance fails catastrophically at sea
* **Card 1: The Machine:**
  - Turbines are 300-ft tall robotic power plants with 80-meter blades.
  - Internal components operate under titanic mechanical torque & cyclic stress.
  - A 20-ton gearbox steps up rotor speed from 15 RPM to 1,500 RPM for the generator.
* **Card 2: The Catastrophe:**
  - Offshore crane ships cost \$30,000+ per day just to mobilize.
  - Replacing shattered gearboxes costs \$150,000 to \$250,000+ in parts.
  - Rough winter seas can delay repairs for 6 to 8 weeks, losing hundreds of thousands in green power.
* **Card 3: The Goal:**
  - Spot component degradation 2 to 4 weeks before catastrophic failure.
  - Use existing SCADA temperature and speed sensors without new hardware.
  - Avoid false alarm fatigue so technicians genuinely trust the alerts.
* **Speaker Cue:** "Imagine a wind turbine standing out at sea. When a 20-ton gearbox breaks, it's not like calling a tow truck. A specialized crane ship costs \$30,000 a day just to leave port. If high waves hit, the turbine sits broken for two months. Our mission was simple: can we spot the failure 2 to 4 weeks early using the sensors already on the turbine, without drowning technicians in false alarms?"

---

### Slide 3: Dataset Anatomy (What Data We Had)
* **Header:** Dataset Anatomy — Understanding the Benchmark (CARE_To_Compare)
* **Subtitle:** 89 years of real-world operational SCADA telemetry across 36 wind turbines
* **Left Card: The Multi-Farm Architecture:**
  - **Wind Farm A (Portugal, Onshore):** 5 turbines, 22 datasets, 86 sensor channels. Transparent component breakdown from EDP Open Data.
  - **Wind Farm B (Germany, Offshore):** 15 datasets, 257 sensor channels. Severe marine environment, rotor bearing & transformer cell issues.
  - **Wind Farm C (Germany, Offshore):** 58 datasets, 957 sensor channels. Deep telemetry (pitch motors, converter IGBTs, blade heaters).
  - **10-Minute Averaging (IEC 61400-25):** Raw milliseconds are aggregated into 10-minute average, min, max, and std deviation.
* **Right Card: Structure of Each Monitored Event:**
  - **Historical Baseline (train):** Exactly 1 full year (~52,000 observations) of normal healthy historical operation for that specific turbine.
  - **Evaluation Window (prediction):** The subsequent 2 to 4 weeks. In anomaly datasets, degradation worsens leading to failure; in normal datasets, turbine keeps running.
  - **Component Failure Modes:** Ground-truth failure logs catalog Gearbox breakdowns, Generator bearing wear, Transformer surges, and Hydraulic valve failures.
  - **Balanced Benchmark:** 44 labeled anomaly failure cases vs. 51 healthy normal control cases across the full repository.
* **Speaker Cue:** "We worked with the CARE_To_Compare benchmark: 89 years of SCADA data across 36 turbines. Wind Farm A in Portugal gave us ground-truth component logs for gearboxes, generator bearings, transformers, and hydraulics. Each dataset contains 1 full year of normal history, followed by a 2-to-4-week test window."

---

### Slide 4: Theoretical Challenge 1 — The Status Code Trap
* **Header:** Theoretical Challenge 1 — The 'Status Code' Trap (Data Leakage)
* **Subtitle:** Why a naive machine learning model achieves 99.9% accuracy but fails in operations
* **Left Card: The Naive Shortcut (The Cheat):**
  - In raw SCADA files, `status_type_id` records turbine states: 0 = Normal, 3 = Service, 4 = Downtime.
  - When an anomaly dataset reaches breakdown, the status flips to 4 (Turbine is halted).
  - A standard AI automatically latches onto `status_type_id == 4` and claims 99.9% accuracy.
  - **Why this is useless:** The wind farm already knows the turbine is down when it trips! Predicting downtime after the machine stops spinning has zero business value.
* **Right Card: How We Resolved It (True Physics):**
  - We strictly erased `status_type_id` from all predictive features.
  - The model must learn failure signatures exclusively from thermodynamic temperatures, vibrations, and aerodynamics.
  - The entire prediction period is evaluated to detect early degradation while status is STILL 0 (Normal operation).
  - **Operational Outcome:** The model provides genuine early warning days before the emergency control system ever trips.
* **Speaker Cue:** "Here is the first major trap we caught: in the raw data, there's a column called 'Status'. When a turbine breaks, status becomes 4 ('Downtime'). An AI will look at this and claim 99.9% accuracy. But that's useless—the operator already knows the turbine is down when it stops spinning! We strictly banned status codes from our features, forcing the model to detect trouble while the turbine is still running normally."

---

### Slide 5: Theoretical Challenge 2 — The Weather Trap & The "Rising Fever" Fix
* **Header:** Theoretical Challenge 2 — The Weather Trap & The 'Rising Fever' Fix
* **Subtitle:** Is the bearing overheating, or is it just a sunny afternoon in July?
* **Left Card: The Weather Confounding Problem:**
  - A healthy gearbox bearing naturally runs at 60°C on a hot 38°C summer afternoon.
  - A dying gearbox bearing might only reach 45°C on a freezing 2°C winter morning.
  - If you feed raw temperatures to an AI, it classifies summer as an anomaly and misses winter failures!
  - **The Scientific Challenge:** How do we isolate genuine internal mechanical friction from external weather?
* **Right Card: The Thermodynamic Solution ($\Delta T$):**
  - Just like a doctor checks fever above normal room temperature, we engineered Differential Temperatures:
    $$\Delta T = T_{\text{Component}} - T_{\text{Ambient Weather}}$$
  - Subtracting ambient weather eliminates summer/winter bias and directly exposes bearing friction.
  - Added Causal 6-Hour Moving Averages (`RollMean 6h`) to track sustained heat accumulation without future data leakage.
* **Speaker Cue:** "Here was our second big physics breakthrough: how do you know if a bearing is overheating or if it's just a hot summer day? In July, a healthy bearing reaches 60°C. In January, a failing bearing might only reach 45°C. If you feed raw temperature to an AI, it gets confused. We used the 'Rising Fever' method: we subtracted outside weather temperature ($\Delta T$). This washed away seasonal weather and exposed pure mechanical friction."

---

### Slide 6: Theoretical Challenge 3 — Generalizing to Unseen Strangers (Turbines)
* **Header:** Theoretical Challenge 3 — Generalizing to Unseen Strangers (Turbines)
* **Subtitle:** Why random train/test splits lie, and how Leave-One-Turbine-Out validation proves reality
* **Left Card: The Flaw of Random Splitting:**
  - Turbines are like human beings: each has slight individual baselines.
  - Turbine #11 might naturally run 1.5°C warmer than Turbine #0 due to its position on a ridge.
  - If you randomly shuffle 10-minute records, the AI simply memorizes individual turbine IDs rather than universal physics.
  - When deployed on a newly installed turbine, such models fail completely.
* **Right Card: Leave-One-Turbine-Out Validation:**
  - We erased turbine ID (`asset_id`) from all model input features.
  - Enforced Leave-One-Turbine-Out Group Cross-Validation: Train on Turbines 0, 10, 11, 13 and evaluate on held-out Turbine 21.
  - The model is forced to learn universal physical wear signatures that apply to ANY turbine.
  - **Proven Result:** Achieved 0.83 Test AUC on completely unseen turbines in held-out validation.
* **Speaker Cue:** "If you randomly split time series data, the AI cheats by memorizing that Turbine 11 runs a little hotter than Turbine 0. But in the real world, you want a model that works when you buy a brand-new turbine! We enforced Leave-One-Turbine-Out validation: we trained on four turbines and tested on a completely unseen fifth turbine, proving the model learned universal mechanical wear."

---

### Slide 7: Our Implemented Solution Architecture
* **Header:** Solution Architecture — How We Built the Production System
* **Subtitle:** A streamlined, high-speed pipeline combining physics, ensembles, and explainability
* **Card 1 (Data Hygiene):**
  - Parsed semicolon delimiters.
  - Audited 102M data points.
  - Sparse NAs (<0.00004%) forward-filled with locf.
  - Zero artificial values (no SMOTE).
* **Card 2 (Physics Features):**
  - $\Delta T$ differentials for Gearbox, Generator, Transformer.
  - Causal 6h rolling averages.
  - Gear ratio ($RPM_{\text{gen}} / RPM_{\text{rotor}}$).
  - $C_p$ power conversion proxy ($P / v^3$).
* **Card 3 (High-Speed Models):**
  - Benchmarked GLM, Random Forest, and XGBoost.
  - Sub-second training (<1 sec).
  - Compact memory footprint (109 MB RAM).
  - Group CV across turbines.
* **Card 4 (Explainability & UI):**
  - Exact TreeSHAP attributions.
  - LIME local decision rules.
  - Physical consistency verification.
  - Production Shiny dashboard.
* **Speaker Cue:** "Here is our 4-stage pipeline: First, clean data with zero synthetic hallucinations. Second, physics-grounded features isolating component heat and gear slip. Third, sub-second machine learning models evaluated on unseen turbines. Fourth, Explainable AI and a full Shiny web app for operators."

---

### Slide 8: Alternative Approaches Considered (The Full Landscape)
* **Header:** Alternative Approaches — What Other Approaches Could We Consider?
* **Subtitle:** Evaluating deep learning, autoencoders, vibration FFTs, and synthetic sampling
* **Card A: Deep Time-Series (LSTM / GRU / Transformers):**
  - Recurrent or attention networks modeling long sequential dependencies directly from raw time-steps.
* **Card B: Unsupervised Autoencoders (Normal Behavior Modeling):**
  - Neural networks trained only on healthy data to predict expected values; high reconstruction error signals fault.
* **Card C: Classical Vibration Signal Processing (FFT / Envelope):**
  - Fourier transforms and spectral analysis on high-frequency (kHz) accelerometers placed on bearing housings.
* **Card D: Synthetic Minority Oversampling (SMOTE / GANs):**
  - Algorithmic generation of artificial failure samples to balance positive and negative class ratios.
* **Speaker Cue:** "We didn't just pick XGBoost blindly; we evaluated the entire landscape. We looked at Deep Recurrent LSTMs, Unsupervised Reconstruction Autoencoders, High-Frequency Vibration FFTs, and Synthetic Data (SMOTE)."

---

### Slide 9: Critical Evaluation: Why We Didn't Choose Them & Future Scope
* **Header:** Critical Evaluation — Why We Didn't Choose Them & What Is Future Scope
* **Subtitle:** Clear justification of design trade-offs: what was rejected vs. what is a valuable future upgrade
* **Left Card: Rejected / Not Recommended:**
  - **Synthetic Data (SMOTE/GANs): REJECTED.** Fabricates physically impossible operating states (e.g., power at zero wind). Ruled out to preserve physical validity.
  - **Unsupervised Clustering (K-Means/PCA): NOT WORTH IT.** Produced intolerable false alarm rates on offshore weather outliers. Simple clustering lacks temporal context.
  - **End-to-End Deep Learning for 10-Min SCADA: REJECTED.** With 22 total events, deep neural nets severely overfit, require heavy compute, and destroy interpretability.
* **Right Card: Valuable Future Scope:**
  - **Physics-Informed Neural Networks (PINNs): FUTURE SCOPE.** Embedding Navier-Stokes and heat diffusion differential equations directly into loss functions for thermodynamic modeling.
  - **High-Frequency Vibration Telemetry: FUTURE SCOPE.** Integrating 10-kHz accelerometer streams for bearing inner/outer race defect frequency analysis (BPFO/BPFI).
  - **Cross-Farm Transfer Learning: FUTURE SCOPE.** Domain-adaptation models transferring failure patterns learned from Farm A (Portugal) to offshore Farm C (Germany).
* **Speaker Cue:** "Why did we reject deep learning and SMOTE? SMOTE invents fake physics. And deep neural networks with only 22 events overfit and act like total black boxes. What IS worth pursuing as future scope? Physics-Informed Neural Networks (PINNs) where differential equations are baked into the loss function, and high-frequency 10-kHz vibration sensors."

---

### Slide 10: Theoretical Challenge 4 — The Black-Box Trust Problem: SHAP & LIME
* **Header:** Theoretical Challenge 4 — The Black-Box Trust Problem: SHAP & LIME
* **Subtitle:** Why operators reject unexplained alerts and how XAI proved physical fidelity
* **Card 1: The Operator's Dilemma:**
  - If an AI flags a turbine as '90% Risk' without explanation, maintenance crews will ignore it.
  - Technicians must know WHICH component to inspect: the gearbox, the generator, or the transformer?
  - Black box predictions create distrust and alert fatigue.
* **Card 2: How SHAP Solves It:**
  - TreeSHAP calculates exact additive Shapley values based on game theory.
  - Allocates exact risk 'points' to every individual sensor channel.
  - Global SHAP reveals fleet-wide thermal drift drivers.
  - Local SHAP waterfalls explain the exact alert moment for a specific turbine.
* **Card 3: Ground Truth Match:**
  - **GEARBOX (Ev 72):** Top SHAP feature was gearbox bearing temperature (+4.3°C rise).
  - **GENERATOR (Ev 0):** Drive-end bearing temperature surged to 76°C-94°C, triggering alarm.
  - **TRANSFORMER (Ev 68):** Phase L1 reached 117°C, dominating local SHAP attributions.
  - **HEALTHY (Ev 25):** Negative scores across all components (zero alarm).
* **Speaker Cue:** "If you tell an offshore engineer 'Turbine 21 has an anomaly,' they will ask: 'Which part is broken?' If you can't tell them, they won't charter a boat. We used SHAP and LIME to peek inside the black box. When the gearbox failed, the top SHAP driver was gearbox bearing heat (+4.3°C). When the generator failed, the drive-end bearing lit up the chart. The AI points right to the broken component."

---

### Slide 11: Theoretical Challenge 5 — Asymmetric Financial Economics
* **Header:** Theoretical Challenge 5 — Asymmetric Financial Economics & Thresholding
* **Subtitle:** Why standard 50% accuracy fails in operations, and how cost matrices save millions
* **Left Card: The Asymmetric Cost Matrix:**
  - **MISSED FAILURE (False Negative):** \$150,000 - \$300,000. Shattered gearbox, offshore vessel chartering, 6 weeks lost power.
  - **FALSE ALARM (False Positive):** \$3,500. Remote log diagnostics and routine technician inspection visit.
  - **PLANNED REPAIR (True Positive):** \$8,000. Uptower bearing replacement during scheduled calm weather window.
  - **Critical Reality:** Missing a breakdown is **40 TIMES MORE EXPENSIVE** than sending a technician on a false alarm!
* **Right Card: The Cost-Optimal Threshold:**
  - In textbooks, models use a 0.50 (50%) decision threshold.
  - In wind energy, a 50% threshold allows too many catastrophic gearboxes to slip through.
  - By plotting the Total Fleet Cost Curve, we discovered the economically optimal threshold is **0.30 - 0.35**.
  - This sweet spot catches impending failures 8 to 34 days early while keeping technician inspection costs under control.
* **Speaker Cue:** "In textbooks, people use a 50% cutoff. In wind energy, that is a multi-million-dollar mistake. Missing a gearbox costs \$150,000; a false inspection costs \$3,500. Missing a failure is 40 times worse! We tuned our decision threshold to 0.30–0.35, which minimizes total financial loss and catches breakdowns weeks early."

---

### Slide 12: Deployment: The Production Shiny Dashboard
* **Header:** Decision Support — Deployment: The Production Shiny Dashboard
* **Subtitle:** Empowering wind farm operators and financial executives with interactive analytics
* **Left Card: 5 Operational Dashboard Tabs:**
  - **1. Fleet Overview:** Live status cards across 3 wind farms, turbine catalog & event registry.
  - **2. SCADA Telemetry Studio:** Multi-sensor time-series plots ($\Delta T$, wind, power) + real-time risk timeline.
  - **3. Model Benchmark & CARE:** Leave-One-Turbine-Out validation stats, confusion matrix & lead times.
  - **4. Explainable AI Studio:** Interactive SHAP waterfall and LIME rules for every failure mode.
  - **5. Business ROI Calculator:** Interactive cost sliders calculating net fleet dollar savings.
* **Right Card: Deployment & Running Locally:**
  - **Built with R & bslib:** Modern industrial Darkly theme with responsive cards and SVG icons.
  - **Instant Launch:** One-click launcher script in the project root:
    `Rscript run_app.R`
  - Or inside an active R session / RStudio:
    `shiny::runApp('shiny_app')`
  - Runs on `http://127.0.0.1:3838` with instant reactive plots, requiring zero cloud dependencies.
* **Speaker Cue:** "We didn't just leave our models in code; we deployed a full interactive Shiny dashboard. Operators can view live sensor telemetry, inspect real-time risk scores, examine SHAP waterfalls for any alert, and test financial ROI sliders to see fleet dollar savings."

---

### Slide 13: Summary & The 5-Point Presenter's Cheat Sheet
* **Header:** Summary & Key Takeaways — The 5-Point Presenter's Cheat Sheet
* **Subtitle:** Everything you need to deliver a convincing, memorable presentation
* **Card 1: Real Physics, Not Fake Data:** Rejected synthetic SMOTE and purged post-trip status codes; 100% genuine sensor telemetry.
* **Card 2: The 'Rising Fever' Method:** Differential temperatures ($\Delta T$) subtracted weather fluctuations and exposed true mechanical friction.
* **Card 3: Sub-Second Speed:** XGBoost trains in 0.67 seconds on 100k rows (109 MB RAM), reaching 0.83 AUC on completely unseen turbines.
* **Card 4: 8 to 34 Days Lead Time:** Achieved multi-week early warning across gearboxes, generator bearings, transformers, and hydraulics.
* **Card 5: Explainable & Actionable:** SHAP and LIME prove alerts match physical components; Shiny dashboard empowers operators with ROI calculators.
* **Speaker Cue:** "To wrap up, here are the 5 core takeaways: 1) Real physics, zero fake data. 2) The Rising Fever method that isolates friction. 3) Sub-second training speed on standard laptops. 4) 8 to 34 days of lead time before breakdown. And 5) Explainable AI that maintenance crews can genuinely trust. Thank you!"

---
