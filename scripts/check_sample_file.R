base_dir <- file.path(getwd(), "CARE_To_Compare", "CARE_To_Compare")

# Let's inspect Wind Farm A
events_a <- read.csv(file.path(base_dir, "Wind Farm A", "event_info.csv"), sep = ";")
cat("=== WIND FARM A EVENTS ===\n")
print(events_a)

cat("\n=== SAMPLE DATASET 68.csv (Wind Farm A) ===\n")
f68 <- file.path(base_dir, "Wind Farm A", "datasets", "68.csv")
d68 <- read.csv(f68, sep = ";", nrows = 20)
cat(sprintf("Rows: (checking total line count)...\n"))

# Let's check distribution of train_test and status_type_id in 68.csv
df_sub <- read.csv(f68, sep = ";", colClasses = c(time_stamp="character", train_test="character", status_type_id="integer"))
cat(sprintf("Total rows in 68.csv: %d\n", nrow(df_sub)))
cat("train_test table:\n")
print(table(df_sub$train_test))
cat("status_type_id table:\n")
print(table(df_sub$status_type_id))
cat("Time stamp range:\n")
print(range(df_sub$time_stamp))
cat("Time stamp range in test:\n")
print(range(df_sub$time_stamp[df_sub$train_test == "test"]))
cat("Time stamp range in train:\n")
print(range(df_sub$time_stamp[df_sub$train_test == "train"]))

# Compare with event_info for event 68
cat("Event info for 68:\n")
print(events_a[events_a$event_id == 68, ])
