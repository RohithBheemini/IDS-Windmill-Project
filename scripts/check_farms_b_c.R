base_dir <- file.path(getwd(), "CARE_To_Compare", "CARE_To_Compare")

cat("=== CHECKING WIND FARM B ===\n")
events_b <- read.csv(file.path(base_dir, "Wind Farm B", "event_info.csv"), sep = ";")
print(head(events_b, 10))

cat("\n=== CHECKING WIND FARM C ===\n")
events_c <- read.csv(file.path(base_dir, "Wind Farm C", "event_info.csv"), sep = ";")
print(head(events_c, 10))
cat("Total events in B:", nrow(events_b), "Total events in C:", nrow(events_c), "\n")
