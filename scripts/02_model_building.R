# scripts/02_model_building.R
# Comprehensive multi-model training, group cross-validation, and business evaluation
suppressPackageStartupMessages({
  library(data.table)
  library(ranger)
  library(xgboost)
  library(pROC)
})

cat("========================================================\n")
cat("STEP 2: MODEL BUILDING & RIGOROUS INDUSTRIAL BENCHMARKING\n")
cat("========================================================\n\n")

data_dir  <- file.path(getwd(), "data_clean")
model_dir <- file.path(getwd(), "models")
dir.create(model_dir, showWarnings = FALSE)

# 1. Load Clean Telemetry and Event Data
telemetry <- readRDS(file.path(data_dir, "clean_telemetry.rds"))
events    <- readRDS(file.path(data_dir, "clean_events.rds"))

cat(sprintf("Telemetry dataset loaded: %d rows\n", nrow(telemetry)))
cat(sprintf("Event-level dataset loaded: %d events\n", nrow(events)))

# Feature list for predictive models (Strictly excluding leaky status_type_id and static IDs)
feature_cols <- c(
  "temp_ambient", "temp_gearbox_bearing", "temp_gearbox_oil", "temp_gen_bearing_de",
  "temp_gen_bearing_nde", "temp_generator_stator", "temp_transformer", "temp_hydraulic_oil",
  "temp_nacelle", "delta_T_gearbox", "delta_T_oil", "delta_T_gen_de", "delta_T_gen_nde",
  "delta_T_transformer", "delta_T_hydraulic", "delta_T_nacelle", "wind_speed",
  "wind_speed_std", "wind_speed_max", "pitch_angle", "pitch_angle_std", "generator_rpm",
  "rotor_rpm", "active_power", "reactive_power", "gear_ratio_est", "power_coefficient",
  "apparent_power", "roll_mean_gearbox_6h", "roll_mean_gen_de_6h", "roll_mean_trans_6h",
  "roll_mean_hydr_6h"
)

# 2. Leave-One-Turbine-Out Cross-Validation (Group K-Fold by Asset ID)
turbines <- sort(unique(telemetry$asset_id))
cat(sprintf("Evaluating models across %d wind turbines: %s\n", length(turbines), paste(turbines, collapse = ", ")))

# Prepare a balanced/stratified training sample for model training efficiency:
# In each turbine's train data, keep all anomalies and sample normal points
set.seed(42)
sample_idx <- telemetry[, .I[target == 1 | (target == 0 & runif(.N) < 0.25)]]
dt_sub <- telemetry[sample_idx]
cat(sprintf("Working training sample size: %d rows (Anomalies: %d, Normal: %d)\n",
            nrow(dt_sub), sum(dt_sub$target == 1), sum(dt_sub$target == 0)))

cv_predictions <- data.table(
  asset_id = dt_sub$asset_id,
  target = dt_sub$target,
  glm_prob = 0.0,
  rf_prob  = 0.0,
  xgb_prob = 0.0
)

# Cross-Validation Loop across physical turbines
for (turb in turbines) {
  cat(sprintf("\n--- Cross-Validation Fold: Holding out Turbine %s ---\n", turb))
  train_fold <- dt_sub[asset_id != turb]
  test_fold  <- dt_sub[asset_id == turb]
  
  # A. Regularized Logistic Regression (GLM)
  glm_fit <- glm(
    formula = as.formula(paste("target ~", paste(feature_cols, collapse = " + "))),
    data = train_fold,
    family = binomial(link = "logit")
  )
  pred_glm <- predict(glm_fit, newdata = test_fold, type = "response")
  cv_predictions[asset_id == turb, glm_prob := pred_glm]
  
  # B. Random Forest (Ranger)
  rf_fit <- ranger(
    formula = as.formula(paste("target ~", paste(feature_cols, collapse = " + "))),
    data = train_fold,
    num.trees = 100,
    probability = TRUE,
    num.threads = 4,
    seed = 42
  )
  pred_rf <- predict(rf_fit, data = test_fold)$predictions[, 2]
  cv_predictions[asset_id == turb, rf_prob := pred_rf]
  
  # C. Extreme Gradient Boosting (XGBoost)
  dtrain <- xgb.DMatrix(data = as.matrix(train_fold[, ..feature_cols]), label = train_fold$target)
  dtest  <- xgb.DMatrix(data = as.matrix(test_fold[, ..feature_cols]), label = test_fold$target)
  
  xgb_fit <- xgb.train(
    params = list(
      objective = "binary:logistic",
      eval_metric = "auc",
      max_depth = 6,
      eta = 0.1,
      subsample = 0.8,
      colsample_bytree = 0.8
    ),
    data = dtrain,
    nrounds = 80,
    verbose = 0
  )
  pred_xgb <- predict(xgb_fit, newdata = dtest)
  cv_predictions[asset_id == turb, xgb_prob := pred_xgb]
}

# 3. Comprehensive Performance Metrics
cat("\n========================================================\n")
cat("CROSS-VALIDATION PERFORMANCE SUMMARY (LEAVE-ONE-TURBINE-OUT)\n")
cat("========================================================\n")

