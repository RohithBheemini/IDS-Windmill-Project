cat("Starting inspection...\n")
base_dir <- file.path(getwd(), "CARE_To_Compare", "CARE_To_Compare")
farms <- c("Wind Farm A", "Wind Farm B", "Wind Farm C")

for (f in farms) {
  p <- file.path(base_dir, f)
  event_file <- file.path(p, "event_info.csv")
  feat_file <- file.path(p, "feature_description.csv")
  data_dir <- file.path(p, "datasets")
  
  events <- read.csv(event_file, sep = ";")
  features <- read.csv(feat_file, sep = ";")
  data_files <- list.files(data_dir, pattern = "\\.csv$")
  
  cat("=========================================\n")
  cat(sprintf("Wind Farm: %s\n", f))
  cat(sprintf("Number of events: %d\n", nrow(events)))
  cat("Event label counts:\n")
  print(table(events$event_label))
  cat(sprintf("Number of features in description: %d\n", nrow(features)))
  cat(sprintf("Number of CSV datasets: %d\n", length(data_files)))
  
  # Inspect first dataset file size and columns
  if (length(data_files) > 0) {
    first_file <- file.path(data_dir, data_files[1])
    cat(sprintf("Sample dataset: %s (Size: %.2f MB)\n", data_files[1], file.info(first_file)$size / 1024^2))
    
    # Read first few lines
    sample_df <- read.csv(first_file, sep = ";", nrows = 5)
    cat(sprintf("Sample columns count: %d\n", ncol(sample_df)))
    cat("Sample column names (first 10):", paste(head(names(sample_df), 10), collapse = ", "), "\n")
  }
}
cat("Inspection complete.\n")
