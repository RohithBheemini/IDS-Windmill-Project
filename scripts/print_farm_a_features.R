base_dir <- file.path(getwd(), "CARE_To_Compare", "CARE_To_Compare", "Wind Farm A")
feats <- read.csv(file.path(base_dir, "feature_description.csv"), sep = ";", stringsAsFactors = FALSE)
print(feats[, c("sensor_name", "statistics_type", "description", "unit")])