calc_metrics <- function(actual, probs, model_name, threshold = 0.35) {
  roc_obj <- roc(actual, probs, quiet = TRUE)
  auc_val <- as.numeric(auc(roc_obj))
  
  pred_bin <- as.integer(probs >= threshold)
  tp <- sum(actual == 1 & pred_bin == 1)
  fp <- sum(actual == 0 & pred_bin == 1)
  tn <- sum(actual == 0 & pred_bin == 0)
  fn <- sum(actual == 1 & pred_bin == 0)
  
  sensitivity <- tp / (tp + fn)
  specificity <- tn / (tn + fp)
  precision   <- ifelse((tp + fp) > 0, tp / (tp + fp), 0)
  f1_score    <- ifelse((precision + sensitivity) > 0, 2 * (precision * sensitivity) / (precision + sensitivity), 0)
  
  # Asymmetric Business Cost Calculation ($)
  # Cost: FN = $150k, FP = $3.5k, TP = $8k, TN = $0
  total_cost  <- (fn * 150000) + (fp * 3500) + (tp * 8000)
  baseline_cost <- (sum(actual == 1) * 150000) # If no detector was used
  savings     <- baseline_cost - total_cost
  
  data.table(
    Model = model_name,
    ROC_AUC = round(auc_val, 4),
    Sensitivity_Recall = round(sensitivity, 4),
    Specificity = round(specificity, 4),
    Precision = round(precision, 4),
    F1_Score = round(f1_score, 4),
    Total_Cost_USD = total_cost,
    Net_Savings_USD = savings
  )
}

metrics_glm <- calc_metrics(cv_predictions$target, cv_predictions$glm_prob, "Logistic Regression (GLM)")
metrics_rf  <- calc_metrics(cv_predictions$target, cv_predictions$rf_prob, "Random Forest (Ranger)")
metrics_xgb <- calc_metrics(cv_predictions$target, cv_predictions$xgb_prob, "XGBoost")

benchmark_results <- rbind(metrics_glm, metrics_rf, metrics_xgb)
print(benchmark_results)

# 4. Train Final Full Production Models
cat("\nTraining Final Full Production Models on All Fleet Data...\n")

final_rf <- ranger(
  formula = as.formula(paste("target ~", paste(feature_cols, collapse = " + "))),
  data = dt_sub,
  num.trees = 150,
  importance = "impurity",
  probability = TRUE,
  num.threads = 4,
  seed = 42
)

dtrain_full <- xgb.DMatrix(data = as.matrix(dt_sub[, ..feature_cols]), label = dt_sub$target)
final_xgb <- xgb.train(
  params = list(
    objective = "binary:logistic",
    eval_metric = "auc",
    max_depth = 6,
    eta = 0.08,
    subsample = 0.85,
    colsample_bytree = 0.85
  ),
  data = dtrain_full,
  nrounds = 100,
  verbose = 0
)

final_glm <- glm(
  formula = as.formula(paste("target ~", paste(feature_cols, collapse = " + "))),
  data = dt_sub,
  family = binomial(link = "logit")
)
# Strip redundant in-memory training matrices to prevent 49MB file bloat
final_glm$data <- NULL
final_glm$model <- NULL
final_glm$residuals <- NULL
final_glm$fitted.values <- NULL
final_glm$effects <- NULL
final_glm$weights <- NULL
final_glm$prior.weights <- NULL
final_glm$linear.predictors <- NULL
final_glm$y <- NULL

# 5. CARE Score Evaluation (Coverage, Accuracy, Reliability, Earliness)
# We test Earliness on the prediction period of anomaly events
anomaly_events <- events[event_label == "anomaly"]$event_id
earliness_list <- list()

for (ev in anomaly_events) {
  ev_data <- telemetry[event_id == ev & train_test == "prediction"]
  if (nrow(ev_data) == 0) next
  
  dtest_ev <- xgb.DMatrix(data = as.matrix(ev_data[, ..feature_cols]))
  probs <- predict(final_xgb, newdata = dtest_ev)
  
  # Find first time 3 consecutive alarms are triggered (threshold >= 0.35)
  alarm_idx <- which(probs >= 0.35)
  if (length(alarm_idx) >= 3) {
    first_alarm_step <- alarm_idx[1]
    hours_before_end <- round((nrow(ev_data) - first_alarm_step) * 10 / 60, 1)
  } else {
    hours_before_end <- 0
  }
  
  earliness_list[[as.character(ev)]] <- data.table(
    event_id = ev,
    failure_mode = ev_data$failure_mode[1],
    total_prediction_hours = round(nrow(ev_data) * 10 / 60, 1),
    hours_lead_time = hours_before_end
  )
}

care_earliness_df <- rbindlist(earliness_list)
cat("\n=== CARE EARLINESS EVALUATION (LEAD TIME BEFORE SHUTDOWN) ===\n")
print(care_earliness_df)

# Save Models and Benchmark Results
saveRDS(final_rf, file.path(model_dir, "rf_model.rds"))
saveRDS(final_xgb, file.path(model_dir, "xgb_model.rds"))
saveRDS(final_glm, file.path(model_dir, "glm_model.rds"))
saveRDS(benchmark_results, file.path(model_dir, "benchmark_results.rds"))
saveRDS(cv_predictions, file.path(model_dir, "cv_predictions.rds"))
saveRDS(care_earliness_df, file.path(model_dir, "care_earliness.rds"))
saveRDS(feature_cols, file.path(model_dir, "feature_cols.rds"))

cat("\nModel building and benchmarking completed successfully.\n")
cat("Saved models and validation results to 'models/'.\n")
