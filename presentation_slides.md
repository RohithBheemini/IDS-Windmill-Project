# Wind Turbine SCADA Condition Monitoring & Predictive Anomaly Detection
## Presentation Slide Deck & Complete Speaker Script
**File:** `presentation_wind_turbine_ids.pptx`  
**Layout:** 16:9 Widescreen | Clean Modern Bright-White Theme | High-Readability Large Typography  
**Palette:** Pure White Background (`#FFFFFF`), Deep Slate Text (`#0F172A`), Professional Accents (Navy, Sky Blue, Forest Green, Amber, Crimson)

---

### Slide 1: Title Slide — The Big Picture
* **Category Tag:** INDUSTRIAL DATA SCIENCE CASE STUDY
* **Main Title:** Saving Millions in the Wind
* **Subtitle:** How Physics, Machine Learning & Explainable AI Spot Turbine Failures Weeks in Advance
* **Key Results Highlights:**
  - **8 to 34 Days Early Warning** before catastrophic breakdown across all key components.
  - **0.67-Second Machine Learning Training** on 100,000 records (109 MB RAM, 0.83 AUC).
  - **Zero Fake Data** (No SMOTE hallucinations) — 100% genuine physical SCADA telemetry.
  - **Explainable AI** (SHAP & LIME) directly pointing maintenance crews to failing bearings.
* **Speaker Script:**
  > "Good morning/afternoon everyone. Today, I am excited to walk you through an industrial data science case study on wind turbine predictive maintenance. We will look at how we took real sensor telemetry from offshore turbines, rejected common machine learning shortcuts, used basic physics to spot major mechanical breakdowns weeks before they happen, and proved with Explainable AI that every alert points directly to the failing physical component."

---

### Slide 2: Step 1 (The Challenge) — The High Stakes of Wind Turbine Breakdowns
* **Header Tag:** STEP 1: THE CHALLENGE
* **Main Title:** The High Stakes of Wind Turbine Breakdowns
* **Subtitle:** Why waiting for alarms to trip at sea costs hundreds of thousands of dollars
* **Card 1: The Machine:**
  - 300-ft tall mechanical giants standing in rough offshore seas.
  - Blades span 80+ meters, capturing colossal kinetic wind energy.
  - A 20-ton internal gearbox accelerates rotor speed from 15 RPM to 1,500 RPM for the generator.
  - Extreme mechanical friction and cyclic fatigue on internal bearings 24/7.
* **Card 2: The Breakdown:**
  - A shattered gearbox costs $150,000+ in hardware alone.
  - Chartering an offshore crane vessel costs $25,000 to $40,000 per day.
  - Rough winter weather blocks ships, causing 6 to 8 weeks of idle downtime.
  - Total bill per emergency failure: $250,000 to $350,000+ in parts, boats, and lost green power.
* **Card 3: Our Mission:**
  - Detect internal wear 2 to 4 weeks BEFORE the turbine trips and halts.
  - Use existing SCADA temperature and vibration sensors without buying new hardware.
  - Give crews time to order parts and wait for calm weather windows.
  - Avoid false alarms so maintenance managers genuinely trust the system.
* **Speaker Script:**
  > "Imagine managing a wind farm out in the North Sea. When a 20-ton gearbox breaks, it's not like calling a roadside mechanic. A specialized offshore crane vessel costs upwards of $30,000 a day just to mobilize. If stormy winter seas prevent ships from docking, the turbine sits idle for nearly two months. Our mission was simple: can we detect component degradation 2 to 4 weeks early using the sensors already installed on the turbine, without drowning operators in false alarms?"

---

### Slide 3: Step 2 (The Data) — What Data Did We Listen To? (CARE_To_Compare)
* **Header Tag:** STEP 2: THE DATA
* **Main Title:** What Data Did We Listen To? (CARE_To_Compare)
* **Subtitle:** 89 years of real SCADA telemetry across 36 turbines in Portugal and Germany
* **Left Card: Multi-Farm Telemetry Network:**
  - **Farm A (Portugal, Onshore):** 5 turbines, 22 datasets, 86 sensor channels with ground-truth failure logs from EDP Open Data.
  - **Farm B & C (Germany, Offshore):** 73 datasets, up to 957 sensor channels in harsh marine environments.
  - **Standard 10-Minute Telemetry (IEC 61400-25):** Mean, min, max, and standard deviation recorded continuously.
  - **Monitored Signals:** Wind speed, electric active power, generator bearing temperatures, gearbox oil temperatures, rotor RPM, blade pitch angles.
