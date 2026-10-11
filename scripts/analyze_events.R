base_dir <- file.path(getwd(), "CARE_To_Compare", "CARE_To_Compare")
farms <- c("Wind Farm A", "Wind Farm B", "Wind Farm C")

cat("=== EVENT INFO DETAILS ===\n")
for (f in farms) {
  event_file <- file.path(base_dir, f, "event_info.csv")
  events <- read.csv(event_file, sep = ";")
  cat(sprintf("\n--- %s ---\n", f))
  print(head(events, 8))
  cat("\nAnomaly descriptions breakdown:\n")
  print(table(events$event_description[events$event_label == "anomaly"]))
}
