# run_app.R
# Script to launch the Wind Turbine SCADA Condition Monitoring Shiny App
message("Launching Wind Turbine Condition Monitoring & XAI Shiny App...")
message("Listening on http://127.0.0.1:3838 (Press Ctrl+C to stop)")

shiny::runApp("shiny_app", host = "127.0.0.1", port = 3838, launch.browser = FALSE)