* **Right Card: Anatomy of Monitored Events:**
  - **1 Full Year of Normal History:** Exactly ~52,000 observations establishing baseline seasonal operating behavior for that specific machine.
  - **2 to 4-Week Prediction Window:** The subsequent critical evaluation period evaluated for incipient mechanical fault.
  - **44 Labeled Anomaly Cases vs 51 Healthy Controls:** Ground-truth confirmed failures across 4 critical sub-assemblies.
  - **Monitored Components:** Gearbox High-Speed Shaft, Generator Drive-End Bearing, Transformer Winding, Hydraulics.
* **Speaker Script:**
  > "To solve this, we used the CARE_To_Compare benchmark: an extensive archive containing 89 cumulative years of SCADA data across 36 commercial turbines. Farm A in Portugal gave us ground-truth component logs for gearboxes, generator bearings, transformers, and hydraulics. Crucially, each event provides exactly 1 full year of normal history to learn baseline operating behavior, followed by a 2-to-4-week test window."

---

### Slide 4: Step 3 (Ground Rules) — Avoiding the Two Classic AI Cheats
* **Header Tag:** STEP 3: GROUND RULES
* **Main Title:** Avoiding the Two Classic AI Cheats
* **Subtitle:** Why naive data science achieves 99% accuracy on paper but fails completely in the real world
* **Left Card: Trap 1: The 'Status Code' Shortcut:**
  - In raw SCADA data, there is a column called `status_type_id` (0=Normal, 4=Downtime).
  - When a turbine breaks down and stops, this column flips to 4.
  - A naive AI learns: 'If status is 4, it is broken!' and boasts 99.9% accuracy.
  - **Why this is useless:** The wind farm already knows the machine is broken when it stops spinning!
  - **Our Fix:** We strictly erased all status codes from predictive features, forcing the model to detect trouble while the turbine is still running normally.
* **Right Card: Trap 2: The 'Fake Data' Trap (SMOTE):**
  - Because failures are rare, data scientists often generate synthetic samples with SMOTE.
  - **The Physical Flaw:** Turbines obey strict laws of thermodynamics and Betz aerodynamic limits.
  - A mathematical algorithm blindly invents data points: e.g. 2,000 kW power at zero wind speed and 90° blade pitch!
  - That is physically impossible in the real world.
  - **Our Commitment:** Zero synthetic data. Every single observation in our model is 100% genuine sensor telemetry.
* **Speaker Script:**
  > "Here are the two traps that ruin many academic predictive maintenance projects. Trap 1: in the raw data, there's a column called 'Status'. When a turbine breaks, status changes to 4 ('Downtime'). An AI will latch onto this and claim 99.9% accuracy. But that's useless—the operator already knows the turbine is down! We strictly deleted status codes so our model must detect trouble while the turbine is still running. Trap 2: synthetic oversampling like SMOTE creates physically impossible states—like generating 2,000 kW of power with zero wind! We strictly banned SMOTE to preserve 100% physical reality."

---

### Slide 5: Step 4 (Physics Features) — The 'Rising Fever' Breakthrough ($\Delta T$)
* **Header Tag:** STEP 4: PHYSICS FEATURES
* **Main Title:** The 'Rising Fever' Breakthrough ($\Delta T$)
* **Subtitle:** Why raw temperature lies to models and how basic thermodynamics isolates friction
* **Left Card: The Weather Confounding Trap:**
  - In hot July, a perfectly healthy bearing reaches 60°C simply because the outside air is 38°C.
  - In freezing January, a dying, grinding bearing might only reach 45°C because the outside air is 2°C.
  - If you feed raw temperatures to an AI, it treats summer as an emergency and misses winter breakdowns!
  - **The Challenge:** How do you isolate mechanical friction from outside weather fluctuations?
