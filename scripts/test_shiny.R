# scripts/test_shiny.R
cat("Testing shiny_app/app.R compilation...\n")
source("shiny_app/app.R")
cat("Checking ui and server objects...\n")
stopifnot(!is.null(ui))
stopifnot(is.function(server))
cat("Shiny App verified successfully! UI and server are valid.\n")
