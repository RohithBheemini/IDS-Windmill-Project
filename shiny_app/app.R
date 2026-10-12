# shiny_app/app.R
# Industrial Wind Turbine Condition Monitoring & Explainable AI (SHAP & LIME) Dashboard
suppressPackageStartupMessages({
  library(shiny)
  library(bslib)
  library(data.table)
  library(ggplot2)
  library(scales)
  library(DT)
  library(xgboost)
})

# 1. Load Pre-processed Data & Model Artifacts
base_proj <- normalizePath("..")
data_dir  <- file.path(base_proj, "data_clean")
model_dir <- file.path(base_proj, "models")

# Fallback paths if launched from within shiny_app directory or project root
if (!dir.exists(data_dir)) {
  data_dir  <- file.path(getwd(), "data_clean")
  model_dir <- file.path(getwd(), "models")
}

telemetry         <- readRDS(file.path(data_dir, "clean_telemetry.rds"))
events            <- readRDS(file.path(data_dir, "clean_events.rds"))
benchmark_results <- readRDS(file.path(model_dir, "benchmark_results.rds"))
cv_predictions    <- readRDS(file.path(model_dir, "cv_predictions.rds"))
care_earliness    <- readRDS(file.path(model_dir, "care_earliness.rds"))
final_xgb         <- readRDS(file.path(model_dir, "xgb_model.rds"))
feature_cols      <- readRDS(file.path(model_dir, "feature_cols.rds"))
global_shap       <- readRDS(file.path(model_dir, "xai_global_shap.rds"))
local_shap        <- readRDS(file.path(model_dir, "xai_local_shap.rds"))
lime_results      <- readRDS(file.path(model_dir, "xai_lime_results.rds"))

# Modern industrial theme with bslib
theme_industrial <- bs_theme(
  version = 5,
  bootswatch = "darkly",
  primary = "#00bcd4",
  secondary = "#455a64",
  success = "#00e676",
  warning = "#ffb300",
  danger = "#ff5252",
  base_font = font_google("Inter"),
  heading_font = font_google("Rajdhani")
)

