library(data.table)

base_dir <- file.path(getwd(), "CARE_To_Compare", "CARE_To_Compare", "Wind Farm A")
events <- fread(file.path(base_dir, "event_info.csv"), sep = ";")
feats <- fread(file.path(base_dir, "feature_description.csv"), sep = ";")

cat("Analyzing all 22 dataset files in Wind Farm A...\n")

all_checks <- list()

for (i in 1:nrow(events)) {
  ev_id <- events$event_id[i]
  fpath <- file.path(base_dir, "datasets", paste0(ev_id, ".csv"))
  dt <- fread(fpath, sep = ";")
  
  # Check numeric columns
  num_cols <- names(dt)[sapply(dt, is.numeric)]
  
  na_count <- sum(is.na(dt[, ..num_cols]))
  inf_count <- sum(sapply(dt[, ..num_cols], function(x) sum(is.infinite(x))))
  
  train_count <- sum(dt$train_test == "train")
  pred_count <- sum(dt$train_test == "prediction")
  
  # Check negative wind speeds
  neg_wind <- sum(dt$wind_speed_3_avg < 0, na.rm = TRUE)
  
  # Check extreme pitch angles (outside [-10, 100])
  ext_pitch <- sum(dt$sensor_5_avg < -10 | dt$sensor_5_avg > 100, na.rm = TRUE)
  
  all_checks[[i]] <- data.table(
    event_id = ev_id,
    label = events$event_label[i],
    desc = events$event_description[i],
    asset_id = events$asset[i],
    total_rows = nrow(dt),
    train_rows = train_count,
    pred_rows = pred_count,
    na_count = na_count,
    inf_count = inf_count,
    neg_wind = neg_wind,
    ext_pitch = ext_pitch,
    min_date = min(dt$time_stamp),
    max_date = max(dt$time_stamp)
  )
}

res <- rbindlist(all_checks)
print(res)
cat("\nTotal rows across Wind Farm A:", sum(res$total_rows), "\n")
cat("Total NAs:", sum(res$na_count), "Total Infs:", sum(res$inf_count), "\n")