* **Right Card: The Thermodynamic Solution ($\Delta T$):**
  - Just like a doctor measures a fever above room temperature, we subtracted outside weather:
    $$\Delta T = T_{\text{Component}} - T_{\text{Ambient}}$$
  - This wiped out summer/winter seasonal noise and exposed pure bearing and gear friction.
  - **Causal 6-Hour Rolling Fever:** Tracks slow, creeping heat accumulation without future leakage.
  - **Gearbox Slip Ratio ($RPM_{\text{gen}} / RPM_{\text{rotor}}$):** Flags dragging or slipping mechanical gears.
* **Speaker Script:**
  > "Here was our core physics breakthrough. If you look at raw temperature, a healthy bearing in hot July reaches 60°C, while a failing bearing in freezing January might only reach 45°C. Raw temperature confuses machine learning models. We used what we call the 'Rising Fever' method: we subtracted ambient weather temperature from each component. This simple differential wiped away weather noise and exposed pure mechanical friction."

---

### Slide 6: Step 5 (The Model) — Sub-Second Machine Learning (Why XGBoost Wins)
* **Header Tag:** STEP 5: THE MODEL
* **Main Title:** Sub-Second Machine Learning (Why XGBoost Wins)
* **Subtitle:** Why tabular SCADA telemetry needs gradient boosted trees, not heavy deep neural networks
* **Card 1: Logistic Regression:**
  - Training Time: 1.61 seconds.
  - Test AUC: 0.7544.
  - Pros: Simple, highly interpretable linear coefficients.
  - Cons: Cannot capture non-linear aerodynamic power curves or multi-sensor thermal interactions.
* **Card 2: Random Forest (`ranger`):**
  - Training Time: 14.58 seconds.
  - Test AUC: 0.7735.
  - Pros: 100 de-correlated trees voting in parallel, resistant to outlier noise.
  - Cons: Slower training; conservative probabilities on extreme minority failure states.
* **Card 3: XGBoost (Champion):**
  - Training Time: **0.67 seconds!**
  - Test AUC: **0.8297 (Top score).**
  - RAM Usage: **Only 109 MB.**
  - Why It Wins: Gradient boosting focuses sequentially on difficult subtle temperature drifts. Runs in sub-second speed on standard laptop CPUs.
* **Speaker Script:**
  > "A lot of people ask: 'Do you need deep neural networks or hours of GPU training?' The answer on tabular SCADA telemetry is a resounding no. We benchmarked Logistic Regression, Random Forest, and XGBoost. XGBoost trained in just 0.67 seconds on 100,000 records, consumed only 109 MB of RAM, and achieved the highest test AUC of 0.83. It is fast, lightweight, and incredibly accurate."

---

### Slide 7: Step 6 (Scientific Testing) — Testing on Complete Strangers (Turbine Generalization)
* **Header Tag:** STEP 6: SCIENTIFIC TESTING
* **Main Title:** Testing on Complete Strangers (Turbine Generalization)
* **Subtitle:** Why random train/test splits lie and how Leave-One-Turbine-Out validation proves reality
* **Left Card: Why Standard Random Splits Lie:**
  - Turbines are like human beings: each has slight personal quirks.
  - Turbine #11 might naturally run 1.5°C warmer than Turbine #0 due to its position on the hill.
  - If you randomly shuffle 10-minute rows, the model memorizes individual turbine IDs rather than universal physics.
  - When installed on a brand-new turbine, models trained with random splits fail completely.
* **Right Card: Leave-One-Turbine-Out Proof:**
  - We completely removed turbine ID (`asset_id`) from all model input features.
  - We trained the model on Turbines 0, 10, 11, and 13, and evaluated it on a totally unseen held-out Turbine 21.
  - The AI was forced to learn universal laws of mechanical wear that apply to ANY machine.
  - **Proven Result:** Achieved 0.83 AUC on held-out stranger turbine, proving robust real-world generalization.
* **Speaker Script:**
  > "In data science, randomly splitting your rows is a major trap. Turbines have individual personalities—Turbine 11 might run 1.5 degrees hotter than Turbine 0 just because of wind exposure on the ridge. If you shuffle data, the AI cheats by memorizing turbine IDs. We enforced Leave-One-Turbine-Out validation: we trained on Turbines 0, 10, 11, and 13, and tested on an unseen Turbine 21. Achieving 0.83 AUC on a complete stranger proves our model learned universal physics."

---

