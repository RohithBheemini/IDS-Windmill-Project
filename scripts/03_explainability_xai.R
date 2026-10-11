# scripts/03_explainability_xai.R
# Explainable AI (XAI) using exact TreeSHAP and LIME for Black-Box Model Interpretability
suppressPackageStartupMessages({
  library(data.table)
  library(xgboost)
  library(ranger)
  library(lime)
  library(ggplot2)
})

cat("========================================================\n")
cat("STEP 3: EXPLAINABLE AI (SHAP & LIME) INDUSTRIAL AUDIT\n")
cat("========================================================\n\n")

data_dir  <- file.path(getwd(), "data_clean")
model_dir <- file.path(getwd(), "models")

# 1. Load Telemetry, Events, and Production Models
telemetry    <- readRDS(file.path(data_dir, "clean_telemetry.rds"))
events       <- readRDS(file.path(data_dir, "clean_events.rds"))
final_xgb    <- readRDS(file.path(model_dir, "xgb_model.rds"))
feature_cols <- readRDS(file.path(model_dir, "feature_cols.rds"))

cat(sprintf("Loaded models and features (%d features).\n", length(feature_cols)))

# 2. Global SHAP Feature Importance via TreeSHAP
cat("Computing Exact TreeSHAP Contributions on Evaluation Telemetry...\n")

# Sample 5,000 observations representing diverse operating regimes
set.seed(42)
eval_sample <- telemetry[sample(.N, min(.N, 5000))]
dmat_sample <- xgb.DMatrix(data = as.matrix(eval_sample[, ..feature_cols]))

# Exact Shapley values: columns 1..P are features, column P+1 is the base margin (bias)
shap_contribs <- predict(final_xgb, newdata = dmat_sample, predcontrib = TRUE)
shap_values   <- shap_contribs[, 1:length(feature_cols)]
colnames(shap_values) <- feature_cols

# Mean absolute SHAP value (Global Importance)
mean_abs_shap <- colMeans(abs(shap_values))
global_shap_dt <- data.table(
  feature = names(mean_abs_shap),
  mean_abs_shap = mean_abs_shap
)[order(-mean_abs_shap)]

cat("\nTop 12 Global SHAP Features:\n")
print(head(global_shap_dt, 12))

# 3. Local SHAP Attribution for Specific Failure Modes
cat("\nExtracting Local SHAP Attributions for Benchmark Events...\n")

target_events <- c(
  "Gearbox"           = 72,
  "Generator Bearing" = 0,
  "Transformer"       = 68,
  "Hydraulic Group"   = 22,
  "Normal Control"    = 25
)

local_shap_list <- list()

for (mode in names(target_events)) {
  ev_id <- target_events[mode]
  ev_slice <- telemetry[event_id == ev_id & train_test == "prediction"]
  if (nrow(ev_slice) == 0) next
  
  # Take median operational state during prediction period
  mid_idx <- max(1, floor(nrow(ev_slice) / 2))
  sample_row <- ev_slice[mid_idx]
  
  dmat_row <- xgb.DMatrix(data = as.matrix(sample_row[, ..feature_cols]))
  row_contrib <- predict(final_xgb, newdata = dmat_row, predcontrib = TRUE)[1, ]
  
  base_val <- row_contrib[length(row_contrib)]
  feat_shap <- row_contrib[1:length(feature_cols)]
  names(feat_shap) <- feature_cols
  
  # Sort by absolute impact
  top_local <- data.table(
    failure_mode = mode,
    event_id = ev_id,
    feature = names(feat_shap),
    actual_value = as.numeric(sample_row[, ..feature_cols][1]),
    shap_value = feat_shap,
    abs_shap = abs(feat_shap)
  )[order(-abs_shap)]
  
  local_shap_list[[mode]] <- top_local
  cat(sprintf("\n--- Top Attributions for Event %d (%s) ---\n", ev_id, mode))
  print(head(top_local[, .(feature, actual_value = round(actual_value, 2), shap_value = round(shap_value, 4))], 5))
}

# 4. LIME Local Explanations using the 'lime' package
cat("\n========================================================\n")
cat("Fitting Local Interpretable Model-agnostic Explanations (LIME)...\n")

# Prepare reference training distribution for LIME
lime_train <- as.data.frame(eval_sample[target == 0, ..feature_cols])

# Custom predictor wrapper for lime
model_wrapper <- list(
  predict = function(model, newdata) {
    dmat <- xgb.DMatrix(data = as.matrix(newdata))
    probs <- predict(model, newdata = dmat)
    data.frame(Normal = 1 - probs, Anomaly = probs)
  }
)
class(model_wrapper) <- "custom_model"

predict_model.custom_model <- function(x, newdata, type, ...) {
  x$predict(final_xgb, newdata)
}
model_type.custom_model <- function(x, ...) "classification"

explainer <- lime(
  x = lime_train,
  model = model_wrapper,
  bin_continuous = TRUE,
  n_bins = 4
)

# Prepare test cases for LIME
test_cases_list <- list()
for (mode in names(target_events)) {
  ev_id <- target_events[mode]
  ev_slice <- telemetry[event_id == ev_id & train_test == "prediction"]
  if (nrow(ev_slice) == 0) next
  mid_idx <- max(1, floor(nrow(ev_slice) / 2))
  test_cases_list[[mode]] <- as.data.frame(ev_slice[mid_idx, ..feature_cols])
}
test_cases_df <- do.call(rbind, test_cases_list)
rownames(test_cases_df) <- names(target_events)

# Run LIME explanations
lime_explanation <- explain(
  x = test_cases_df,
  explainer = explainer,
  labels = "Anomaly",
  n_features = 5
)

cat("LIME Explanations Generated:\n")
lime_dt <- as.data.table(lime_explanation)
print(lime_dt[, .(case, feature, feature_weight = round(feature_weight, 4), feature_desc)])

# 5. Save XAI Artifacts for Shiny Application
saveRDS(global_shap_dt, file.path(model_dir, "xai_global_shap.rds"))
saveRDS(local_shap_list, file.path(model_dir, "xai_local_shap.rds"))
saveRDS(lime_dt, file.path(model_dir, "xai_lime_results.rds"))

cat("\nExplainable AI (SHAP & LIME) pipeline finished successfully.\n")
cat("Artifacts saved to 'models/'.\n")
