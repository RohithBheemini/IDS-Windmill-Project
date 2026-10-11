# scripts/benchmark_models_timing.R
# Benchmarking training time, convergence, and computational budget for wind turbine models
suppressPackageStartupMessages({
  library(data.table)
  library(ranger)
  library(xgboost)
  library(pROC)
})

cat("====================================================================\n")
cat("MODEL VERIFICATION & COMPUTATIONAL BENCHMARKING REPORT\n")
cat("====================================================================\n\n")

data_dir <- file.path(getwd(), "data_clean")
telemetry <- readRDS(file.path(data_dir, "clean_telemetry.rds"))
feature_cols <- readRDS(file.path(getwd(), "models", "feature_cols.rds"))

cat(sprintf("Full Telemetry Corpus: %d rows x %d features\n", nrow(telemetry), length(feature_cols)))
cat(sprintf("Memory footprint in RAM: %.2f MB\n\n", object.size(telemetry) / 1024^2))

# Split into Train (turbines 0, 10, 11, 13) and Test (turbine 21 held out)
turbines_train <- c(0, 10, 11, 13)
test_turbine   <- 21

train_full <- telemetry[asset_id %in% turbines_train]
test_data  <- telemetry[asset_id == test_turbine]

cat(sprintf("Training Pool: %d rows (Anomalies: %d, Normal: %d)\n",
            nrow(train_full), sum(train_full$target == 1), sum(train_full$target == 0)))
cat(sprintf("Held-out Test Pool (Turbine %d): %d rows (Anomalies: %d, Normal: %d)\n\n",
            test_turbine, nrow(test_data), sum(test_data$target == 1), sum(test_data$target == 0)))

# Test 3 Training Budgets:
# 1. Fast Prototype (Subsampled 25,000 rows - 1-second training for live tuning)
# 2. Balanced Recommended (100,000 rows - ~5-10 seconds, optimal sweet spot)
# 3. Full Fleet Scale (~300,000 rows - ~25-35 seconds)

set.seed(42)
budgets <- list(
  "1_Fast_Prototype_25k" = train_full[sample(.N, min(.N, 25000))],
  "2_Recommended_Balanced_100k" = train_full[sample(.N, min(.N, 100000))],
  "3_Full_Fleet_Scale" = train_full
)

benchmark_log <- list()

for (b_name in names(budgets)) {
  dt_b <- budgets[[b_name]]
  n_rows <- nrow(dt_b)
  cat(sprintf(">>> Benchmarking Budget: %s (%d rows) <<<\n", b_name, n_rows))
  
  # A. Logistic Regression (GLM)
  t_glm <- system.time({
    glm_fit <- glm(
      formula = as.formula(paste("target ~", paste(feature_cols, collapse = " + "))),
      data = dt_b,
      family = binomial(link = "logit")
    )
  })
  pred_glm <- predict(glm_fit, newdata = test_data, type = "response")
  auc_glm <- as.numeric(auc(roc(test_data$target, pred_glm, quiet = TRUE)))
  
  # B. Random Forest (Ranger - 100 trees, 4 cores)
  t_rf <- system.time({
    rf_fit <- ranger(
      formula = as.formula(paste("target ~", paste(feature_cols, collapse = " + "))),
      data = dt_b,
      num.trees = 100,
      probability = TRUE,
      num.threads = 4,
      seed = 42
    )
  })
  pred_rf <- predict(rf_fit, data = test_data)$predictions[, 2]
  auc_rf <- as.numeric(auc(roc(test_data$target, pred_rf, quiet = TRUE)))
  
  # C. XGBoost (80 rounds)
  dtrain <- xgb.DMatrix(data = as.matrix(dt_b[, ..feature_cols]), label = dt_b$target)
  dtest  <- xgb.DMatrix(data = as.matrix(test_data[, ..feature_cols]), label = test_data$target)
  
  t_xgb <- system.time({
    xgb_fit <- xgb.train(
      params = list(
        objective = "binary:logistic",
        eval_metric = "auc",
        max_depth = 6,
        eta = 0.08,
        subsample = 0.85,
        colsample_bytree = 0.85
      ),
      data = dtrain,
      nrounds = 80,
      verbose = 0
    )
  })
  pred_xgb <- predict(xgb_fit, newdata = dtest)
  auc_xgb <- as.numeric(auc(roc(test_data$target, pred_xgb, quiet = TRUE)))
  
  benchmark_log[[b_name]] <- data.table(
    Budget = b_name,
    Sample_Size = n_rows,
    GLM_Time_Sec = round(t_glm["elapsed"], 2),
    GLM_Test_AUC = round(auc_glm, 4),
    RF_Time_Sec  = round(t_rf["elapsed"], 2),
    RF_Test_AUC  = round(auc_rf, 4),
    XGB_Time_Sec = round(t_xgb["elapsed"], 2),
    XGB_Test_AUC = round(auc_xgb, 4)
  )
}

bench_summary <- rbindlist(benchmark_log)
cat("\n====================================================================\n")
cat("BENCHMARK TIMING & ACCURACY SUMMARY TABLE\n")
cat("====================================================================\n")
print(bench_summary)

# Model Verification Checks
cat("\n====================================================================\n")
cat("MODEL VERIFICATION CHECKS ON UNSEEN TURBINE 21\n")
cat("====================================================================\n")
cat("1. Range of GLM predicted probabilities:   [", min(pred_glm, na.rm=T), ", ", max(pred_glm, na.rm=T), "]\n")
cat("2. Range of RF predicted probabilities:    [", min(pred_rf, na.rm=T), ", ", max(pred_rf, na.rm=T), "]\n")
cat("3. Range of XGB predicted probabilities:   [", min(pred_xgb, na.rm=T), ", ", max(pred_xgb, na.rm=T), "]\n")
cat("4. Any NaN or NA in predictions: GLM =", anyNA(pred_glm), ", RF =", anyNA(pred_rf), ", XGB =", anyNA(pred_xgb), "\n")
cat("5. Mean risk score for actual Anomaly events: GLM =", round(mean(pred_glm[test_data$target==1]), 4),
    ", RF =", round(mean(pred_rf[test_data$target==1]), 4),
    ", XGB =", round(mean(pred_xgb[test_data$target==1]), 4), "\n")
cat("6. Mean risk score for actual Healthy normal: GLM =", round(mean(pred_glm[test_data$target==0]), 4),
    ", RF =", round(mean(pred_rf[test_data$target==0]), 4),
    ", XGB =", round(mean(pred_xgb[test_data$target==0]), 4), "\n")

saveRDS(bench_summary, file.path(getwd(), "models", "bench_training_times.rds"))
cat("\nBenchmarking complete. Saved results to 'models/bench_training_times.rds'.\n")