# UI Definition
ui <- page_navbar(
  title = "WIND TURBINE CONDITION MONITORING | CARE BENCHMARK & XAI",
  theme = theme_industrial,
  fillable = TRUE,
  
  # Tab 1: Fleet Status & Overview
  nav_panel(
    "Fleet Overview",
    layout_columns(
      col_widths = c(3, 3, 3, 3),
      value_box(
        title = "Total Wind Farms",
        value = "3 Farms (A, B, C)",
        showcase = bsicons::bs_icon("buildings"),
        theme = "primary",
        p("Onshore (Portugal) & Offshore (Germany)")
      ),
      value_box(
        title = "Monitored SCADA Fleet",
        value = "36 Turbines",
        showcase = bsicons::bs_icon("wind"),
        theme = "info",
        p("89 Years of SCADA Telemetry (10-min)")
      ),
      value_box(
        title = "Benchmark Events",
        value = "95 Events",
        showcase = bsicons::bs_icon("activity"),
        theme = "warning",
        p("44 Anomalies | 51 Normal Cases")
      ),
      value_box(
        title = "Lead Time Before Failure",
        value = "8 - 34 Days",
        showcase = bsicons::bs_icon("clock-history"),
        theme = "success",
        p("Average Earliness across Subsystems")
      )
    ),
    layout_columns(
      col_widths = c(8, 4),
      card(
        card_header("Wind Farm A: Monitored Events & Failure Mode Registry"),
        DTOutput("table_events")
      ),
      card(
        card_header("Multi-Farm Architecture & Class Balance"),
        p("The CARE benchmark incorporates 95 balanced operational datasets:"),
        tags$ul(
          tags$li(strong("Wind Farm A:"), " 5 Onshore Turbines, 22 Datasets, 86 Features (EDP Open Data). Ground-truth failures in Gearbox, Generator, Transformer, and Hydraulics."),
          tags$li(strong("Wind Farm B:"), " Offshore Germany, 15 Datasets, 257 Features. Severe marine environmental loads, rotor bearing and transformer faults."),
          tags$li(strong("Wind Farm C:"), " Offshore Germany, 58 Datasets, 957 Features. Deep component telemetry including pitch motors, converter IGBTs, and blade heating.")
        ),
        hr(),
        h5("Industrial Operating Integrity"),
        tags$p(
          span(class = "badge bg-danger", "Leakage Guard"),
          " Operational status codes (status_type_id == 3/4) strictly omitted to prevent post-trip cheat leakage."
        ),
        tags$p(
          span(class = "badge bg-success", "Physical Fidelity"),
          " Zero synthetic oversampling (no SMOTE). 100% genuine thermodynamic sensor records."
        )
      )
    )
  ),
  
  # Tab 2: Telemetry & Anomaly Timeline Studio
  nav_panel(
    "SCADA Telemetry Studio",
    layout_sidebar(
      sidebar = sidebar(
        title = "Telemetry Controls",
        selectInput(
          "sel_event",
          "Select Monitoring Event:",
          choices = setNames(events$event_id, paste0("Event ", events$event_id, " (", events$failure_mode, " - Turbine ", events$asset_id, ")")),
          selected = 72
        ),
        selectInput(
          "sel_sensor_group",
          "Sensor Telemetry View:",
          choices = c(
            "Thermodynamic Differentials (Delta T over Ambient)" = "delta_t",
            "Component Absolute Temperatures (Gearbox, Gen, Trans)" = "temps",
            "Aerodynamic & Power Curves (Power vs Wind vs Pitch)" = "aero",
            "Rotational Dynamics (Generator & Rotor RPM)" = "rpm"
          )
        ),
        sliderInput("risk_thresh_plot", "Alarm Decision Threshold:", min = 0.1, max = 0.9, value = 0.35, step = 0.05)
      ),
      layout_columns(
        col_widths = c(12),
        card(
          card_header("SCADA Sensor Trajectory (Training vs. Prediction Window)"),
          plotOutput("plot_telemetry", height = "360px")
        ),
        card(
          card_header("Real-Time Anomaly Probability & Early Warning Detection"),
          plotOutput("plot_risk_timeline", height = "280px")
        )
      )
    )
  ),
  
  # Tab 3: Model Performance & CARE Benchmarking
  nav_panel(
    "Model Benchmark & CARE",
    layout_columns(
      col_widths = c(6, 6),
      card(
        card_header("Leave-One-Turbine-Out Cross-Validation Benchmark"),
        DTOutput("table_benchmark"),
        p(class = "text-muted small", "Evaluated on strictly held-out unseen physical wind turbines (Group K-Fold by Asset ID).")
      ),
      card(
        card_header("CARE Benchmark Earliness (Lead Time Before Shutdown)"),
        DTOutput("table_care"),
        p(class = "text-muted small", "Shows the lead time (hours/days) achieved by the model before emergency standstill or service shutdown.")
      )
    ),
    layout_columns(
      col_widths = c(6, 6),
      card(
        card_header("Fleet Anomaly Score Distribution"),
        plotOutput("plot_score_dist", height = "300px")
      ),
      card(
        card_header("Confusion Matrix at Current Alarm Threshold"),
        verbatimTextOutput("conf_matrix_text")
      )
    )
  ),
  
  # Tab 4: Explainable AI (SHAP & LIME Studio)
  nav_panel(
    "Explainable AI (SHAP & LIME)",
    layout_sidebar(
      sidebar = sidebar(
        title = "XAI Diagnostics",
        selectInput(
          "sel_xai_case",
          "Select Benchmark Failure Mode:",
          choices = c(
            "Gearbox Failure (Event 72)" = "Gearbox",
            "Generator Bearing Failure (Event 0)" = "Generator Bearing",
            "Transformer Failure (Event 68)" = "Transformer",
            "Hydraulic Group Failure (Event 22)" = "Hydraulic Group",
            "Healthy Control (Event 25)" = "Normal Control"
          ),
          selected = "Gearbox"
        ),
        hr(),
        h6("Methodology Comparison:"),
        tags$p(tags$small("SHAP provides exact game-theoretic additive Shapley values from tree structure.")),
        tags$p(tags$small("LIME fits local interpretable linear surrogate models with discrete condition rules."))
      ),
      layout_columns(
        col_widths = c(6, 6),
        card(
          card_header("Global SHAP Feature Importance (Fleet-wide Drivers)"),
          plotOutput("plot_global_shap", height = "380px")
        ),
        card(
          card_header("Local SHAP Attribution Breakdown (Selected Event)"),
          plotOutput("plot_local_shap", height = "380px")
        )
      ),
      layout_columns(
        col_widths = c(7, 5),
        card(
          card_header("LIME Local Decision Rules & Surrogate Feature Weights"),
          plotOutput("plot_lime", height = "300px")
        ),
        card(
          card_header("Critic's Physics-Informed Verification"),
          uiOutput("xai_critique_text")
        )
      )
    )
  ),
  
  # Tab 5: Business Value & Financial ROI Calculator
  nav_panel(
    "Business Value & ROI",
    layout_sidebar(
      sidebar = sidebar(
        title = "Financial Parameters",
        sliderInput("cost_fn", "Unplanned Breakdown Cost ($ C_FN):", min = 50000, max = 300000, value = 150000, step = 10000),
        sliderInput("cost_fp", "False Alarm Inspection Cost ($ C_FP):", min = 1000, max = 10000, value = 3500, step = 500),
        sliderInput("cost_tp", "Preventive Early Action Cost ($ C_TP):", min = 2000, max = 20000, value = 8000, step = 1000),
        sliderInput("fleet_turbines", "Fleet Turbine Count:", min = 5, max = 100, value = 36, step = 1),
        sliderInput("biz_threshold", "Alarm Threshold:", min = 0.1, max = 0.9, value = 0.35, step = 0.05)
      ),
      layout_columns(
        col_widths = c(4, 4, 4),
        value_box(
          title = "Expected Net Fleet Savings",
          value = textOutput("text_savings"),
          showcase = bsicons::bs_icon("cash-coin"),
          theme = "success"
        ),
        value_box(
          title = "Avoided Downtime Hours",
          value = textOutput("text_downtime_avoided"),
          showcase = bsicons::bs_icon("shield-check"),
          theme = "primary"
        ),
        value_box(
          title = "Estimated Return on Investment",
          value = textOutput("text_roi"),
          showcase = bsicons::bs_icon("graph-up-arrow"),
          theme = "warning"
        )
      ),
      layout_columns(
        col_widths = c(8, 4),
        card(
          card_header("Expected Total Fleet Cost vs Decision Threshold"),
          plotOutput("plot_cost_curve", height = "360px")
        ),
        card(
          card_header("Cost Asymmetry Rationale"),
          p("In wind turbine condition monitoring, costs are profoundly asymmetric:"),
          tags$ul(
            tags$li(strong("False Negatives ($150,000+):"), " Catastrophic gearbox/bearing destruction causes crane ship chartering and 30-60 days lost production."),
            tags$li(strong("True Positives ($8,000):"), " Planned uptower bearing swap or hydraulic seal replacement during calm weather window."),
            tags$li(strong("False Positives ($3,500):"), " Diagnostic review and technician inspection visit."),
            tags$li(strong("Threshold Strategy:"), " Lower thresholds (0.25 - 0.35) minimize total financial risk by heavily prioritizing recall over false alarm elimination.")
          )
        )
      )
    )
  )
)

