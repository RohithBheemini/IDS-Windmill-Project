base_dir <- file.path(getwd(), "CARE_To_Compare", "CARE_To_Compare")
farms <- c("Wind Farm A", "Wind Farm B", "Wind Farm C")

for (f in farms) {
  cat(sprintf("\n================= %s FEATURE DESCRIPTION =================\n", f))
  feat_file <- file.path(base_dir, f, "feature_description.csv")
  feats <- read.csv(feat_file, sep = ";", stringsAsFactors = FALSE)
  cat(sprintf("Total features: %d\n", nrow(feats)))
  print(head(feats, 12))
  cat("\nStatistics type distribution:\n")
  print(table(feats$statistics_type))
  cat("\nAngle / Counter summary:\n")
  print(table(is_angle = feats$is_angle, is_counter = feats$is_counter))
}