### Slide 8: Step 7 (Lead Time Results) — 8 to 34 Days Notice: The CARE Earliness Results
* **Header Tag:** STEP 7: LEAD TIME RESULTS
* **Main Title:** 8 to 34 Days Notice: The CARE Earliness Results
* **Subtitle:** Real lead times achieved before catastrophic trip across all major physical assemblies
* **Component 1: Gearbox High-Speed Shaft:**
  - **14.0 to 16.6 Days Notice (337 to 400 hours).**
  - Advance warning before high-speed shaft bearing failure. Ample time to mobilize cranes and stage replacements.
* **Component 2: Generator Drive-End Bearing:**
  - **19.7 to 34.2 Days Notice (472 to 820 hours).**
  - Thermal drift detected nearly a month in advance, preventing electrical fire and generator seizure.
* **Component 3: High-Voltage Transformer:**
  - **15.9 Days Notice (381 hours).**
  - Advance warning on Phase L1 winding insulation breakdown, averting major substation flashover.
* **Component 4: Hydraulic Pitch Group:**
  - **8.0 Days Notice (192 hours).**
  - Advance warning on proportional pitch valve pressure loss, allowing safe blade feathering before overspeed.
* **Speaker Script:**
  > "Here are the early-warning lead times our model achieved under the international CARE benchmark. For gearboxes, we caught failure 14 to 16 days in advance. For generator bearings, we gave between 19 and 34 days of advance notice—nearly a full month! That gives the maintenance manager ample time to monitor maritime weather, order spare parts, and schedule uptower repairs during a calm weather window."

---

### Slide 9: Step 8 (Explainable AI) — Opening the Black Box: Why Engineers Trust the Model
* **Header Tag:** STEP 8: EXPLAINABLE AI
* **Main Title:** Opening the Black Box: Why Engineers Trust the Model
* **Subtitle:** Using SHAP & LIME to prove that AI alerts point directly to the failing mechanical parts
* **Left Card: The Trust Problem: Why XAI Is Mandatory:**
  - If an AI alerts: 'Turbine 21 is at 90% Risk', the maintenance manager asks: 'Which part is broken?'
  - If the model cannot explain itself, engineers will ignore the alert to avoid wasting a $30,000 boat charter.
  - **TreeSHAP:** Calculates exact additive risk contributions (in Shapley points) for every sensor channel.
  - **LIME:** Generates human-readable 'if-then' diagnostic rules explaining individual alert moments.
* **Right Card: Physical Ground-Truth Verifications:**
  - **Gearbox Failure (Ev 72):** Top SHAP feature was `temp_gearbox_bearing` (+4.3°C rise) and oil heat. Exact match to friction physics.
  - **Generator Bearing Failure (Ev 0):** Drive-end bearing surged to 76°C, completely dominating SHAP attributions.
  - **Transformer Surge (Ev 68):** Phase L1 reached 117°C, correctly driving local alert triggers.
  - **Healthy Turbine (Ev 25):** Negative scores across all components, keeping false alarms at zero.
* **Speaker Script:**
  > "If you tell an offshore engineer 'The AI says Turbine 21 has an anomaly,' they will ask: 'Which part is broken?' If the AI can't answer, they won't charter a ship. We integrated SHAP and LIME to open the black box. When we audited real failures, the results were striking: for Event 72, the top SHAP driver was gearbox bearing heat (+4.3°C). For Event 0, the Drive-End generator bearing lit up the chart. The AI points right to the broken part."

---

### Slide 10: Step 9 (Business ROI) — The Money Story: Finding the Financial Sweet Spot
* **Header Tag:** STEP 9: BUSINESS ROI
* **Main Title:** The Money Story: Finding the Financial Sweet Spot
* **Subtitle:** Why 50% thresholding is a multi-million-dollar mistake and how cost matrices save $4.5M
* **Left Card: The 40:1 Asymmetric Cost Reality:**
  - **Missed Failure (False Negative):** $150,000 to $300,000+. Shattered gearbox, offshore vessel charter, 8 weeks lost power.
  - **False Alarm (False Positive):** $3,500. Remote log diagnostics and routine technician inspection visit.
  - **Planned Repair (True Positive):** $8,000. Uptower bearing replacement during scheduled calm weather window.
  - **Core Reality:** Missing a breakdown is **40 TIMES MORE EXPENSIVE** than sending a technician on a false alarm!