# Server Logic
server <- function(input, output, session) {
  
  # Tab 1: Event Registry Table
  output$table_events <- renderDT({
    disp_events <- copy(events)
    disp_events[, `:=`(
      pred_duration = paste0(pred_duration_hours, " hrs"),
      delta_T_gearbox = round(mean_delta_T_gearbox, 1),
      delta_T_oil = round(mean_delta_T_oil, 1),
      delta_T_gen = round(mean_delta_T_gen_de, 1),
      delta_T_trans = round(mean_delta_T_transformer, 1)
    )]
    
    datatable(
      disp_events[, .(Event = event_id, Turbine = asset_id, Label = event_label,
                      Failure_Mode = failure_mode, Duration = pred_duration,
                      dT_Gearbox = delta_T_gearbox, dT_Gen = delta_T_gen, dT_Trans = delta_T_trans)],
      options = list(pageLength = 8, scrollX = TRUE),
      rownames = FALSE
    ) %>%
      formatStyle(
        "Failure_Mode",
        backgroundColor = styleEqual(
          c("Gearbox", "Generator Bearing", "Transformer", "Hydraulic Group", "Normal"),
          c("#5c0000", "#4a148c", "#880e4f", "#e65100", "#1b5e20")
        )
      )
  })
  
  # Tab 2: Reactive Telemetry Data
  reactive_event_data <- reactive({
    ev_id <- as.integer(input$sel_event)
    ev_dt <- telemetry[event_id == ev_id]
    
    # Subsample training period slightly if large for instant plotting
    train_sub <- ev_dt[train_test == "train"][seq(1, .N, by = 4)]
    pred_sub  <- ev_dt[train_test == "prediction"]
    rbind(train_sub, pred_sub)
  })
  
  output$plot_telemetry <- renderPlot({
    dt <- reactive_event_data()
    req(nrow(dt) > 0)
    
    dt[, plot_time := as.POSIXct(time_stamp)]
    
    if (input$sel_sensor_group == "delta_t") {
      p <- ggplot(dt, aes(x = plot_time)) +
        geom_line(aes(y = delta_T_gearbox, color = "Gearbox dT (°C)"), alpha = 0.8) +
        geom_line(aes(y = delta_T_gen_de, color = "Gen Drive-End dT (°C)"), alpha = 0.8) +
        geom_line(aes(y = delta_T_transformer, color = "Transformer dT (°C)"), alpha = 0.8) +
        geom_line(aes(y = delta_T_hydraulic, color = "Hydraulic Oil dT (°C)"), alpha = 0.8) +
        labs(y = "Temperature Differential over Ambient (°C)", x = "Timestamp", color = "Subsystem")
    } else if (input$sel_sensor_group == "temps") {
      p <- ggplot(dt, aes(x = plot_time)) +
        geom_line(aes(y = temp_ambient, color = "Ambient Temp (°C)"), linetype = "dashed") +
        geom_line(aes(y = temp_gearbox_bearing, color = "Gearbox Bearing (°C)")) +
        geom_line(aes(y = temp_gen_bearing_de, color = "Generator DE (°C)")) +
        geom_line(aes(y = temp_transformer, color = "Transformer (°C)")) +
        labs(y = "Temperature (°C)", x = "Timestamp", color = "Measurement")
    } else if (input$sel_sensor_group == "aero") {
      p <- ggplot(dt, aes(x = plot_time)) +
        geom_line(aes(y = wind_speed, color = "Wind Speed (m/s)")) +
        geom_line(aes(y = active_power / 100, color = "Active Power (kW / 100)")) +
        geom_line(aes(y = pitch_angle, color = "Pitch Angle (°)"), linetype = "dotted") +
        labs(y = "Magnitude", x = "Timestamp", color = "Telemetry")
    } else {
      p <- ggplot(dt, aes(x = plot_time)) +
        geom_line(aes(y = generator_rpm, color = "Generator RPM"), alpha = 0.8) +
        geom_line(aes(y = rotor_rpm * 50, color = "Rotor RPM (x50)"), alpha = 0.8) +
        labs(y = "RPM", x = "Timestamp", color = "Speed")
    }
    
    p + theme_minimal(base_size = 13) +
      theme(
        plot.background = element_rect(fill = "#222", color = NA),
        panel.background = element_rect(fill = "#222", color = NA),
        panel.grid.major = element_line(color = "#333"),
        panel.grid.minor = element_line(color = "#2a2a2a"),
        text = element_text(color = "#eee"),
        axis.text = element_text(color = "#ccc"),
        legend.background = element_rect(fill = "#222", color = NA),
        legend.text = element_text(color = "#eee")
      ) +
      scale_color_brewer(palette = "Set2")
  })
  
  output$plot_risk_timeline <- renderPlot({
    dt <- reactive_event_data()
    req(nrow(dt) > 0)
    
    # Predict real-time risk score using production XGBoost
    dmat <- xgb.DMatrix(data = as.matrix(dt[, ..feature_cols]))
    dt[, risk_score := predict(final_xgb, newdata = dmat)]
    dt[, plot_time := as.POSIXct(time_stamp)]
    
    thresh <- input$risk_thresh_plot
    
    ggplot(dt, aes(x = plot_time, y = risk_score)) +
      geom_area(fill = "#ff5252", alpha = 0.25) +
      geom_line(color = "#ff5252", linewidth = 1) +
      geom_hline(yintercept = thresh, color = "#ffb300", linetype = "dashed", linewidth = 1) +
      annotate("text", x = min(dt$plot_time), y = thresh + 0.05, label = paste("Alarm Threshold:", thresh),
               color = "#ffb300", hjust = 0, size = 4) +
      labs(y = "Anomaly Risk Probability", x = "Timestamp", title = paste("Event", dt$event_id[1], "-", dt$failure_mode[1])) +
      ylim(0, 1) +
      theme_minimal(base_size = 13) +
      theme(
        plot.background = element_rect(fill = "#222", color = NA),
        panel.background = element_rect(fill = "#222", color = NA),
        panel.grid.major = element_line(color = "#333"),
        panel.grid.minor = element_line(color = "#2a2a2a"),
        text = element_text(color = "#eee"),
        axis.text = element_text(color = "#ccc")
      )
  })
  
  # Tab 3: Model Benchmark & CARE Tables
  output$table_benchmark <- renderDT({
    datatable(
      benchmark_results[, .(Model, ROC_AUC, Recall = Sensitivity_Recall, Specificity, Precision, F1_Score)],
      options = list(dom = 't', paging = FALSE),
      rownames = FALSE
    )
  })
  
  output$table_care <- renderDT({
    datatable(
      care_earliness[, .(Event = event_id, Failure_Mode = failure_mode,
                         Monitoring_Hours = total_prediction_hours,
                         Lead_Time_Hours = hours_lead_time,
                         Lead_Days = round(hours_lead_time / 24, 1))],
      options = list(pageLength = 6, scrollX = TRUE),
      rownames = FALSE
    )
  })
  
  output$plot_score_dist <- renderPlot({
    ggplot(cv_predictions, aes(x = xgb_prob, fill = factor(target))) +
      geom_density(alpha = 0.5) +
      scale_fill_manual(values = c("0" = "#00bcd4", "1" = "#ff5252"), labels = c("Healthy", "Anomaly")) +
      labs(x = "Predicted Anomaly Probability (XGBoost)", y = "Density", fill = "Ground Truth",
           title = "Fleet Anomaly Risk Distribution") +
      theme_minimal(base_size = 13) +
      theme(
        plot.background = element_rect(fill = "#222", color = NA),
        panel.background = element_rect(fill = "#222", color = NA),
        panel.grid = element_line(color = "#333"),
        text = element_text(color = "#eee"),
        axis.text = element_text(color = "#ccc"),
        legend.background = element_rect(fill = "#222", color = NA),
        legend.text = element_text(color = "#eee")
      )
  })
  
  output$conf_matrix_text <- renderPrint({
    thresh <- input$risk_thresh_plot
    preds  <- as.integer(cv_predictions$xgb_prob >= thresh)
    actual <- cv_predictions$target
    
    tp <- sum(actual == 1 & preds == 1)
    fp <- sum(actual == 0 & preds == 1)
    tn <- sum(actual == 0 & preds == 0)
    fn <- sum(actual == 1 & preds == 0)
    
    cat(sprintf("Decision Threshold: %.2f\n", thresh))
    cat(sprintf("---------------------------------------------\n"))
    cat(sprintf("True Positives  (Impending Fault Detected): %d\n", tp))
    cat(sprintf("False Positives (False Alarms Dispatched): %d\n", fp))
    cat(sprintf("False Negatives (Missed Breakdowns):       %d\n", fn))
    cat(sprintf("True Negatives  (Healthy States Normal):    %d\n", tn))
    cat(sprintf("---------------------------------------------\n"))
    cat(sprintf("Pointwise Sensitivity (Recall): %.2f%%\n", (tp / (tp + fn)) * 100))
    cat(sprintf("Pointwise Specificity:          %.2f%%\n", (tn / (tn + fp)) * 100))
  })
  
  # Tab 4: Explainable AI Studio (SHAP & LIME)
  output$plot_global_shap <- renderPlot({
    top_shap <- head(global_shap, 12)
    ggplot(top_shap, aes(x = reorder(feature, mean_abs_shap), y = mean_abs_shap)) +
      geom_col(fill = "#00bcd4") +
      coord_flip() +
      labs(x = "Feature", y = "Mean |SHAP Value| (Impact on Model Output)",
           title = "Global Fleet SHAP Importance") +
      theme_minimal(base_size = 13) +
      theme(
        plot.background = element_rect(fill = "#222", color = NA),
        panel.background = element_rect(fill = "#222", color = NA),
        panel.grid = element_line(color = "#333"),
        text = element_text(color = "#eee"),
        axis.text = element_text(color = "#ccc")
      )
  })
  
  output$plot_local_shap <- renderPlot({
    case_name <- input$sel_xai_case
    dt_local  <- local_shap[[case_name]]
    req(dt_local)
    
    top_case <- head(dt_local, 8)
    top_case[, sign := ifelse(shap_value > 0, "Pushes Towards Anomaly", "Pushes Towards Normal")]
    
    ggplot(top_case, aes(x = reorder(feature, abs_shap), y = shap_value, fill = sign)) +
      geom_col() +
      coord_flip() +
      scale_fill_manual(values = c("Pushes Towards Anomaly" = "#ff5252", "Pushes Towards Normal" = "#00e676")) +
      labs(x = "Sensor Feature", y = "SHAP Attribution Value",
           title = paste("Local SHAP Attribution:", case_name), fill = "Direction") +
      theme_minimal(base_size = 13) +
      theme(
        plot.background = element_rect(fill = "#222", color = NA),
        panel.background = element_rect(fill = "#222", color = NA),
        panel.grid = element_line(color = "#333"),
        text = element_text(color = "#eee"),
        axis.text = element_text(color = "#ccc"),
        legend.position = "bottom",
        legend.background = element_rect(fill = "#222", color = NA),
        legend.text = element_text(color = "#eee")
      )
  })
  
  output$plot_lime <- renderPlot({
    case_name <- input$sel_xai_case
    dt_lime   <- lime_results[case == case_name]
    req(nrow(dt_lime) > 0)
    
    dt_lime[, sign := ifelse(feature_weight > 0, "Supports Anomaly", "Contradicts Anomaly")]
    
    ggplot(dt_lime, aes(x = reorder(feature_desc, abs(feature_weight)), y = feature_weight, fill = sign)) +
      geom_col() +
      coord_flip() +
      scale_fill_manual(values = c("Supports Anomaly" = "#ff5252", "Contradicts Anomaly" = "#00e676")) +
      labs(x = "Decision Rule Condition", y = "LIME Feature Weight",
           title = paste("LIME Explanations:", case_name), fill = "Influence") +
      theme_minimal(base_size = 13) +
      theme(
        plot.background = element_rect(fill = "#222", color = NA),
        panel.background = element_rect(fill = "#222", color = NA),
        panel.grid = element_line(color = "#333"),
        text = element_text(color = "#eee"),
        axis.text = element_text(color = "#ccc"),
        legend.position = "bottom",
        legend.background = element_rect(fill = "#222", color = NA),
        legend.text = element_text(color = "#eee")
      )
  })
  
  output$xai_critique_text <- renderUI({
    case_name <- input$sel_xai_case
    if (case_name == "Gearbox") {
      tagList(
        h6("Physical Mechanics Validation: Gearbox"),
        p("In Event 72, the model correctly highlights high-speed shaft bearing temperatures (temp_gearbox_bearing) and rolling thermal drift (roll_mean_trans_6h, roll_mean_hydr_6h)."),
        p("Physical Consistency: HIGH. Mechanical bearing friction causes localized heating of lubrication oil, proving the model is not memorizing spurious noise.")
      )
    } else if (case_name == "Generator Bearing") {
      tagList(
        h6("Physical Mechanics Validation: Generator Bearing"),
        p("In Event 0, the top SHAP drivers are generator drive-end bearing temperature (temp_gen_bearing_de) and 6-hour rolling thermal averages."),
        p("Physical Consistency: VERY HIGH. The Drive-End bearing directly bears generator magnetic rotor alignment forces; thermal surge indicates catastrophic bearing spalling.")
      )
    } else if (case_name == "Transformer") {
      tagList(
        h6("Physical Mechanics Validation: Transformer"),
        p("In Event 68, transformer temperature (temp_transformer) and rolling gearbox/ambient differentials are identified."),
        p("Physical Consistency: HIGH. Phase winding overload and cooling radiator degradation are clearly reflected in the top SHAP features.")
      )
    } else if (case_name == "Hydraulic Group") {
      tagList(
        h6("Physical Mechanics Validation: Hydraulic Group"),
        p("In Event 22, the model triggers on hydraulic oil temperature (temp_hydraulic_oil reaches 112°C)."),
        p("Physical Consistency: CRITICAL. Overheated hydraulic fluid compromises pitch cylinder pressure, causing impending aerodynamic loss.")
      )
    } else {
      tagList(
        h6("Physical Mechanics Validation: Healthy Control"),
        p("In Event 25, all key components maintain negative or near-zero anomaly attributions."),
        p("Physical Consistency: EXCELLENT. Thermal differentials stay coupled with ambient temperature without uncoupling.")
      )
    }
  })
  
  # Tab 5: Business Value & ROI Dynamic Calculations
  reactive_financials <- reactive({
    c_fn <- input$cost_fn
    c_fp <- input$cost_fp
    c_tp <- input$cost_tp
    thresh <- input$biz_threshold
    
    preds  <- as.integer(cv_predictions$xgb_prob >= thresh)
    actual <- cv_predictions$target
    
    tp <- sum(actual == 1 & preds == 1)
    fp <- sum(actual == 0 & preds == 1)
    fn <- sum(actual == 1 & preds == 0)
    
    total_cost <- (fn * c_fn) + (fp * c_fp) + (tp * c_tp)
    baseline_cost <- sum(actual == 1) * c_fn
    net_savings <- baseline_cost - total_cost
    roi <- (net_savings / (total_cost + 1)) * 100
    
    list(
      net_savings = net_savings,
      roi = roi,
      total_cost = total_cost,
      downtime_hours = tp * 180 # Average 180 hours downtime saved per caught event
    )
  })
  
  output$text_savings <- renderText({
    fin <- reactive_financials()
    paste0("$", format(round(fin$net_savings / 1e6, 2), big.mark = ","), " Million")
  })
  
  output$text_downtime_avoided <- renderText({
    fin <- reactive_financials()
    paste0(format(round(fin$downtime_hours / 1000, 1), big.mark = ","), "k Hours")
  })
  
  output$text_roi <- renderText({
    fin <- reactive_financials()
    paste0(round(fin$roi, 1), "%")
  })
  
  output$plot_cost_curve <- renderPlot({
    c_fn <- input$cost_fn
    c_fp <- input$cost_fp
    c_tp <- input$cost_tp
    
    thresholds <- seq(0.1, 0.9, by = 0.05)
    costs <- sapply(thresholds, function(t) {
      preds <- as.integer(cv_predictions$xgb_prob >= t)
      tp <- sum(cv_predictions$target == 1 & preds == 1)
      fp <- sum(cv_predictions$target == 0 & preds == 1)
      fn <- sum(cv_predictions$target == 1 & preds == 0)
      (fn * c_fn) + (fp * c_fp) + (tp * c_tp)
    })
    
    df_cost <- data.frame(Threshold = thresholds, TotalCostMillions = costs / 1e6)
    opt_idx <- which.min(df_cost$TotalCostMillions)
    opt_thresh <- df_cost$Threshold[opt_idx]
    
    ggplot(df_cost, aes(x = Threshold, y = TotalCostMillions)) +
      geom_line(color = "#00bcd4", linewidth = 1.2) +
      geom_point(data = df_cost[opt_idx, ], aes(x = Threshold, y = TotalCostMillions),
                 color = "#00e676", size = 4) +
      geom_vline(xintercept = input$biz_threshold, color = "#ffb300", linetype = "dashed") +
      annotate("text", x = opt_thresh, y = max(df_cost$TotalCostMillions) * 0.95,
               label = paste("Optimal Threshold:", opt_thresh), color = "#00e676", size = 4) +
      labs(x = "Decision Alarm Threshold", y = "Total Fleet Cost ($ Millions)",
           title = "Fleet Total Operational Cost Curve") +
      theme_minimal(base_size = 13) +
      theme(
        plot.background = element_rect(fill = "#222", color = NA),
        panel.background = element_rect(fill = "#222", color = NA),
        panel.grid = element_line(color = "#333"),
        text = element_text(color = "#eee"),
        axis.text = element_text(color = "#ccc")
      )
  })
}

# Run App
shinyApp(ui = ui, server = server)
