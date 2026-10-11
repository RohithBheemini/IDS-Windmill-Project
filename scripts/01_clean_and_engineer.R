# scripts/01_clean_and_engineer.R
# End-to-end data cleaning, hygiene validation, and physics-grounded feature engineering
suppressPackageStartupMessages({
  library(data.table)
  library(zoo)
})

cat("========================================================\n")
cat("STEP 1: WIND TURBINE SCADA DATA CLEANING & FEATURE PIPELINE\n")
cat("========================================================\n\n")

base_dir <- file.path(getwd(), "CARE_To_Compare", "CARE_To_Compare")
output_dir <- file.path(getwd(), "data_clean")
dir.create(output_dir, showWarnings = FALSE)

# 1. Load Event Info and Feature Descriptions across all farms
events_a <- fread(file.path(base_dir, "Wind Farm A", "event_info.csv"), sep = ";")
feats_a  <- fread(file.path(base_dir, "Wind Farm A", "feature_description.csv"), sep = ";")
events_b <- fread(file.path(base_dir, "Wind Farm B", "event_info.csv"), sep = ";")
events_c <- fread(file.path(base_dir, "Wind Farm C", "event_info.csv"), sep = ";")

cat(sprintf("Loaded metadata: Farm A (%d events), Farm B (%d events), Farm C (%d events)\n",
            nrow(events_a), nrow(events_b), nrow(events_c)))

# Standardize failure categories for Wind Farm A
events_a[, failure_mode := fcase(
  event_label == "normal", "Normal",
  grepl("Transformer", event_description, ignore.case = TRUE), "Transformer",
  grepl("Gearbox", event_description, ignore.case = TRUE), "Gearbox",
  grepl("Generator", event_description, ignore.case = TRUE), "Generator Bearing",
  grepl("Hydraulic", event_description, ignore.case = TRUE), "Hydraulic Group",
  default = "Other Anomaly"
)]

cat("Wind Farm A Failure Mode Breakdown:\n")
print(table(events_a$failure_mode))

# 2. Process Wind Farm A Datasets with Domain-Informed Engineering
farm_a_dir <- file.path(base_dir, "Wind Farm A", "datasets")
event_features_list <- list()
telemetry_samples_list <- list()