* **Right Card: The 0.35 Optimal Threshold:**
  - In textbooks, models use a 0.50 cutoff. In wind energy, that lets too many catastrophic breakdowns slip through.
  - By optimizing total fleet costs, the ideal threshold is **0.30 - 0.35**.
  - **Expected Fleet Savings:** **~$4.5 Million** net savings across 36 turbines over 2-3 years.
  - **Avoided Downtime:** **6,500 hours** of productive green energy generation saved.
  - **Estimated Return on Investment:** **~200% ROI** on the condition monitoring platform.
* **Speaker Script:**
  > "In standard machine learning, people use a 50% cutoff. In wind energy, that is a multi-million-dollar mistake. Missing a failure costs $150,000; a false inspection costs $3,500. A missed failure is 40 times worse! We calculated the total financial cost curve and found the sweet spot at 0.30 to 0.35. At this threshold, our model delivers ~$4.5 Million in net savings and saves 6,500 hours of downtime across a 36-turbine fleet."

---

### Slide 11: Step 10 (Decision Support) — Empowering Operators: The Interactive Shiny Dashboard
* **Header Tag:** STEP 10: DECISION SUPPORT
* **Main Title:** Empowering Operators: The Interactive Shiny Dashboard
* **Subtitle:** A complete live decision support application with real-time SCADA telemetry & ROI calculus
* **Left Card: 5 Operational Dashboard Tabs:**
  - **1. Fleet Overview:** Live status cards across 3 farms, turbine registry, and event logs.
  - **2. Telemetry Studio:** Multi-sensor time-series (Delta T, power, wind) + real-time risk timeline.
  - **3. Model Benchmark:** Cross-validation audit tables, confusion matrices, and CARE lead times.
  - **4. Explainable AI:** Interactive SHAP waterfalls and LIME diagnostic rulebook.
  - **5. ROI Calculator:** Sliders for repair costs, fleet size, and interactive net dollar savings.
* **Right Card: Master Script Execution (`main.R`):**
  - **One-Click Launch:** The master runner handles all workflows:
    - `Rscript main.R` (Live demo + launch dashboard)
    - `Rscript main.R --app` (Directly launch dashboard)
    - `Rscript main.R --demo` (Terminal condition demo)
    - `Rscript main.R --train` (Re-train ML models)
  - **Zero Cloud Dependencies:** Runs locally on `http://127.0.0.1:3838` with instant reactive rendering.
* **Speaker Script:**
  > "We wrapped this entire methodology into a production Shiny dashboard. Operators can view live sensor telemetry, inspect real-time risk timelines, explore interactive SHAP waterfall plots for any alert, and test financial ROI sliders to calculate dollar savings for their fleet. The entire project is controlled by a single master script, `main.R`, which launches in one command."

---

### Slide 12: Step 11 (Summary) — The 5-Point Presenter's Cheat Sheet
* **Header Tag:** STEP 11: SUMMARY
* **Main Title:** The 5-Point Presenter's Cheat Sheet
* **Subtitle:** Everything you need to deliver a convincing, memorable presentation in 60 seconds
* **Card 1: Real Physics, Not Fake Data:**
  - Rejected synthetic SMOTE and purged post-trip status codes; 100% genuine sensor telemetry.
* **Card 2: The 'Rising Fever' Method:**
  - Differential temperatures ($\Delta T$) subtracted weather fluctuations and exposed true mechanical friction.
* **Card 3: Sub-Second Speed:**
  - XGBoost trains in 0.67 seconds on 100k rows (109 MB RAM), reaching 0.83 AUC on completely unseen turbines.
* **Card 4: 8 to 34 Days Lead Time:**
  - Achieved multi-week early warning across gearboxes, generator bearings, transformers, and hydraulics.
* **Card 5: Explainable & Actionable:**
  - SHAP and LIME prove alerts match physical components; Shiny dashboard empowers operators with ROI calculators.
* **Speaker Script:**
  > "To wrap up, here are the 5 core takeaways: 1) Real physics, zero fake data. 2) The Rising Fever method that isolates friction. 3) Sub-second training speed on standard hardware. 4) 8 to 34 days of lead time before breakdown. And 5) Explainable AI that maintenance crews can genuinely trust. Thank you!"

---
*Presentation deck and speaker guide prepared for academic review and executive industry demonstration.*
