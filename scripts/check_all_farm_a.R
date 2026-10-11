base_dir <- file.path(getwd(), "CARE_To_Compare", "CARE_To_Compare", "Wind Farm A")
events_a <- read.csv(file.path(base_dir, "event_info.csv"), sep = ";")
cat("Wind Farm A Events:\n")
print(events_a)

cat("\nChecking row counts, missing values, and status distribution across Wind Farm A datasets:\n")
summary_list <- list()

for (i in 1:nrow(events_a)) {
  ev_id <- events_a$event_id[i]
  ev_label <- events_a$event_label[i]
  ev_desc <- events_a$event_description[i]
  fpath <- file.path(base_dir, "datasets", paste0(ev_id, ".csv"))
  
  if (!file.exists(fpath)) {
    cat(sprintf("File %s not found!\n", fpath))
    next
  }
  
  # Read with data.table for speed
  dt <- data.table::fread(fpath, sep = ";")
  n_rows <- nrow(dt)
  n_cols <- ncol(dt)
  train_rows <- sum(dt$train_test == "train")
  pred_rows <- sum(dt$train_test == "prediction")
  
  # Check NA count in numeric cols
  num_cols <- names(dt)[sapply(dt, is.numeric)]
  total_nas <- sum(is.na(dt[, ..num_cols]))
  pct_na <- round(total_nas / (n_rows * length(num_cols)) * 100, 2)
  
  # Check statuses in prediction
  pred_statuses <- paste(names(table(dt$status_type_id[dt$train_test == "prediction"])), collapse = ",")
  
  summary_list[[i]] <- data.frame(
    event_id = ev_id,
    label = ev_label,
    desc = ev_desc,
    asset = events_a$asset[i],
    total_rows = n_rows,
    train_rows = train_rows,
    pred_rows = pred_rows,
    pct_na = pct_na,
    pred_statuses = pred_statuses,
    stringsAsFactors = FALSE
  )
}

res_df <- do.call(rbind, summary_list)
print(res_df)