for (i in 1:nrow(events_a)) {
  ev_id    <- events_a$event_id[i]
  ev_label <- events_a$event_label[i]
  ev_mode  <- events_a$failure_mode[i]
  asset    <- events_a$asset[i]
  fpath    <- file.path(farm_a_dir, paste0(ev_id, ".csv"))
  
  if (!file.exists(fpath)) next
  
  # Fast read
  dt <- fread(fpath, sep = ";")
  
  # Step 2a: Physical Validation & Hygiene
  # Clean NAs using Last Observation Carried Forward (locf) within turbine series
  num_cols <- names(dt)[sapply(dt, is.numeric)]
  for (col in num_cols) {
    if (anyNA(dt[[col]])) {
      set(dt, j = col, value = na.locf(dt[[col]], na.rm = FALSE))
      # If leading NAs remain, backward fill
      if (anyNA(dt[[col]])) {
        set(dt, j = col, value = na.locf(dt[[col]], fromLast = TRUE, na.rm = FALSE))
      }
    }
  }
  
  # Physical Boundary Corrections (No artificial hallucinations, clipping obvious sensor transmission glitches)
  # Wind speed cannot be negative
  dt[wind_speed_3_avg < 0, wind_speed_3_avg := 0]
  # Pitch angle in normal operating envelope [-10, 95]
  dt[sensor_5_avg < -10, sensor_5_avg := -10]
  dt[sensor_5_avg > 95, sensor_5_avg := 95]
  
  # Step 2b: Engineering Physical Indicators
  dt[, `:=`(
    event_id = ev_id,
    asset_id = asset,
    failure_mode = ev_mode,
    is_anomaly_event = as.integer(ev_label == "anomaly"),
    
    # Subsystem Temperatures
    temp_ambient           = sensor_0_avg,
    temp_gearbox_bearing  = sensor_11_avg,
    temp_gearbox_oil      = sensor_12_avg,
    temp_gen_bearing_de   = sensor_13_avg,
    temp_gen_bearing_nde  = sensor_14_avg,
    temp_generator_stator = (sensor_16_avg + sensor_17_avg + sensor_18_avg) / 3,
    temp_transformer      = (sensor_39_avg + sensor_40_avg + sensor_41_avg) / 3,
    temp_hydraulic_oil    = sensor_42_avg,
    temp_nacelle          = sensor_44,
    
    # Temperature Differentials over Ambient (Thermodynamic Stress)
    delta_T_gearbox     = sensor_11_avg - sensor_0_avg,
    delta_T_oil         = sensor_12_avg - sensor_0_avg,
    delta_T_gen_de      = sensor_13_avg - sensor_0_avg,
    delta_T_gen_nde     = sensor_14_avg - sensor_0_avg,
    delta_T_transformer = ((sensor_39_avg + sensor_40_avg + sensor_41_avg) / 3) - sensor_0_avg,
    delta_T_hydraulic   = sensor_42_avg - sensor_0_avg,
    delta_T_nacelle     = sensor_44 - sensor_0_avg,
    
    # Aerodynamic & Electrical Telemetry
    wind_speed        = wind_speed_3_avg,
    wind_speed_std    = wind_speed_3_std,
    wind_speed_max    = wind_speed_3_max,
    pitch_angle       = sensor_5_avg,
    pitch_angle_std   = sensor_5_std,
    generator_rpm     = sensor_18_avg,
    rotor_rpm         = sensor_53_avg,
    active_power      = power_30_avg,
    reactive_power    = sensor_31_avg
  )]
  
  # Electromechanical ratios
  dt[, gear_ratio_est := fifelse(rotor_rpm > 1 & generator_rpm > 50, generator_rpm / rotor_rpm, 0)]
  dt[, power_coefficient := fifelse(wind_speed > 3 & active_power > 0, active_power / (wind_speed^3), 0)]
  dt[, apparent_power := sqrt(active_power^2 + reactive_power^2)]
  
  # Temporal degradation markers: 6-hour (36-step) and 24-hour (144-step) rolling statistics
  # Using only backward rolling alignment to avoid any lookahead leakage
  dt[, roll_mean_gearbox_6h := rollmean(delta_T_gearbox, k = 36, fill = "extend", align = "right")]
  dt[, roll_mean_gen_de_6h  := rollmean(delta_T_gen_de, k = 36, fill = "extend", align = "right")]
  dt[, roll_mean_trans_6h   := rollmean(delta_T_transformer, k = 36, fill = "extend", align = "right")]
  dt[, roll_mean_hydr_6h    := rollmean(delta_T_hydraulic, k = 36, fill = "extend", align = "right")]
  
  # Step 2c: Timestep Target Definition (Predicting Anomaly State vs Normal)
  # In training data, normal operation has status_type_id == 0.
  # In prediction data:
  # If normal event -> all prediction points are Normal (target = 0).
  # If anomaly event -> prediction points represent the degradation and failure event (target = 1).
  dt[, target := fifelse(train_test == "prediction" & ev_label == "anomaly", 1L, 0L)]
  
  # Step 2d: Construct Event-level Summary Features
  # Summarize the operational window of prediction vs normal
  pred_dt <- dt[train_test == "prediction"]
  if (nrow(pred_dt) > 0) {
    # We take the first 500 timesteps (~3.5 days) of prediction period for early warning feature extraction
    early_dt <- pred_dt[1:min(nrow(pred_dt), 500)]
    
    event_features_list[[i]] <- data.table(
      event_id             = ev_id,
      asset_id             = asset,
      event_label          = ev_label,
      failure_mode         = ev_mode,
      target               = as.integer(ev_label == "anomaly"),
      pred_duration_hours  = round(nrow(pred_dt) * 10 / 60, 1),
      
      # Mean Thermal Differentials
      mean_delta_T_gearbox     = mean(early_dt$delta_T_gearbox, na.rm = TRUE),
      max_delta_T_gearbox      = max(early_dt$delta_T_gearbox, na.rm = TRUE),
      mean_delta_T_oil         = mean(early_dt$delta_T_oil, na.rm = TRUE),
      mean_delta_T_gen_de      = mean(early_dt$delta_T_gen_de, na.rm = TRUE),
      max_delta_T_gen_de       = max(early_dt$delta_T_gen_de, na.rm = TRUE),
      mean_delta_T_gen_nde     = mean(early_dt$delta_T_gen_nde, na.rm = TRUE),
      mean_delta_T_transformer = mean(early_dt$delta_T_transformer, na.rm = TRUE),
      max_delta_T_transformer  = max(early_dt$delta_T_transformer, na.rm = TRUE),
      mean_delta_T_hydraulic   = mean(early_dt$delta_T_hydraulic, na.rm = TRUE),
      max_delta_T_hydraulic    = max(early_dt$delta_T_hydraulic, na.rm = TRUE),
      
      # Mechanical & Aerodynamic
      mean_wind_speed          = mean(early_dt$wind_speed, na.rm = TRUE),
      mean_pitch_angle         = mean(early_dt$pitch_angle, na.rm = TRUE),
      sd_pitch_angle           = sd(early_dt$pitch_angle, na.rm = TRUE),
      mean_active_power        = mean(early_dt$active_power, na.rm = TRUE),
      mean_apparent_power      = mean(early_dt$apparent_power, na.rm = TRUE),
      mean_gear_ratio          = mean(early_dt$gear_ratio_est[early_dt$gear_ratio_est > 0], na.rm = TRUE),
      sd_gearbox_temp          = sd(early_dt$temp_gearbox_bearing, na.rm = TRUE),
      sd_gen_de_temp           = sd(early_dt$temp_gen_bearing_de, na.rm = TRUE)
    )
  }
  
  # Step 2e: Select representative telemetry rows for time-series modeling
  # To avoid memory bottlenecks while preserving 100% of event prediction dynamics:
  # - Keep 100% of prediction period observations (full 10-minute resolution for evaluation)
  # - Subsample training data to 30-minute intervals (step = 3) during normal operation (status 0)
  train_sample <- dt[train_test == "train" & status_type_id == 0][seq(1, .N, by = 3)]
  pred_sample  <- dt[train_test == "prediction"]
  
  combined_sample <- rbind(train_sample, pred_sample)
  
  # Keep only engineered clean columns (EXCLUDING leaky status_type_id and id)
  feature_cols <- c(
    "time_stamp", "event_id", "asset_id", "train_test", "failure_mode", "target",
    "temp_ambient", "temp_gearbox_bearing", "temp_gearbox_oil", "temp_gen_bearing_de",
    "temp_gen_bearing_nde", "temp_generator_stator", "temp_transformer", "temp_hydraulic_oil",
    "temp_nacelle", "delta_T_gearbox", "delta_T_oil", "delta_T_gen_de", "delta_T_gen_nde",
    "delta_T_transformer", "delta_T_hydraulic", "delta_T_nacelle", "wind_speed",
    "wind_speed_std", "wind_speed_max", "pitch_angle", "pitch_angle_std", "generator_rpm",
    "rotor_rpm", "active_power", "reactive_power", "gear_ratio_est", "power_coefficient",
    "apparent_power", "roll_mean_gearbox_6h", "roll_mean_gen_de_6h", "roll_mean_trans_6h",
    "roll_mean_hydr_6h"
  )
  
  telemetry_samples_list[[i]] <- combined_sample[, ..feature_cols]
}

# 3. Combine and Save Clean Datasets
clean_telemetry <- rbindlist(telemetry_samples_list)
clean_events    <- rbindlist(event_features_list)

cat("\n=== CLEAN DATASET SUMMARY ===\n")
cat(sprintf("Clean Telemetry Dataset: %d rows x %d columns\n", nrow(clean_telemetry), ncol(clean_telemetry)))
cat(sprintf("Clean Event-level Dataset: %d events x %d columns\n", nrow(clean_events), ncol(clean_events)))
cat("Target Distribution in Telemetry:\n")
print(table(clean_telemetry$target))
cat("Target Distribution in Events:\n")
print(table(clean_events$target))

# Save RDS and CSV for modeling and Shiny app
saveRDS(clean_telemetry, file.path(output_dir, "clean_telemetry.rds"))
saveRDS(clean_events, file.path(output_dir, "clean_events.rds"))
fwrite(clean_events, file.path(output_dir, "clean_events.csv"))

# Also save Wind Farms B and C metadata overview
saveRDS(events_b, file.path(output_dir, "events_farm_b.rds"))
saveRDS(events_c, file.path(output_dir, "events_farm_c.rds"))

cat("\nSaved clean data artifacts successfully to 'data_clean/'.\n")
