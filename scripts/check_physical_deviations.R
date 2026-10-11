base_dir <- file.path(getwd(), "CARE_To_Compare", "CARE_To_Compare", "Wind Farm A", "datasets")

# Event 72: Gearbox failure
d72 <- data.table::fread(file.path(base_dir, "72.csv"), sep = ";")
cat("=== Event 72 (Gearbox failure) ===\n")
cat("Prediction rows count:", sum(d72$train_test == "prediction"), "\n")
cat("Summary of gearbox bearing temp (sensor_11_avg):\n")
cat("Train mean:", mean(d72[train_test == "train", sensor_11_avg], na.rm = TRUE), 
    "max:", max(d72[train_test == "train", sensor_11_avg], na.rm = TRUE), "\n")
cat("Prediction mean:", mean(d72[train_test == "prediction", sensor_11_avg], na.rm = TRUE), 
    "max:", max(d72[train_test == "prediction", sensor_11_avg], na.rm = TRUE), "\n")

cat("\n=== Event 68 (Transformer failure) ===\n")
d68 <- data.table::fread(file.path(base_dir, "68.csv"), sep = ";")
cat("Transformer L1 temp (sensor_39_avg):\n")
cat("Train mean:", mean(d68[train_test == "train", sensor_39_avg], na.rm = TRUE), 
    "max:", max(d68[train_test == "train", sensor_39_avg], na.rm = TRUE), "\n")
cat("Prediction mean:", mean(d68[train_test == "prediction", sensor_39_avg], na.rm = TRUE), 
    "max:", max(d68[train_test == "prediction", sensor_39_avg], na.rm = TRUE), "\n")

cat("\n=== Event 0 (Generator bearing failure) ===\n")
d0 <- data.table::fread(file.path(base_dir, "0.csv"), sep = ";")
cat("Generator bearing DE temp (sensor_13_avg):\n")
cat("Train mean:", mean(d0[train_test == "train", sensor_13_avg], na.rm = TRUE), 
    "max:", max(d0[train_test == "train", sensor_13_avg], na.rm = TRUE), "\n")
cat("Prediction mean:", mean(d0[train_test == "prediction", sensor_13_avg], na.rm = TRUE), 
    "max:", max(d0[train_test == "prediction", sensor_13_avg], na.rm = TRUE), "\n")

cat("\n=== Event 25 (Normal control) ===\n")
d25 <- data.table::fread(file.path(base_dir, "25.csv"), sep = ";")
cat("Train mean sensor_11:", mean(d25[train_test == "train", sensor_11_avg], na.rm = TRUE),
    "Pred mean sensor_11:", mean(d25[train_test == "prediction", sensor_11_avg], na.rm = TRUE), "\n")
cat("Train mean sensor_13:", mean(d25[train_test == "train", sensor_13_avg], na.rm = TRUE),
    "Pred mean sensor_13:", mean(d25[train_test == "prediction", sensor_13_avg], na.rm = TRUE), "\n")
