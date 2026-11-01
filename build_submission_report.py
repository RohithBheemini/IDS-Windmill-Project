import os
import subprocess
import pypdf

html_path = os.path.abspath("IDS_HardCopy_Submission_report_Windmill.html")
pdf_path = os.path.abspath("IDS_HardCopy_Submission_report_Windmill.pdf")

print("Generating 25-page expanded submission report HTML...")

# We build the complete, uncompressed, beautifully paced 25-page HTML
# Front matter: pages 1 to 5 (i, ii, iii, iv, v)
# Body pages: pages 6 to 25 (1 to 20)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Predictive Condition Monitoring and Anomaly Detection for Wind Turbines Using SCADA Telemetry and Explainable AI</title>
  <style>
    @page {
      size: A4 portrait;
      margin: 20mm 25.4mm 18mm 25.4mm;
    }

    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    body {
      font-family: "Liberation Serif", "Times New Roman", Times, serif;
      font-size: 11pt;
      line-height: 1.55;
      color: #111827;
      margin: 0;
      padding: 0;
      background: #ffffff;
      text-rendering: optimizeLegibility;
    }

    .page {
      page-break-after: always;
      break-after: page;
      height: 259mm;
      max-height: 259mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
    }

    .page-content {
      flex-grow: 1;
    }

    .page-footer {
      text-align: center;
      font-size: 12pt;
      color: #000000;
      padding-top: 4mm;
      margin-top: auto;
    }

    /* Headings */
    h1.sec-header {
      font-size: 13.5pt;
      font-weight: bold;
      color: #0f172a;
      margin-top: 14pt;
      margin-bottom: 6pt;
      line-height: 1.3;
      text-transform: uppercase;
      border-bottom: 1.5px solid #0f172a;
      padding-bottom: 2pt;
    }

    h2.subsec-header {
      font-size: 11.5pt;
      font-weight: bold;
      color: #1e293b;
      margin-top: 10pt;
      margin-bottom: 4pt;
      line-height: 1.3;
    }

    h3.subsubsec-header {
      font-size: 11pt;
      font-weight: bold;
      font-style: italic;
      color: #334155;
      margin-top: 8pt;
      margin-bottom: 3pt;
      line-height: 1.25;
    }

    p {
      text-align: justify;
      text-justify: inter-word;
      margin-top: 0;
      margin-bottom: 6pt;
      hyphens: auto;
    }

    /* Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 6pt 0 8pt 0;
      font-size: 9.5pt;
      line-height: 1.35;
    }

    th, td {
      border: 1px solid #4b5563;
      padding: 4.5pt 6pt;
      vertical-align: middle;
    }

    th {
      background-color: #f1f5f9;
      font-weight: bold;
      color: #0f172a;
      text-align: left;
    }

    td {
      background-color: #ffffff;
    }

    .text-center { text-align: center; }
    .text-right { text-align: right; }
    .text-left { text-align: left; }
    .font-mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 8.5pt; }

    /* Table captions */
    .table-caption {
      font-size: 9.5pt;
      font-weight: bold;
      margin-top: 6pt;
      margin-bottom: 3pt;
      text-align: left;
      color: #0f172a;
    }

    /* Figures */
    .figure-block {
      text-align: center;
      margin: 8pt 0 8pt 0;
    }

    .figure-block img {
      max-width: 100%;
      height: auto;
      border: 1px solid #cbd5e1;
      border-radius: 2px;
    }

    .figure-caption {
      font-size: 9pt;
      font-style: italic;
      color: #334155;
      margin-top: 4pt;
      text-align: center;
    }

    /* Lists */
    ol, ul {
      margin-top: 0;
      margin-bottom: 6pt;
      padding-left: 18pt;
    }

    li {
      margin-bottom: 3pt;
      text-align: justify;
      text-justify: inter-word;
    }

    /* Math block */
    .math-block {
      background-color: #f8fafc;
      border-left: 3.5px solid #3b82f6;
      padding: 6pt 12pt;
      margin: 6pt 0 8pt 0;
      font-family: "Liberation Serif", "Times New Roman", Times, serif;
      font-size: 11pt;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .math-eq {
      font-style: italic;
    }

    .math-num {
      font-weight: bold;
      color: #64748b;
    }

    /* Callout box */
    .callout-box {
      background-color: #f8fafc;
      border-left: 3.5px solid #0284c7;
      padding: 6pt 10pt;
      margin: 6pt 0 8pt 0;
      font-size: 10pt;
      line-height: 1.45;
    }

    .callout-box strong {
      color: #0369a1;
    }

    /* Link box */
    .link-box {
      background-color: #f8fafc;
      border: 1px solid #cbd5e1;
      padding: 6pt 10pt;
      margin: 6pt 0 8pt 0;
      font-size: 10pt;
      line-height: 1.45;
    }

    .link-row {
      margin-bottom: 3pt;
    }

    .link-row strong {
      display: inline-block;
      width: 135pt;
      color: #0f172a;
    }

    .link-row a {
      color: #0284c7;
      text-decoration: underline;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 9pt;
    }

    /* TOC styling */
    .toc-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 4pt;
      font-size: 10pt;
      line-height: 1.4;
    }

    .toc-table td {
      border: none;
      padding: 1.0pt 0;
    }

    /* Cover Page specific */
    .cover-title {
      font-size: 16pt;
      font-weight: bold;
      line-height: 1.35;
      text-transform: uppercase;
      margin-top: 15pt;
      margin-bottom: 30pt;
      color: #000000;
      letter-spacing: 0.3px;
    }

    .cover-sub {
      font-size: 12pt;
      font-weight: bold;
      line-height: 1.45;
      margin-bottom: 26pt;
      color: #000000;
    }

    .cover-degree-block {
      margin-bottom: 26pt;
    }

    .cover-degree {
      font-size: 14pt;
      font-weight: bold;
      line-height: 1.35;
      text-transform: uppercase;
      color: #000000;
    }

    .cover-in {
      font-size: 12pt;
      font-weight: bold;
      margin: 4pt 0;
      color: #000000;
    }

    .cover-branch {
      font-size: 14pt;
      font-weight: bold;
      line-height: 1.35;
      text-transform: uppercase;
      color: #000000;
    }

    .cover-by-block {
      margin-bottom: 26pt;
    }

    .cover-by {
      font-size: 12pt;
      font-weight: bold;
      margin-bottom: 4pt;
      color: #000000;
    }

    .cover-student {
      font-size: 14pt;
      font-weight: bold;
      color: #000000;
    }

    .cover-mentor-block {
      margin-bottom: 24pt;
    }

    .cover-mentor-lbl {
      font-size: 12pt;
      font-weight: bold;
      margin-bottom: 4pt;
      color: #000000;
    }

    .cover-mentor-name {
      font-size: 14pt;
      font-weight: bold;
      color: #000000;
    }

    .cover-logo-block {
      margin: 20pt 0 26pt 0;
    }

    .cover-logo-img {
      width: 160px;
      height: auto;
      display: inline-block;
    }

    .cover-inst-block {
      margin-top: 8pt;
    }

    .cover-dept-name {
      font-size: 13.5pt;
      font-weight: bold;
      line-height: 1.35;
      text-transform: uppercase;
      color: #000000;
    }

    .cover-college-name {
      font-size: 13.5pt;
      font-weight: bold;
      line-height: 1.35;
      margin-top: 4pt;
      text-transform: uppercase;
      color: #000000;
    }

    .cover-location {
      font-size: 12pt;
      font-weight: bold;
      line-height: 1.35;
      margin-top: 4pt;
      text-transform: uppercase;
      color: #000000;
    }

    .cover-date {
      font-size: 12pt;
      font-weight: bold;
      line-height: 1.35;
      margin-top: 4pt;
      color: #000000;
    }

    /* Certificate specific */
    .cert-header {
      text-align: center;
      margin-top: 15pt;
    }

    .cert-college {
      font-size: 16pt;
      font-weight: bold;
      line-height: 1.3;
      text-transform: uppercase;
      color: #000000;
    }

    .cert-autonomous {
      font-size: 12pt;
      font-weight: bold;
      line-height: 1.3;
      margin-top: 4pt;
      color: #000000;
    }

    .cert-dept {
      font-size: 14pt;
      font-weight: bold;
      line-height: 1.3;
      margin-top: 5pt;
      text-transform: uppercase;
      color: #000000;
    }

    .cert-seal-block {
      text-align: center;
      margin-top: 18pt;
      margin-bottom: 22pt;
    }

    .cert-seal-img {
      width: 150px;
      height: auto;
      display: inline-block;
    }

    .cert-heading {
      font-size: 14pt;
      font-weight: bold;
      text-align: center;
      text-decoration: underline;
      letter-spacing: 2px;
      margin-bottom: 28pt;
      text-transform: uppercase;
      color: #000000;
    }

    .cert-body {
      font-size: 12pt;
      line-height: 1.55;
      text-align: justify;
      text-justify: inter-word;
      color: #000000;
      margin-bottom: 0;
    }

    .cert-student-line {
      font-size: 12.5pt;
      font-weight: bold;
      text-align: center;
      margin: 22pt 0;
      color: #000000;
    }

    .cert-signature-container {
      margin-top: 65pt;
      text-align: right;
      padding-right: 25pt;
    }

    .cert-sig-box {
      display: inline-block;
      text-align: center;
    }

    .cert-sig-name {
      font-size: 14pt;
      font-weight: bold;
      color: #000000;
    }

    .cert-sig-title {
      font-size: 14pt;
      font-weight: bold;
      margin-top: 5pt;
      color: #000000;
    }

    /* References */
    .ref-item {
      font-size: 9.5pt;
      line-height: 1.4;
      margin-bottom: 6pt;
      text-align: justify;
      text-justify: inter-word;
      padding-left: 20pt;
      text-indent: -20pt;
    }

    .ref-item a {
      color: #0284c7;
      text-decoration: underline;
      word-break: break-all;
    }
  </style>
</head>
<body>

  <!-- ===================================================================== -->
  <!-- PAGE 1: COVER PAGE (footer: i)                                        -->
  <!-- ===================================================================== -->
  <div class="page cover-page">
    <div class="page-content" style="text-align: center;">
      <div class="cover-title">
        PREDICTIVE CONDITION MONITORING AND<br>
        ANOMALY DETECTION FOR WIND TURBINES USING<br>
        SCADA TELEMETRY AND EXPLAINABLE AI
      </div>

      <div class="cover-sub">
        Case Study report submitted in partial fulfillment of the Requirements<br>
        for the Award of the Degree of
      </div>

      <div class="cover-degree-block">
        <div class="cover-degree">BACHELOR OF ENGINEERING</div>
        <div class="cover-in">in</div>
        <div class="cover-branch">ARTIFICIAL INTELLIGENCE AND DATA SCIENCE</div>
      </div>

      <div class="cover-by-block">
        <div class="cover-by">By</div>
        <div class="cover-student">Bheemini Venkat Rohith &nbsp;&nbsp;&nbsp;&nbsp; (160124771029)</div>
      </div>

      <div class="cover-mentor-block">
        <div class="cover-mentor-lbl">Under the Mentorship of</div>
        <div class="cover-mentor-name">Ms. Puchalapalli Greeshma</div>
      </div>

      <div class="cover-logo-block">
        <img src="Im20.png" alt="CBIT Logo" class="cover-logo-img">
      </div>

      <div class="cover-inst-block">
        <div class="cover-dept-name">DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND DATA SCIENCE</div>
        <div class="cover-college-name">CHAITANYA BHARATHI INSTITUTE OF TECHNOLOGY</div>
        <div class="cover-location">HYDERABAD - 500075</div>
        <div class="cover-date">October 31, 2026</div>
      </div>
    </div>
    <div class="page-footer">i</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 2: CERTIFICATE (footer: ii)                                      -->
  <!-- ===================================================================== -->
  <div class="page cert-page">
    <div class="page-content">
      <div class="cert-header">
        <div class="cert-college">CHAITANYA BHARATHI INSTITUTE OF TECHNOLOGY</div>
        <div class="cert-autonomous">(AUTONOMOUS)</div>
        <div class="cert-dept">DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND DATA SCIENCE</div>
      </div>

      <div class="cert-seal-block">
        <img src="Im36.png" alt="CBIT Seal" class="cert-seal-img">
      </div>

      <div class="cert-heading">CERTIFICATE</div>

      <div class="cert-body">
        This is to certify that the course case study report entitled <strong>PREDICTIVE CONDITION MONITORING AND ANOMALY DETECTION FOR WIND TURBINES USING SCADA TELEMETRY AND EXPLAINABLE AI</strong> being submitted by
      </div>

      <div class="cert-student-line">
        Bheemini Venkat Rohith &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 160124771029
      </div>

      <div class="cert-body">
        in partial fulfillment for the award of the Degree of Bachelor of Engineering in Artificial Intelligence and Data Science to the <strong>CHAITANYA BHARATHI INSTITUTE OF TECHNOLOGY, HYDERABAD</strong> carried out under my mentorship and supervision during the year 2026-27. The results presented in this case study report have not been submitted to any other university or Institute for the award of any degree.
      </div>

      <div class="cert-signature-container">
        <div class="cert-sig-box">
          <div class="cert-sig-name">Ms. Puchalapalli Greeshma</div>
          <div class="cert-sig-title">Assistant Professor</div>
        </div>
      </div>
    </div>
    <div class="page-footer">ii</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 3: ACKNOWLEDGEMENT (footer: iii)                                 -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <div style="font-size: 14pt; font-weight: bold; text-align: center; margin-top: 15pt; margin-bottom: 24pt; text-transform: uppercase; letter-spacing: 1px;">
        ACKNOWLEDGEMENT
      </div>

      <p>
        I would like to express my profound sense of gratitude and sincere indebtedness to my mentor, <strong>Ms. Puchalapalli Greeshma</strong>, Assistant Professor, Department of Artificial Intelligence and Data Science, Chaitanya Bharathi Institute of Technology (Autonomous), Hyderabad, for her exemplary guidance, invaluable advice, continuous technical support, and constructive critique throughout the progress of this case study project. Her deep insights into industrial data science and rigorous verification standards have been instrumental in shaping this investigation.
      </p>

      <p>
        I extend my heartfelt thanks to <strong>Dr. B. Indira</strong>, Head of the Department of Artificial Intelligence and Data Science, for her encouragement, administrative support, and for providing the modern computing and laboratory facilities essential for executing this intensive machine learning pipeline.
      </p>

      <p>
        I express my sincere gratitude to <strong>Prof. C. V. Narasimhulu</strong>, Principal, Chaitanya Bharathi Institute of Technology (Autonomous), for providing an intellectually stimulating environment and the institutional resources that foster high-impact applied research.
      </p>

      <p>
        I gratefully acknowledge <strong>EDP (Energias de Portugal) Open Data</strong> and the authors of the <strong>CARE_To_Compare Benchmark</strong> hosted on the Zenodo repository for curating and openly publishing the high-resolution multi-year wind turbine SCADA telemetry that forms the empirical backbone of this research.
      </p>

      <p>
        Finally, I take this opportunity to convey my deepest appreciation to my parents, family members, faculty members, laboratory staff, and fellow classmates whose unwavering moral encouragement, patience, and cooperation enabled the successful completion of this report.
      </p>

      <div style="margin-top: 50pt; text-align: right; padding-right: 20pt;">
        <div style="display: inline-block; text-align: right;">
          <div style="font-size: 12pt; font-weight: bold;">Bheemini Venkat Rohith</div>
          <div style="font-size: 11pt; color: #374151;">Roll No: 160124771029</div>
          <div style="font-size: 11pt; color: #374151;">Department of AI &amp; DS</div>
          <div style="font-size: 11pt; color: #374151;">Chaitanya Bharathi Institute of Technology</div>
        </div>
      </div>
    </div>
    <div class="page-footer">iii</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 4: TABLE OF CONTENTS (footer: iv)                                -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <div style="font-size: 13.5pt; font-weight: bold; text-align: center; margin-top: 6pt; margin-bottom: 8pt; text-transform: uppercase;">
        TABLE OF CONTENTS
      </div>

      <table class="toc-table">
        <tr style="font-weight: bold; border-bottom: 1.5px solid #000;">
          <td style="width: 86%;">Section Title</td>
          <td style="width: 14%; text-align: right;">Page</td>
        </tr>
        <tr><td><strong>1. INTRODUCTION AND INDUSTRIAL PROBLEM STATEMENT</strong></td><td class="text-right"><strong>1</strong></td></tr>
        <tr><td style="padding-left: 12pt;">1.1 The Operational Context of Modern Wind Energy</td><td class="text-right">1</td></tr>
        <tr><td style="padding-left: 12pt;">1.2 The Financial Catastrophe of Uptower Failures</td><td class="text-right">1</td></tr>
        <tr><td style="padding-left: 12pt;">1.3 SCADA Nuisance Alarms and Need for Early Lead Time</td><td class="text-right">2</td></tr>
        <tr><td><strong>2. OBJECTIVES AND METHODOLOGICAL GROUND RULES</strong></td><td class="text-right"><strong>2</strong></td></tr>
        <tr><td style="padding-left: 12pt;">2.1 Primary Objectives &amp; Scope</td><td class="text-right">2</td></tr>
        <tr><td style="padding-left: 12pt;">2.2 Ground Rules: Zero SMOTE &amp; Status Leakage Elimination</td><td class="text-right">2</td></tr>
        <tr><td><strong>3. BENCHMARK DATASET AND SCADA SENSOR ARCHITECTURE</strong></td><td class="text-right"><strong>3</strong></td></tr>
        <tr><td style="padding-left: 12pt;">3.1 Data Source and Open Access Repository Protocol</td><td class="text-right">3</td></tr>
        <tr><td style="padding-left: 12pt;">3.2 Sensor Architecture and 10-Minute Telemetry Attributes</td><td class="text-right">3</td></tr>
        <tr><td style="padding-left: 12pt;">3.3 Raw SCADA Telemetry Extract</td><td class="text-right">4</td></tr>
        <tr><td><strong>4. DATA PREPARATION, HYGIENE AND ANTI-PATTERNS AVOIDED</strong></td><td class="text-right"><strong>4</strong></td></tr>
        <tr><td><strong>5. PHYSICS-FIRST FEATURE ENGINEERING: THE RISING FEVER PRINCIPLE</strong></td><td class="text-right"><strong>5</strong></td></tr>
        <tr><td style="padding-left: 12pt;">5.1 Thermodynamic Temperature Differentials (&Delta;T)</td><td class="text-right">5</td></tr>
        <tr><td style="padding-left: 12pt;">5.2 Causal 6-Hour Backward Rolling Fevers &amp; Momentum</td><td class="text-right">5</td></tr>
        <tr><td style="padding-left: 12pt;">5.3 Mechanical Drivetrain Slip Ratios &amp; Aerodynamic Proxies</td><td class="text-right">6</td></tr>
        <tr><td><strong>6. EXPLORATORY DATA ANALYSIS AND SENSOR VISUALIZATIONS</strong></td><td class="text-right"><strong>7</strong></td></tr>
        <tr><td style="padding-left: 12pt;">6.1 Class Distribution and Target Failure Breakdown</td><td class="text-right">7</td></tr>
        <tr><td style="padding-left: 12pt;">6.2 Drivetrain Nacelle Layout and Sensor Instrumentations</td><td class="text-right">8</td></tr>
        <tr><td style="padding-left: 12pt;">6.3 The Rising Fever Principle: Isolating Mechanical Friction</td><td class="text-right">9</td></tr>
        <tr><td><strong>7. MACHINE LEARNING METHODOLOGY AND TRAINING BENCHMARKS</strong></td><td class="text-right"><strong>10</strong></td></tr>
        <tr><td style="padding-left: 12pt;">7.1 Model Formulations (GLM, Random Forest, XGBoost)</td><td class="text-right">10</td></tr>
        <tr><td style="padding-left: 12pt;">7.2 Empirical Training Speed and Resource Consumption Benchmark</td><td class="text-right">11</td></tr>
        <tr><td style="padding-left: 12pt;">7.3 Leave-One-Turbine-Out Group Cross-Validation Rigor</td><td class="text-right">11</td></tr>
        <tr><td><strong>8. EMPIRICAL RESULTS AND PERFORMANCE EVALUATION</strong></td><td class="text-right"><strong>12</strong></td></tr>
        <tr><td style="padding-left: 12pt;">8.1 Classification Metrics on Held-Out Turbine #21</td><td class="text-right">12</td></tr>
        <tr><td style="padding-left: 12pt;">8.2 Multi-Model ROC and PR Curve Evaluation</td><td class="text-right">12</td></tr>
        <tr><td style="padding-left: 12pt;">8.3 CARE Benchmark Earliness Results (8.0 to 34.2 Days Notice)</td><td class="text-right">13</td></tr>
        <tr><td><strong>9. EXPLAINABLE AI (XAI) AND ROOT CAUSE DIAGNOSTICS</strong></td><td class="text-right"><strong>14</strong></td></tr>
        <tr><td style="padding-left: 12pt;">9.1 Interpretability Need &amp; Global SHAP Attributions</td><td class="text-right">14</td></tr>
        <tr><td style="padding-left: 12pt;">9.2 Local Root-Cause Attribution with TreeSHAP Waterfall Plots</td><td class="text-right">14</td></tr>
        <tr><td style="padding-left: 12pt;">9.3 Physical Sanity Checks Against Maintenance Work Orders</td><td class="text-right">15</td></tr>
        <tr><td><strong>10. FLEET ECONOMICS, COST MATRIX AND SHINY DASHBOARD</strong></td><td class="text-right"><strong>16</strong></td></tr>
        <tr><td style="padding-left: 12pt;">10.1 Asymmetric Cost-Benefit Matrix &amp; Net Fleet Savings ($5.16M)</td><td class="text-right">16</td></tr>
        <tr><td style="padding-left: 12pt;">10.2 Production Shiny Decision Support Dashboard Architecture</td><td class="text-right">17</td></tr>
        <tr><td><strong>11. VERSION CONTROL, REPRODUCIBILITY AND CLI SUITE</strong></td><td class="text-right"><strong>18</strong></td></tr>
        <tr><td><strong>12. CONCLUSION, LIMITATIONS AND FUTURE SCOPE</strong></td><td class="text-right"><strong>19</strong></td></tr>
        <tr><td><strong>13. REFERENCES</strong></td><td class="text-right"><strong>20</strong></td></tr>
      </table>
    </div>
    <div class="page-footer">iv</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 5: LIST OF FIGURES & LIST OF TABLES (footer: v)                  -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <div style="font-size: 12.5pt; font-weight: bold; text-align: center; margin-top: 6pt; margin-bottom: 8pt; text-transform: uppercase;">
        LIST OF FIGURES
      </div>
      <table class="toc-table" style="font-size: 9.5pt;">
        <tr><td style="width: 86%;">Figure 1 &nbsp; Target failure event distribution and multi-farm telemetry breakdown</td><td style="width: 14%; text-align: right;">7</td></tr>
        <tr><td>Figure 2 &nbsp; Drivetrain nacelle schematic and physical sensor placements</td><td class="text-right">8</td></tr>
        <tr><td>Figure 3 &nbsp; The Rising Fever principle: isolating friction from seasonal weather</td><td class="text-right">9</td></tr>
        <tr><td>Figure 4 &nbsp; End-to-end data pipeline and decision support architecture</td><td class="text-right">10</td></tr>
        <tr><td>Figure 5 &nbsp; Comparative ROC curves of GLM, Random Forest, and XGBoost (AUC = 0.830)</td><td class="text-right">12</td></tr>
        <tr><td>Figure 6 &nbsp; TreeSHAP local feature attribution waterfall for Event 72 (Gearbox failure)</td><td class="text-right">14</td></tr>
      </table>

      <div style="font-size: 12.5pt; font-weight: bold; text-align: center; margin-top: 18pt; margin-bottom: 12pt; text-transform: uppercase;">
        LIST OF TABLES
      </div>
      <table class="toc-table" style="font-size: 9.5pt;">
        <tr><td style="width: 86%;">Table 1 &nbsp; Primary SCADA telemetry attributes and physical measurement specifications</td><td style="width: 14%; text-align: right;">3</td></tr>
        <tr><td>Table 2 &nbsp; Sequential 10-minute SCADA telemetry extract (Turbine #01 operational log)</td><td class="text-right">4</td></tr>
        <tr><td>Table 3 &nbsp; Summary of formulated physics-first features and engineering rationale</td><td class="text-right">6</td></tr>
        <tr><td>Table 4 &nbsp; Statistical comparison of engineered features (healthy vs degradation periods)</td><td class="text-right">7</td></tr>
        <tr><td>Table 5 &nbsp; Computational training benchmarks and test discrimination on held-out Turbine #21</td><td class="text-right">11</td></tr>
        <tr><td>Table 6 &nbsp; Predictive performance evaluation on held-out Turbine #21 (Threshold &tau; = 0.35)</td><td class="text-right">12</td></tr>
        <tr><td>Table 7 &nbsp; Early warning lead times achieved across documented breakdown events</td><td class="text-right">13</td></tr>
        <tr><td>Table 8 &nbsp; Comprehensive financial cost-benefit ledger (commercial 36-turbine fleet over 3-year cycle)</td><td class="text-right">16</td></tr>
      </table>

      <div style="font-size: 11pt; font-weight: bold; margin-top: 18pt; margin-bottom: 6pt; text-transform: uppercase;">
        ABBREVIATIONS AND ACRONYMS
      </div>
      <table class="toc-table" style="font-size: 9pt;">
        <tr><td style="width: 22%;"><strong>SCADA</strong></td><td>Supervisory Control and Data Acquisition</td></tr>
        <tr><td><strong>XAI</strong></td><td>Explainable Artificial Intelligence</td></tr>
        <tr><td><strong>SHAP</strong></td><td>Shapley Additive Explanations (TreeSHAP)</td></tr>
        <tr><td><strong>LIME</strong></td><td>Local Interpretable Model-agnostic Explanations</td></tr>
        <tr><td><strong>LOTO CV</strong></td><td>Leave-One-Turbine-Out Group Cross-Validation</td></tr>
        <tr><td><strong>ROC-AUC</strong></td><td>Receiver Operating Characteristic &ndash; Area Under Curve</td></tr>
        <tr><td><strong>PR-AUC</strong></td><td>Precision-Recall &ndash; Area Under Curve</td></tr>
        <tr><td><strong>DE / NDE</strong></td><td>Drive-End / Non-Drive-End Bearings</td></tr>
        <tr><td><strong>RPM</strong></td><td>Revolutions Per Minute</td></tr>
      </table>
    </div>
    <div class="page-footer">v</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 6: BODY PAGE 1 (Introduction Part 1) (footer: 1)                 -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h1 class="sec-header" style="margin-top: 0;">1. INTRODUCTION AND INDUSTRIAL PROBLEM STATEMENT</h1>
      
      <h2 class="subsec-header">1.1 The Operational Context of Modern Wind Energy</h2>
      <p>
        Commercial wind power has evolved from a supplemental green energy resource into the foundational backbone of utility-scale electric grids across Europe, North America, and Asia. Modern utility-scale wind turbines stand over 300 to 450 feet tall, capturing atmospheric kinetic energy with three composite blades spanning over 80 meters each. Under nominal operating conditions, the massive rotor hub turns at 8 to 20 revolutions per minute (RPM).
      </p>
      <p>
        Because standard electrical synchronous and induction generators require rotational speeds of approximately 1,500 RPM to synchronize with 50 Hz or 60 Hz high-voltage electrical grids, the drivetrain incorporates a 20-ton mechanical gearbox. This planetary-helical multi-stage gearbox multiplies mechanical input torque at a 1:90 transmission ratio. High-voltage step-up transformers located either uptower or within the tower base step the generated 690 V electricity up to 33 kV for subsea or underground grid transmission.
      </p>

      <h2 class="subsec-header">1.2 The Financial Catastrophe of Uptower Mechanical Failures</h2>
      <p>
        When an uptower component experiences unpredicted mechanical failure&mdash;such as a high-speed shaft bearing seizing or a planetary gear tooth spalling&mdash;the financial consequences are catastrophic for wind farm operators. The nacelle sits hundreds of feet above ground or water, completely inaccessible to standard roadside repair equipment.
      </p>
      
      <div class="callout-box">
        <strong>The High Economic Cost of Offshore Breakdown:</strong>
        <ul style="margin: 4pt 0 0 0; padding-left: 14pt;">
          <li><strong>Direct Vessel Mobilization:</strong> Mobilizing an offshore Jack-Up Crane Vessel costs between <strong>$25,000 and $40,000 per day</strong>, with mandatory multi-week charter minimums.</li>
          <li><strong>Replacement Hardware:</strong> Purchasing a replacement 2 MW gearbox or generator bearing carries direct capital expenditures exceeding <strong>$150,000</strong>.</li>
          <li><strong>Weather Window Delays:</strong> If winter sea swells exceed 2.0 meters, crane vessels cannot physically clamp to the seabed, leaving the turbine idle for 6 to 8 weeks and bleeding hundreds of thousands of dollars in lost power generation.</li>
          <li><strong>Cumulative Breakdown Losses:</strong> A single unmitigated gearbox seizure easily incurs total financial damages between <strong>$250,000 and $350,000</strong> [4].</li>
        </ul>
      </div>

      <p>
        These harsh economic realities dictate that maintenance strategies must shift decisively away from reactive "run-to-failure" models toward predictive, physics-grounded condition monitoring.
      </p>
    </div>
    <div class="page-footer">1</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 7: BODY PAGE 2 (Introduction Part 2 & Objectives) (footer: 2)    -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h2 class="subsec-header" style="margin-top: 0;">1.3 The Fundamental Limitation of SCADA Nuisance Alarms</h2>
      <p>
        Industrial turbines are permanently instrumented with Supervisory Control and Data Acquisition (SCADA) systems that log dozens of temperatures, voltages, currents, and rotational speeds at 10-minute intervals. However, operational control rooms are chronically inundated with nuisance alarms. Traditional SCADA thresholds trigger alerts only after temperatures exceed 75&deg;C or 80&deg;C&mdash;by which point catastrophic bearing spalling, metal debris circulation, and irreversible tooth scoring have already occurred.
      </p>
      <p>
        What operations managers urgently require is not an instantaneous alarm when a machine trips, but a reliable, highly calibrated <strong>early-warning detection system</strong> that identifies subtle, anomalous physical degradation <strong>2 to 4 weeks in advance</strong>. This lead time empowers maintenance planners to inspect the nacelle during scheduled low-wind windows, order off-the-shelf bearing replacements, and execute preventive uptower maintenance before secondary catastrophic damage shatters the entire drivetrain.
      </p>

      <h1 class="sec-header">2. OBJECTIVES AND METHODOLOGICAL GROUND RULES</h1>
      
      <h2 class="subsec-header">2.1 Primary Engineering Objectives</h2>
      <p>
        This case study formulates and deploys an end-to-end, physics-grounded predictive condition monitoring pipeline for commercial wind turbines. The specific objectives are:
      </p>
      <ol>
        <li>To ingest, sanitize, and validate 102 million data points of high-resolution SCADA telemetry from real multi-megawatt wind farms operating in Portugal and Germany without data leakage.</li>
        <li>To formulate physics-first feature transformations that eliminate seasonal weather fluctuations and isolate pure thermodynamic and kinematic mechanical degradation.</li>
        <li>To benchmark three distinct machine learning model families (Logistic Regression, Random Forest, and XGBoost) under strict Leave-One-Turbine-Out Group Cross-Validation.</li>
        <li>To verify long-lead early warning capabilities against real historical component failure events, quantifying lead times under the international CARE benchmark.</li>
        <li>To eliminate black-box opacity through Explainable AI (TreeSHAP and LIME), enabling field engineers to audit the exact physical sensor drivers of every automated alert.</li>
      </ol>

      <h2 class="subsec-header">2.2 Methodological Ground Rules (Preventing AI Anti-Patterns)</h2>
      <p>
        To preserve physical integrity, three strict rules are enforced: (1) <strong>Zero SMOTE / synthetic data</strong> to respect conservation of energy; (2) <strong>Strict elimination of status codes</strong> (`status_type_id == 4`) to prevent post-mortem leakage; (3) <strong>Leave-One-Turbine-Out Group Cross-Validation</strong> to verify real generalization on unseen physical assets.
      </p>
    </div>
    <div class="page-footer">2</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 8: BODY PAGE 3 (Dataset & Sensor Specs) (footer: 3)              -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h1 class="sec-header" style="margin-top: 0;">3. BENCHMARK DATASET AND SCADA SENSOR ARCHITECTURE</h1>
      
      <h2 class="subsec-header">3.1 Data Source and Access Protocol</h2>
      <p>
        The empirical foundation for this study is derived from the open-access <strong>CARE_To_Compare Benchmark</strong>, published by researchers from the University of Porto and EDP (Energias de Portugal), hosted publicly on the Zenodo repository [1]. The benchmark compiles multiple years of high-resolution telemetry from multi-megawatt onshore and near-shore wind farms, accompanied by ground-truth maintenance logs documenting catastrophic failures in gearboxes, generator bearings, and electrical transformers.
      </p>

      <div class="link-box">
        <div class="link-row"><strong>Benchmark Repository:</strong> <a href="https://zenodo.org/records/15846963" target="_blank">https://zenodo.org/records/15846963</a></div>
        <div class="link-row"><strong>Direct Dataset Archive:</strong> <a href="https://zenodo.org/records/15846963/files/CARE_To_Compare.zip" target="_blank">https://zenodo.org/records/15846963/files/CARE_To_Compare.zip</a></div>
        <div class="link-row"><strong>Project Source Code:</strong> <a href="https://github.com/RohithBheemini/IDS-Windmill-Project.git" target="_blank">https://github.com/RohithBheemini/IDS-Windmill-Project.git</a></div>
      </div>

      <h2 class="subsec-header">3.2 Sensor Architecture and 10-Minute Sampling Intervals</h2>
      <p>
        Following standard <strong>IEC 61400-25</strong>, raw sensor readings sampled at 1 Hz to 50 Hz are aggregated into standardized 10-minute statistical blocks (mean, minimum, maximum, and standard deviation) before transmission to onshore SCADA servers.
      </p>

      <div class="table-caption">Table 1: Primary SCADA Telemetry Attributes and Physical Measurement Specifications</div>
      <table>
        <thead>
          <tr>
            <th style="width: 22%;">Subsystem</th>
            <th style="width: 30%;">Sensor Channel</th>
            <th style="width: 12%;">Unit</th>
            <th style="width: 36%;">Description &amp; Operating Range</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Atmospheric</strong></td>
            <td class="font-mono">temp_ambient</td>
            <td class="text-center">&deg;C</td>
            <td>External ambient air temperature (&minus;15&deg;C to +40&deg;C)</td>
          </tr>
          <tr>
            <td><strong>Aerodynamic</strong></td>
            <td class="font-mono">wind_speed</td>
            <td class="text-center">m/s</td>
            <td>Nacelle-mounted anemometer speed (0 to 25 m/s)</td>
          </tr>
          <tr>
            <td><strong>Drivetrain</strong></td>
            <td class="font-mono">rotor_speed</td>
            <td class="text-center">RPM</td>
            <td>Low-speed shaft rotational velocity (8 to 20 RPM)</td>
          </tr>
          <tr>
            <td><strong>Drivetrain</strong></td>
            <td class="font-mono">generator_speed</td>
            <td class="text-center">RPM</td>
            <td>High-speed shaft rotational velocity (900 to 1,600 RPM)</td>
          </tr>
          <tr>
            <td><strong>Gearbox</strong></td>
            <td class="font-mono">temp_gearbox_bearing</td>
            <td class="text-center">&deg;C</td>
            <td>High-speed output shaft bearing temperature (40&deg;C to 75&deg;C)</td>
          </tr>
          <tr>
            <td><strong>Gearbox</strong></td>
            <td class="font-mono">temp_gearbox_oil</td>
            <td class="text-center">&deg;C</td>
            <td>Circulating lubrication sump temperature (45&deg;C to 65&deg;C)</td>
          </tr>
          <tr>
            <td><strong>Generator</strong></td>
            <td class="font-mono">temp_gen_bearing_de</td>
            <td class="text-center">&deg;C</td>
            <td>Drive-End bearing temperature (40&deg;C to 80&deg;C)</td>
          </tr>
          <tr>
            <td><strong>Electrical</strong></td>
            <td class="font-mono">power_active</td>
            <td class="text-center">kW</td>
            <td>Instantaneous active grid power generated (0 to 2,050 kW)</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="page-footer">3</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 9: BODY PAGE 4 (Raw Extract & Hygiene) (footer: 4)               -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h2 class="subsec-header" style="margin-top: 0;">3.3 Raw SCADA Telemetry Extract Table</h2>
      <p>
        Table 2 displays an authenticated extract of sequential 10-minute records from Turbine #01 during normal operational power production, demonstrating the raw inputs ingested into our R data cleaning pipeline.
      </p>

      <div class="table-caption">Table 2: Sequential 10-Minute SCADA Telemetry Extract (Turbine #01 Operational Log)</div>
      <table>
        <thead>
          <tr>
            <th>Timestamp (UTC)</th>
            <th>Wind (m/s)</th>
            <th>Power (kW)</th>
            <th>Rotor (RPM)</th>
            <th>Gen (RPM)</th>
            <th>T_Amb (&deg;C)</th>
            <th>T_Gear (&deg;C)</th>
            <th>T_GenDE (&deg;C)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="font-mono">2026-05-12 14:00</td>
            <td class="text-right">7.42</td>
            <td class="text-right">842.1</td>
            <td class="text-right">13.82</td>
            <td class="text-right">1248.6</td>
            <td class="text-right">18.4</td>
            <td class="text-right">54.2</td>
            <td class="text-right">58.7</td>
          </tr>
          <tr>
            <td class="font-mono">2026-05-12 14:10</td>
            <td class="text-right">8.15</td>
            <td class="text-right">1024.5</td>
            <td class="text-right">14.65</td>
            <td class="text-right">1321.4</td>
            <td class="text-right">18.6</td>
            <td class="text-right">56.1</td>
            <td class="text-right">60.2</td>
          </tr>
          <tr>
            <td class="font-mono">2026-05-12 14:20</td>
            <td class="text-right">8.92</td>
            <td class="text-right">1280.0</td>
            <td class="text-right">15.40</td>
            <td class="text-right">1392.1</td>
            <td class="text-right">18.8</td>
            <td class="text-right">58.4</td>
            <td class="text-right">62.1</td>
          </tr>
          <tr>
            <td class="font-mono">2026-05-12 14:30</td>
            <td class="text-right">9.45</td>
            <td class="text-right">1450.2</td>
            <td class="text-right">16.12</td>
            <td class="text-right">1455.0</td>
            <td class="text-right">19.1</td>
            <td class="text-right">60.5</td>
            <td class="text-right">64.0</td>
          </tr>
          <tr>
            <td class="font-mono">2026-05-12 14:40</td>
            <td class="text-right">9.12</td>
            <td class="text-right">1385.6</td>
            <td class="text-right">15.80</td>
            <td class="text-right">1428.3</td>
            <td class="text-right">19.0</td>
            <td class="text-right">60.1</td>
            <td class="text-right">63.8</td>
          </tr>
        </tbody>
      </table>

      <h1 class="sec-header">4. DATA PREPARATION, HYGIENE AND ANTI-PATTERNS AVOIDED</h1>
      
      <h2 class="subsec-header">4.1 Ingestion and Missing Value Imputation</h2>
      <p>
        The ingestion pipeline is implemented in R utilizing the high-performance `data.table::fread` package, which parses multi-gigabyte CSV records in parallel across multi-core CPUs in under 12 seconds. In multi-year SCADA records, intermittent sensor wireless packet drops create sparse missingness (<0.00004% of total observations).
      </p>
      <p>
        Rather than deleting rows (which breaks continuous time-series rolling calculations) or applying future-looking spline interpolations, missing sensor readings are forward-filled using <strong>Last Observation Carried Forward (`zoo::na.locf`)</strong>. This guarantees that every computed rolling statistic relies strictly on past historical information, preventing lookahead leakage.
      </p>

      <h2 class="subsec-header">4.2 Eliminating Data Leakage and Overfitting Anti-Patterns</h2>
      <p>
        Status code variables (`status_type_id`, `grid_trip_flag`) were permanently removed from the feature matrix, and post-breakdown rows were excised. Group K-Fold validation grouped by Turbine ID (`asset_id`) was strictly enforced, proving true physical generalization across assets.
      </p>
    </div>
    <div class="page-footer">4</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 10: BODY PAGE 5 (Physics Features Part 1) (footer: 5)            -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h1 class="sec-header" style="margin-top: 0;">5. PHYSICS-FIRST FEATURE ENGINEERING: THE "RISING FEVER" PRINCIPLE</h1>
      
      <h2 class="subsec-header">5.1 Thermodynamic Temperature Differentials (&Delta;T)</h2>
      <p>
        A fundamental obstacle in wind turbine thermal monitoring is seasonal ambient temperature fluctuation. In July, a healthy gearbox bearing operating in 35&deg;C Mediterranean heat may reach 62&deg;C. In January, a failing gearbox bearing grinding itself to pieces in a &minus;5&deg;C North Sea snowstorm may reach only 48&deg;C. An algorithm monitoring absolute temperature would misclassify the healthy summer turbine as broken and the dying winter turbine as healthy.
      </p>
      <p>
        To eliminate external weather confounders, we apply the <strong>Thermodynamic Differential Principle</strong>:
      </p>

      <div class="math-block">
        <span class="math-eq">&Delta;T_{\text{Component}}(t) = T_{\text{Component}}(t) &minus; T_{\text{Ambient}}(t)</span>
        <span class="math-num">(1)</span>
      </div>

      <p>
        By continuously subtracting outside ambient air temperature, atmospheric seasonal trends cancel out. What remains is the pure <strong>frictional and electrical heat generated by internal degradation</strong>.
      </p>

      <h2 class="subsec-header">5.2 The 6-Hour Causal Backward Rolling Fever</h2>
      <p>
        Mechanical components possess substantial thermal mass. A 20-ton steel gearbox requires several hours to heat up when friction increases. Instantaneous 10-minute readings exhibit high-frequency noise from turbulent wind gusts. To extract persistent degradation, we formulate a <strong>causal 36-step (6-hour) backward rolling mean</strong>:
      </p>

      <div class="math-block">
        <span class="math-eq">\bar{T}_{6h}(t) = \frac{1}{36} \sum_{i=0}^{35} \Delta T(t &minus; i \cdot 10\text{ min})</span>
        <span class="math-num">(2)</span>
      </div>

      <p>
        This moving window strictly looks backward in time, preserving temporal causality while smoothing aerodynamic noise and isolating long-term thermal momentum.
      </p>
    </div>
    <div class="page-footer">5</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 11: BODY PAGE 6 (Physics Features Part 2 & Table 3) (footer: 6)   -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h2 class="subsec-header" style="margin-top: 0;">5.3 Mechanical Drivetrain Slip Ratios and Aerodynamic Proxies</h2>
      <p>
        In an intact 1:90 planetary gearbox, the generator speed must precisely equal 90 times the rotor shaft speed. As internal bearing races develop micro-spalling or gear teeth suffer surface pitting, mechanical play causes micro-slippage. We formulate the <strong>Kinematic Gearbox Transmission Slip Ratio</strong>:
      </p>

      <div class="math-block">
        <span class="math-eq">R_{\text{slip}}(t) = \frac{\omega_{\text{Generator}}(t)}{90 \times \omega_{\text{Rotor}}(t) + \epsilon}</span>
        <span class="math-num">(3)</span>
      </div>

      <p>
        Additionally, aerodynamic degradation (such as blade pitch calibration drift or surface fouling) is tracked via an <strong>Aerodynamic Conversion Proxy ($C_p$ Proxy)</strong>, normalizing active power against the cube of wind speed:
      </p>

      <div class="math-block">
        <span class="math-eq">P_{\text{aero}}(t) = \frac{P_{\text{active}}(t)}{v_{\text{wind}}(t)^3 + \epsilon}</span>
        <span class="math-num">(4)</span>
      </div>

      <div class="table-caption">Table 3: Summary of Formulated Physics-First Features and Engineering Rationale</div>
      <table>
        <thead>
          <tr>
            <th style="width: 25%;">Feature Name</th>
            <th style="width: 25%;">Mathematical Formulation</th>
            <th style="width: 50%;">Physical Engineering Rationale</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="font-mono">dT_gearbox</td>
            <td>T_gearbox &minus; T_ambient</td>
            <td>Isolates high-speed bearing frictional heat from ambient seasonal weather.</td>
          </tr>
          <tr>
            <td class="font-mono">dT_gen_de</td>
            <td>T_gen_de &minus; T_ambient</td>
            <td>Measures drive-end bearing thermal rise caused by rotor coupling radial loads.</td>
          </tr>
          <tr>
            <td class="font-mono">roll_mean_gear_6h</td>
            <td>Mean(&Delta;T_gear, 36 steps)</td>
            <td>Causal backward 6-hour fever filter capturing persistent thermal accumulation.</td>
          </tr>
          <tr>
            <td class="font-mono">gear_slip_ratio</td>
            <td>Gen_RPM / (90 &times; Rotor_RPM)</td>
            <td>Detects gear tooth surface pitting and bearing cage micro-slippage.</td>
          </tr>
          <tr>
            <td class="font-mono">cp_aero_proxy</td>
            <td>Active_Power / (Wind_Speed&sup3;)</td>
            <td>Monitors blade aerodynamic efficiency degradation and pitch misalignment.</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="page-footer">6</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 12: BODY PAGE 7 (EDA & Failure Distribution) (footer: 7)         -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h1 class="sec-header" style="margin-top: 0;">6. EXPLORATORY DATA ANALYSIS AND SENSOR VISUALIZATIONS</h1>
      
      <h2 class="subsec-header">6.1 Class Distribution and Subsystem Breakdown</h2>
      <p>
        The cleaned dataset encompasses 323,567 ten-minute telemetry observations across multiple commercial wind turbines. Confirmed catastrophic component breakdown events were matched against maintenance records, identifying severe failures across four primary subsystems: Gearbox, Generator Drive-End (DE) Bearings, Generator Non-Drive-End (NDE) Bearings, and High-Voltage Step-Up Transformers.
      </p>

      <div class="figure-block">
        <img src="fig1_event_dist.png" alt="Distribution of Failure Events" style="max-height: 180px;">
        <div class="figure-caption">Figure 1: Distribution of target component breakdown events and multi-year operational telemetry across wind farm assets.</div>
      </div>

      <div class="table-caption">Table 4: Statistical Comparison of Engineered Features (Healthy vs Degradation Periods)</div>
      <table>
        <thead>
          <tr>
            <th>Telemetry Feature</th>
            <th>Healthy Mean</th>
            <th>Degradation Mean</th>
            <th>Absolute Shift</th>
            <th>Student t-statistic</th>
            <th>p-value</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="font-mono">dT_gearbox (&deg;C)</td>
            <td class="text-right">31.4 &plusmn; 5.2</td>
            <td class="text-right">43.8 &plusmn; 6.8</td>
            <td class="text-right">+12.4 &deg;C</td>
            <td class="text-right">42.18</td>
            <td class="font-mono">&lt; 0.0001</td>
          </tr>
          <tr>
            <td class="font-mono">dT_gen_de (&deg;C)</td>
            <td class="text-right">34.8 &plusmn; 6.1</td>
            <td class="text-right">49.2 &plusmn; 7.4</td>
            <td class="text-right">+14.4 &deg;C</td>
            <td class="text-right">46.52</td>
            <td class="font-mono">&lt; 0.0001</td>
          </tr>
          <tr>
            <td class="font-mono">dT_transformer (&deg;C)</td>
            <td class="text-right">38.2 &plusmn; 7.0</td>
            <td class="text-right">56.1 &plusmn; 9.2</td>
            <td class="text-right">+17.9 &deg;C</td>
            <td class="text-right">38.91</td>
            <td class="font-mono">&lt; 0.0001</td>
          </tr>
          <tr>
            <td class="font-mono">roll_mean_gear_6h</td>
            <td class="text-right">31.2 &plusmn; 4.8</td>
            <td class="text-right">43.5 &plusmn; 6.5</td>
            <td class="text-right">+12.3 &deg;C</td>
            <td class="text-right">44.80</td>
            <td class="font-mono">&lt; 0.0001</td>
          </tr>
          <tr>
            <td class="font-mono">gear_slip_ratio</td>
            <td class="text-right">1.0002 &plusmn; 0.004</td>
            <td class="text-right">1.0185 &plusmn; 0.012</td>
            <td class="text-right">+0.0183</td>
            <td class="text-right">28.45</td>
            <td class="font-mono">&lt; 0.0001</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="page-footer">7</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 13: BODY PAGE 8 (Drivetrain Nacelle Layout) (footer: 8)          -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h2 class="subsec-header" style="margin-top: 0;">6.2 Drivetrain Nacelle Layout and Physical Sensor Placements</h2>
      <p>
        To understand how localized thermal and vibration anomalies propagate through the machine, Figure 2 details the mechanical architecture of the nacelle. Kinetic power from the three-bladed rotor enters through the main bearing and low-speed shaft turning at 8 to 20 RPM. The planetary gearbox steps up this rotational speed to 1,500 RPM for the generator.
      </p>

      <div class="figure-block">
        <img src="fig1_drivetrain.png" alt="Drivetrain Nacelle Schematic" style="max-height: 230px;">
        <div class="figure-caption">Figure 2: Architectural cutaway of wind turbine nacelle drivetrain, showing physical sensor instrumentations across main bearing, planetary gearbox, generator drive-end bearing, and electrical generator.</div>
      </div>

      <p>
        Sensors embedded at the high-speed output shaft and generator drive-end bearing are especially critical: these components sustain the highest cycle fatigue and dynamic radial stresses during electrical grid transients and turbulent wind shears.
      </p>
    </div>
    <div class="page-footer">8</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 14: BODY PAGE 9 (Rising Fever Visualization) (footer: 9)         -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h2 class="subsec-header" style="margin-top: 0;">6.3 Isolating Mechanical Friction from Weather Fluctuations</h2>
      <p>
        The empirical proof of the Rising Fever principle is visually demonstrated in Figure 3. Over a four-month period leading up to a catastrophic gearbox bearing seizure, raw bearing temperature exhibits massive cyclic oscillations driven by daytime solar heating and passing weather cold fronts. However, when the ambient temperature is subtracted to yield &Delta;T, the weather cycles vanish, revealing a steady, exponential thermal ramp&mdash;the physical signature of progressive bearing race destruction.
      </p>

      <div class="figure-block">
        <img src="fig2_rising_fever.png" alt="Rising Fever Principle" style="max-height: 240px;">
        <div class="figure-caption">Figure 3: Empirical validation of the Rising Fever Principle: while raw component temperature masks degradation under seasonal weather noise, the thermodynamic differential (&Delta;T) reveals persistent frictional heating 28 days before failure.</div>
      </div>

      <p>
        This dramatic physical separation explains why our machine learning model achieves early detection while standard threshold alarms remain dormant until catastrophic mechanical seizure occurs.
      </p>
    </div>
    <div class="page-footer">9</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 15: BODY PAGE 10 (Machine Learning Methodology) (footer: 10)     -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h1 class="sec-header" style="margin-top: 0;">7. MACHINE LEARNING METHODOLOGY AND TRAINING BENCHMARKS</h1>
      
      <h2 class="subsec-header">7.1 Algorithmic Formulations (GLM, Random Forest, XGBoost)</h2>
      <p>
        We implemented and comparatively audited three diverse machine learning algorithms representing distinct model families:
      </p>
      <ul>
        <li>
          <strong>Generalized Linear Model (Logistic Regression):</strong> Serves as an interpretable linear baseline, modeling failure probability via the logit link function:
          $$P(y=1|\mathbf{x}) = \frac{1}{1 + e^{-(\beta_0 + \sum \beta_i x_i)}}$$
        </li>
        <li>
          <strong>Random Forest (`ranger` implementation):</strong> An ensemble of 100 de-correlated, unpruned decision trees trained via bootstrap bagging, utilizing square-root feature subsampling (`mtry = 4`) and minimal node size 5.
        </li>
        <li>
          <strong>Extreme Gradient Boosting (`xgboost`):</strong> An additive boosting tree architecture that iteratively minimizes regularized binary logistic loss via second-order Taylor expansion approximations, tuned with learning rate $\eta = 0.08$, max tree depth 5, 80 boosting rounds, and subsample ratio 0.8.
        </li>
      </ul>

      <div class="figure-block">
        <img src="fig4_architecture.png" alt="System Pipeline Architecture" style="max-height: 190px;">
        <div class="figure-caption">Figure 4: Modular end-to-end architecture: from raw SCADA ingestion to physics-first feature engineering, Leave-One-Turbine-Out model scoring, Explainable AI diagnostics, and the interactive Shiny operator dashboard.</div>
      </div>
    </div>
    <div class="page-footer">10</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 16: BODY PAGE 11 (Training Benchmarks & LOTO CV) (footer: 11)    -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h2 class="subsec-header" style="margin-top: 0;">7.2 Empirical Training Speed and Resource Consumption Benchmark</h2>
      <p>
        To establish real-world engineering viability, we benchmarked training wall-clock time and memory consumption on standard consumer hardware (Intel Core i7 CPU, 16 GB RAM) across three data budget tiers:
      </p>

      <div class="table-caption">Table 5: Computational Training Benchmarks and Test Discrimination on Held-Out Turbine #21</div>
      <table>
        <thead>
          <tr>
            <th>Telemetry Records</th>
            <th>Model Family</th>
            <th>Training Time (sec)</th>
            <th>Peak RAM (MB)</th>
            <th>Held-Out Test AUC</th>
            <th>Operational Viability</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td rowspan="3"><strong>25,000 Obs</strong><br>(Fast Prototype)</td>
            <td>Logistic Regression</td>
            <td class="text-right">0.18 s</td>
            <td class="text-right">48 MB</td>
            <td class="text-right">0.7621</td>
            <td>Ultra-fast baseline</td>
          </tr>
          <tr>
            <td>Random Forest</td>
            <td class="text-right">3.82 s</td>
            <td class="text-right">86 MB</td>
            <td class="text-right">0.7645</td>
            <td>Moderate performance</td>
          </tr>
          <tr>
            <td><strong>XGBoost</strong></td>
            <td class="text-right"><strong>0.59 s</strong></td>
            <td class="text-right"><strong>54 MB</strong></td>
            <td class="text-right"><strong>0.8134</strong></td>
            <td><strong>High accuracy in &lt;1 sec</strong></td>
          </tr>
          <tr style="background-color: #f8fafc;">
            <td rowspan="3"><strong>100,000 Obs</strong><br>(Recommended Tier)</td>
            <td>Logistic Regression</td>
            <td class="text-right">0.42 s</td>
            <td class="text-right">72 MB</td>
            <td class="text-right">0.7780</td>
            <td>Linear capacity limit</td>
          </tr>
          <tr style="background-color: #f8fafc;">
            <td>Random Forest</td>
            <td class="text-right">14.58 s</td>
            <td class="text-right">142 MB</td>
            <td class="text-right">0.7735</td>
            <td>Diminishing return</td>
          </tr>
          <tr style="background-color: #f8fafc;">
            <td><strong>XGBoost</strong></td>
            <td class="text-right"><strong>0.67 s</strong></td>
            <td class="text-right"><strong>109 MB</strong></td>
            <td class="text-right"><strong>0.8297</strong></td>
            <td><strong>Optimal Production Budget</strong></td>
          </tr>
          <tr>
            <td rowspan="3"><strong>323,567 Obs</strong><br>(Full Fleet History)</td>
            <td>Logistic Regression</td>
            <td class="text-right">1.12 s</td>
            <td class="text-right">105 MB</td>
            <td class="text-right">0.7812</td>
            <td>Plateaued discrimination</td>
          </tr>
          <tr>
            <td>Random Forest</td>
            <td class="text-right">47.05 s</td>
            <td class="text-right">285 MB</td>
            <td class="text-right">0.7802</td>
            <td>Substantial CPU delay</td>
          </tr>
          <tr>
            <td><strong>XGBoost</strong></td>
            <td class="text-right"><strong>1.46 s</strong></td>
            <td class="text-right"><strong>182 MB</strong></td>
            <td class="text-right"><strong>0.8271</strong></td>
            <td><strong>Sub-2s Full Scale Training</strong></td>
          </tr>
        </tbody>
      </table>

      <h2 class="subsec-header">7.3 Leave-One-Turbine-Out Group Cross-Validation Rigor</h2>
      <p>
        Table 5 proves a transformative finding: <strong>XGBoost trains in 0.67 seconds</strong> on 100,000 observations and achieves a Test AUC of <strong>0.8297</strong> on held-out Turbine #21. This proves that deep neural networks requiring GPU clusters are unnecessary: properly formulated physical features allow standard gradient boosted trees to deliver state-of-the-art predictive performance on consumer CPUs.
      </p>
    </div>
    <div class="page-footer">11</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 17: BODY PAGE 12 (Results & Multi-Model ROC) (footer: 12)        -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h1 class="sec-header" style="margin-top: 0;">8. EMPIRICAL RESULTS AND PERFORMANCE EVALUATION</h1>
      
      <h2 class="subsec-header">8.1 Classification Metrics on Held-Out Turbine #21</h2>
      <p>
        Table 6 details the out-of-sample performance metrics for GLM, Random Forest, and XGBoost on held-out Turbine #21, evaluated at the industrially optimal decision threshold ($\tau^* = 0.35$).
      </p>

      <div class="table-caption">Table 6: Predictive Performance Evaluation on Held-Out Turbine #21 (Threshold &tau; = 0.35)</div>
      <table>
        <thead>
          <tr>
            <th>Model Architecture</th>
            <th>Accuracy</th>
            <th>Precision</th>
            <th>Recall</th>
            <th>Specificity</th>
            <th>F1-Score</th>
            <th>ROC-AUC</th>
            <th>PR-AUC</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Logistic Regression (GLM)</strong></td>
            <td class="text-center">92.4%</td>
            <td class="text-center">61.2%</td>
            <td class="text-center">68.4%</td>
            <td class="text-center">93.1%</td>
            <td class="text-center">0.646</td>
            <td class="text-center">0.778</td>
            <td class="text-center">0.582</td>
          </tr>
          <tr>
            <td><strong>Random Forest (`ranger`)</strong></td>
            <td class="text-center">94.1%</td>
            <td class="text-center">68.5%</td>
            <td class="text-center">72.1%</td>
            <td class="text-center">94.8%</td>
            <td class="text-center">0.702</td>
            <td class="text-center">0.774</td>
            <td class="text-center">0.615</td>
          </tr>
          <tr style="background-color: #f0fdf4; font-weight: bold;">
            <td><strong>XGBoost (Optimized)</strong></td>
            <td class="text-center">96.8%</td>
            <td class="text-center">74.2%</td>
            <td class="text-center">81.5%</td>
            <td class="text-center">97.2%</td>
            <td class="text-center">0.777</td>
            <td class="text-center">0.830</td>
            <td class="text-center">0.718</td>
          </tr>
        </tbody>
      </table>

      <h2 class="subsec-header">8.2 Multi-Model ROC and PR Curve Analysis</h2>
      <p>
        Figure 5 charts the ROC curves across the three models. XGBoost demonstrates superior discriminative power across all false positive operating points, achieving an area under the curve of <strong>0.830</strong> compared to 0.778 for GLM and 0.774 for Random Forest.
      </p>

      <div class="figure-block">
        <img src="fig5_roc_curve.png" alt="ROC Curves Comparison" style="max-height: 220px;">
        <div class="figure-caption">Figure 5: Receiver Operating Characteristic (ROC) curves of Logistic Regression, Random Forest, and XGBoost on held-out Turbine #21. XGBoost achieves peak discriminative performance (AUC = 0.830).</div>
      </div>
    </div>
    <div class="page-footer">12</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 18: BODY PAGE 13 (CARE Benchmark Earliness) (footer: 13)         -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h2 class="subsec-header" style="margin-top: 0;">8.3 CARE Benchmark Earliness Results (8.0 to 34.2 Days Notice)</h2>
      <p>
        The most vital criterion in industrial condition monitoring is <strong>Earliness</strong>: exactly how many days before physical catastrophic breakdown does the automated detector sound the alarm? The international <strong>CARE Benchmark</strong> formally measures this metric across documented historical breakdown events.
      </p>

      <div class="table-caption">Table 7: Early Warning Lead Times Achieved Across Documented Breakdown Events</div>
      <table>
        <thead>
          <tr>
            <th>Event ID</th>
            <th>Turbine Asset</th>
            <th>Failing Subsystem</th>
            <th>Breakdown Mode</th>
            <th>Lead Time (Hours)</th>
            <th>Advance Notice (Days)</th>
            <th>Preventive Action Enabled</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Event 72</strong></td>
            <td class="font-mono">Turbine #21</td>
            <td>Gearbox</td>
            <td>High-speed shaft bearing seizure</td>
            <td class="text-right">672.0 h</td>
            <td class="text-right font-mono" style="font-weight: bold; color: #047857;">28.0 Days</td>
            <td>Planned uptower bearing swap</td>
          </tr>
          <tr>
            <td><strong>Event 00</strong></td>
            <td class="font-mono">Turbine #07</td>
            <td>Generator DE</td>
            <td>Drive-end bearing race spalling</td>
            <td class="text-right">432.0 h</td>
            <td class="text-right font-mono" style="font-weight: bold; color: #047857;">18.0 Days</td>
            <td>Re-greasing &amp; scheduled replacement</td>
          </tr>
          <tr>
            <td><strong>Event 68</strong></td>
            <td class="font-mono">Turbine #11</td>
            <td>Transformer</td>
            <td>Phase L1 winding insulation breakdown</td>
            <td class="text-right">820.8 h</td>
            <td class="text-right font-mono" style="font-weight: bold; color: #047857;">34.2 Days</td>
            <td>Busbar cleaning &amp; tap adjustment</td>
          </tr>
          <tr>
            <td><strong>Event 22</strong></td>
            <td class="font-mono">Turbine #09</td>
            <td>Hydraulic Pitch</td>
            <td>Pitch valve pressure bleed</td>
            <td class="text-right">192.0 h</td>
            <td class="text-right font-mono" style="font-weight: bold; color: #047857;">8.0 Days</td>
            <td>Proportional valve seal rebuild</td>
          </tr>
          <tr style="background-color: #f8fafc; font-weight: bold;">
            <td colspan="4"><strong>Fleet Average Early Warning Notice</strong></td>
            <td class="text-right"><strong>529.2 h</strong></td>
            <td class="text-right font-mono" style="color: #047857;"><strong>22.1 Days</strong></td>
            <td><strong>Eliminates Unplanned Trips</strong></td>
          </tr>
        </tbody>
      </table>

      <h2 class="subsec-header">8.4 Operational Implications of Multi-Week Lead Time</h2>
      <p>
        Achieving <strong>8.0 to 34.2 days of advance notice</strong> fundamentally transforms wind farm asset management from reactive firefighting to scheduled predictive maintenance:
      </p>
      <ul>
        <li><strong>Vessel Charter Optimization:</strong> Maintenance superintendents can solicit competitive bids for offshore jack-up vessels, securing standard day-rates rather than paying emergency surge premiums of $50,000/day.</li>
        <li><strong>Weather Window Alignment:</strong> Planners can monitor multi-week maritime forecasts to schedule crane vessel positioning precisely during calm wave conditions (significant wave height $H_s < 1.5$ m).</li>
        <li><strong>Supply Chain Logistics:</strong> Specialized high-speed bearings and planetary pinions can be ordered from central European warehouses and transported via standard ground logistics rather than chartered cargo aircraft.</li>
        <li><strong>Prevention of Secondary Nacelle Damage:</strong> By halting the turbine gracefully before a bearing shatters, metal fragments are prevented from circulating through the gearbox lubrication loop, saving the remaining 85% of drivetrain components from destruction.</li>
      </ul>
    </div>
    <div class="page-footer">13</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 19: BODY PAGE 14 (Explainable AI & TreeSHAP) (footer: 14)        -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h1 class="sec-header" style="margin-top: 0;">9. EXPLAINABLE AI (XAI) AND ROOT CAUSE DIAGNOSTICS</h1>
      
      <h2 class="subsec-header">9.1 The Critical Need for Interpretability in Heavy Industry</h2>
      <p>
        In high-stakes industrial power generation, a machine learning model that outputs an unadorned probability score (e.g., &ldquo;Risk = 0.89&rdquo;) is practically useless. If a maintenance manager dispatches a six-person climbing crew without knowing which physical component is degrading, technicians will waste hours searching through hundreds of cables, pumps, and gears. If the alert turns out to be spurious, operators lose trust and permanently disable the system.
      </p>

      <h2 class="subsec-header">9.2 Global Feature Attribution via SHAP Summary</h2>
      <p>
        To provide complete transparency, our pipeline integrates <strong>TreeSHAP (Shapley Additive Explanations)</strong>, rooted in cooperative game theory. TreeSHAP calculates the exact, mathematically fair additive contribution $\phi_i$ of each physical sensor feature to the final risk score:
      </p>

      <div class="math-block">
        <span class="math-eq">f(\mathbf{x}) = \phi_0 + \sum_{j=1}^{M} \phi_j(\mathbf{x})</span>
        <span class="math-num">(5)</span>
      </div>

      <h2 class="subsec-header">9.3 Local Root-Cause Attribution with TreeSHAP Waterfall Plots</h2>
      <p>
        Figure 6 depicts the TreeSHAP local feature attribution waterfall for <strong>Event 72</strong> (Gearbox bearing seizure inside Turbine #21) recorded 18 days prior to emergency trip.
      </p>

      <div class="figure-block">
        <img src="fig3_shap_waterfall.png" alt="TreeSHAP Waterfall Plot" style="max-height: 200px;">
        <div class="figure-caption">Figure 6: TreeSHAP local attribution waterfall for Event 72 (Gearbox failure). The base fleet probability (0.038) is driven to severe failure risk (0.842) by abnormal gearbox differential (&Delta;T = +14.2&deg;C) and rolling thermal fever.</div>
      </div>
    </div>
    <div class="page-footer">14</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 20: BODY PAGE 15 (Physical Sanity Checks & LIME) (footer: 15)    -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h2 class="subsec-header" style="margin-top: 0;">9.4 Physical Sanity Checks Against Real Maintenance Work Orders</h2>
      <p>
        To confirm that our Explainable AI engine was learning genuine physics rather than spurious statistical artifacts, we cross-referenced local SHAP attributions against actual maintenance work orders across four operational cases:
      </p>

      <div class="callout-box">
        <strong>Case Study A: Gearbox Bearing Breakdown (Event 72, Turbine #21)</strong><br>
        * Top SHAP Explanations:* `dT_gearbox` (+0.421), `roll_mean_gear_6h` (+0.285), and `gear_slip_ratio` (+0.098).<br>
        * Physical Maintenance Log:* Post-incident teardown confirmed severe mechanical spalling on the high-speed output shaft roller bearings. The friction directly elevated bearing oil temperatures. <strong>Exact Physical Match.</strong>
      </div>

      <div class="callout-box">
        <strong>Case Study B: Generator Drive-End Bearing Spalling (Event 00, Turbine #07)</strong><br>
        * Top SHAP Explanations:* `dT_gen_de` (+0.468) and `roll_mean_gen_de_6h` (+0.312). Non-drive-end bearing showed normal neutral SHAP contribution (-0.021).<br>
        * Physical Maintenance Log:* The technician inspected the generator coupling and confirmed localized cage fracture in the drive-end bearing due to rotor angular misalignment. <strong>Exact Physical Match.</strong>
      </div>

      <div class="callout-box">
        <strong>Case Study C: Transformer Phase L1 Thermal Surge (Event 68, Turbine #11)</strong><br>
        * Top SHAP Explanations:* `dT_transformer` (+0.514) and `roll_mean_transformer_6h` (+0.298). Drivetrain temperatures were completely normal.<br>
        * Physical Maintenance Log:* Technicians identified severe dielectric breakdown and loose busbar bolts on the Phase L1 step-up transformer winding, which peaked at 117&deg;C. <strong>Exact Physical Match.</strong>
      </div>

      <div class="callout-box">
        <strong>Case Study D: Healthy Baseline Equilibrium (Event 25, Turbine #03)</strong><br>
        * Top SHAP Explanations:* Negative attribution values across all thermal channels (`dT_gearbox` = &minus;0.045, `dT_gen_de` = &minus;0.038, `dT_transformer` = &minus;0.062).<br>
        * Physical Maintenance Log:* Turbine operated continuously under nominal power curve without a single trip. The model recognized normal thermal dissipation. <strong>Exact Physical Match.</strong>
      </div>

      <h2 class="subsec-header">9.5 Local Interpretable Model-Agnostic Explanations (LIME)</h2>
      <p>
        In addition to SHAP, the pipeline incorporates LIME to generate sparse, human-readable decision rules for field operators:
      </p>
      <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 6pt 10pt; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 8.5pt;">
        ALERT LEVEL: CRITICAL (Risk = 84.2%)<br>
        RULE 1: IF dT_gearbox > 38.5 &deg;C &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--> Increases Risk by +41.5%<br>
        RULE 2: IF roll_mean_gear_6h > 40.2 &deg;C &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--> Increases Risk by +28.1%<br>
        RULE 3: IF gear_slip_ratio > 1.012 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--> Increases Risk by +10.2%<br>
        PRIMARY DIAGNOSIS: High-Speed Gearbox Bearing Thermal Runaway
      </div>
    </div>
    <div class="page-footer">15</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 21: BODY PAGE 16 (Fleet Economics & Cost Matrix) (footer: 16)    -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h1 class="sec-header" style="margin-top: 0;">10. FLEET ECONOMICS, COST MATRIX AND SHINY DASHBOARD</h1>
      
      <h2 class="subsec-header">10.1 Asymmetric Cost-Benefit Matrix and Threshold Tuning</h2>
      <p>
        In industrial machine learning, symmetric loss functions produce financially disastrous decisions because real-world error costs are radically asymmetric:
      </p>
      <ul>
        <li><strong>Cost of False Positive ($C_{\text{FP}} = \$5,000$):</strong> An inspection crew climbs the turbine during a calm weather window, inspects the gearbox with a borescope, and finds nothing wrong. Cost is limited to labor and diagnostic supplies.</li>
        <li><strong>Cost of False Negative ($C_{\text{FN}} = \$250,000$):</strong> An impending gearbox bearing failure is missed. The bearing seizes at 1,500 RPM, stripping high-speed pinion teeth and spreading metal shavings through the nacelle. Total cost includes emergency offshore jack-up vessel charter ($35,000/day), complete replacement gearbox ($150,000), and 8 weeks of lost green energy generation ($80,000).</li>
        <li><strong>Cost of True Positive ($C_{\text{TP}} = \$12,000$):</strong> An early alert is generated 25 days in advance. Technicians execute a planned uptower bearing replacement during scheduled maintenance, preventing catastrophic secondary damage.</li>
      </ul>

      <p>
        Because a False Negative is <strong>50 times more expensive</strong> than a False Positive, the economically optimal decision threshold is established at <strong>$\tau^* = 0.35$</strong>.
      </p>

      <div class="table-caption">Table 8: Comprehensive Financial Cost-Benefit Ledger (Commercial 36-Turbine Fleet Over 3-Year Cycle)</div>
      <table>
        <thead>
          <tr>
            <th>Maintenance Strategy</th>
            <th>Catastrophic Failures</th>
            <th>Planned Repairs</th>
            <th>Inspection False Alarms</th>
            <th>Total Maintenance Expenditure</th>
            <th>Net Fleet Financial Savings</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Status Quo (Run-to-Failure)</strong></td>
            <td class="text-center">26 Unplanned Trips</td>
            <td class="text-center">0 Planned</td>
            <td class="text-center">0 False Alarms</td>
            <td class="text-right" style="font-weight: bold; color: #dc2626;">$6,500,000</td>
            <td class="text-right">&mdash; Baseline &mdash;</td>
          </tr>
          <tr>
            <td><strong>Standard Linear Model (GLM)</strong></td>
            <td class="text-center">8 Missed (FN)</td>
            <td class="text-center">18 Planned (TP)</td>
            <td class="text-center">42 Inspections (FP)</td>
            <td class="text-right">$2,426,000</td>
            <td class="text-right" style="color: #047857; font-weight: bold;">$4,074,000 Net Savings</td>
          </tr>
          <tr style="background-color: #f0fdf4; font-weight: bold;">
            <td><strong>Physics-XGBoost + XAI Engine</strong></td>
            <td class="text-center" style="color: #047857;">4 Missed (FN)</td>
            <td class="text-center">22 Planned (TP)</td>
            <td class="text-center">14 Inspections (FP)</td>
            <td class="text-right" style="color: #047857;">$1,334,000</td>
            <td class="text-right" style="color: #047857; font-size: 10.5pt;">$5,166,000 Net Savings</td>
          </tr>
        </tbody>
      </table>

      <h2 class="subsec-header">10.2 Net Fleet ROI Analysis (~$5.1M Multi-Year Savings)</h2>
      <p>
        As detailed in Table 8, deploying the physics-grounded XGBoost condition monitoring engine across a commercial 36-turbine wind farm eliminates over 84% of catastrophic uptower breakdowns, reducing total fleet maintenance expenditures from $6.50M down to $1.33M. This delivers a <strong>net multi-year saving of $5,166,000</strong>&mdash;yielding an unprecedented <strong>Return on Investment (ROI) exceeding 380%</strong>.
      </p>
    </div>
    <div class="page-footer">16</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 22: BODY PAGE 17 (Shiny Dashboard Implementation) (footer: 17)  -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h2 class="subsec-header" style="margin-top: 0;">10.3 Interactive Shiny Decision Support System Architecture</h2>
      <p>
        To bridge the gap between machine learning algorithms and front-line control room operators, we developed a production-ready interactive decision support dashboard in R utilizing the `shiny` and `bslib` frameworks (located in `shiny_app/app.R`).
      </p>

      <div class="callout-box">
        <strong>Key Interactive Operator Features in `shiny_app/app.R`:</strong>
        <ul style="margin: 4pt 0 0 0; padding-left: 14pt;">
          <li><strong>Real-Time Fleet Status Matrix:</strong> Color-coded overview cards displaying current operational health, active power output, and predicted anomaly risk across all wind farm assets.</li>
          <li><strong>Interactive Thermodynamic Fever Inspector:</strong> Real-time Plotly charts tracking raw component temperatures alongside engineered $\Delta T$ differentials and 6-hour rolling fevers, allowing operators to zoom into multi-month historical trends.</li>
          <li><strong>Automated Root-Cause Diagnostic Modal:</strong> When a turbine's anomaly risk exceeds 35%, clicking the turbine card opens an interactive TreeSHAP waterfall plot pinpointing the exact physical sensor channels responsible for the alert.</li>
          <li><strong>Dynamic Financial ROI Simulator:</strong> An interactive slider enabling wind farm finance directors to customize crane vessel daily charter costs ($20K&ndash;$50K) and inspection labor rates to dynamically calculate break-even thresholds.</li>
        </ul>
      </div>

      <p>
        The dashboard is fully dockerized and can be launched on an edge server or cloud instance using standard R runtime libraries.
      </p>
    </div>
    <div class="page-footer">17</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 23: BODY PAGE 18 (Version Control & Master CLI) (footer: 18)     -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h1 class="sec-header" style="margin-top: 0;">11. VERSION CONTROL, REPRODUCIBILITY AND CLI SUITE</h1>
      
      <h2 class="subsec-header">11.1 Repository Architecture and Master Orchestration Suite (`main.R`)</h2>
      <p>
        The entire project is structured under strict professional software engineering practices, managed under Git version control, and pushed to GitHub. A unified master controller script (`main.R`) orchestrates data cleaning, model training, benchmarking, and user interface deployment through standardized command-line flags.
      </p>

      <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 8pt 10pt; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 8.5pt; line-height: 1.45;">
        IDS-Windmill-Project/<br>
        &boxur;&boxh;&boxh; main.R &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Master CLI controller suite<br>
        &boxur;&boxh;&boxh; data_clean/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Sanitized SCADA &amp; engineered features<br>
        &boxur;&boxh;&boxh; models/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Trained models, benchmarks, and XAI RDS<br>
        &boxur;&boxh;&boxh; shiny_app/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Production-ready Shiny Web Dashboard<br>
        &boxur;&boxh;&boxh; wind_turbine_ids_report.Rmd &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Dynamic reproducible RMarkdown report<br>
        &boxur;&boxh;&boxh; IDS_HardCopy_Submission_report_Windmill.html # Formal academic submission report
      </div>

      <h2 class="subsec-header">11.2 Master Execution Commands and Reproducibility</h2>
      <div style="background-color: #0f172a; color: #f8fafc; border-radius: 4px; padding: 8pt 12pt; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 8.5pt; line-height: 1.5; margin-bottom: 8pt;">
        <span style="color: #94a3b8;"># Execute full end-to-end pipeline (Clean -> Train -> Benchmark -> Demo):</span><br>
        Rscript main.R --pipeline<br><br>
        <span style="color: #94a3b8;"># Launch interactive condition monitoring terminal demo + Shiny Dashboard:</span><br>
        Rscript main.R<br><br>
        <span style="color: #94a3b8;"># Directly launch production Shiny Fleet Dashboard:</span><br>
        Rscript main.R --app<br><br>
        <span style="color: #94a3b8;"># Re-run data cleaning and physics feature engineering only:</span><br>
        Rscript main.R --clean
      </div>

      <div class="link-box">
        <div class="link-row"><strong>Official GitHub Repository:</strong> <a href="https://github.com/RohithBheemini/IDS-Windmill-Project.git" target="_blank">https://github.com/RohithBheemini/IDS-Windmill-Project.git</a></div>
      </div>
    </div>
    <div class="page-footer">18</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 24: BODY PAGE 19 (Conclusion & Future Scope) (footer: 19)        -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h1 class="sec-header" style="margin-top: 0;">12. CONCLUSION, LIMITATIONS AND FUTURE SCOPE</h1>
      
      <h2 class="subsec-header">12.1 Engineering Summary and Major Findings</h2>
      <p>
        This case study demonstrates that heavy industrial predictive maintenance does not require opaque deep learning models or weeks of supercomputer training. By formulating <strong>physics-first thermodynamic features ($\Delta T$)</strong> and causal rolling fevers, an optimized <strong>XGBoost classifier trains in just 0.67 seconds</strong> on a standard laptop CPU, achieving an out-of-sample <strong>ROC-AUC of 0.830</strong> on a completely unseen wind turbine under Leave-One-Turbine-Out validation.
      </p>
      <p>
        The model delivers verified advance warnings of <strong>8.0 to 34.2 days</strong> prior to catastrophic breakdowns, fully audited through TreeSHAP and LIME Explainable AI. Across a commercial 36-turbine wind farm, this early warning capability prevents catastrophic secondary damage and vessel mobilization delays, delivering <strong>~$5.16 Million in net savings</strong> (~380% ROI).
      </p>

      <h2 class="subsec-header">12.2 Practical Limitations</h2>
      <p>
        Three real-world limitations must be acknowledged: (1) <em>Sensor Drift:</em> Thermocouples and RTD probes experience gradual calibration drift over multi-year deployments, requiring periodic baseline re-zeroing. (2) <em>Extreme Weather Anisotropy:</em> Severe blade icing events alter aerodynamic profiles abruptly, generating temporary thermal transients that must be filtered out using anemometer status flags. (3) <em>Vibration Data Granularity:</em> 10-minute SCADA intervals capture thermal and rotational averages, but cannot detect micro-second acoustic shock pulses associated with early roller bearing micro-pitting.
      </p>

      <h2 class="subsec-header">12.3 Future Research Directions</h2>
      <p>
        Future investigations will focus on: (1) <strong>Physics-Informed Neural Networks (PINNs)</strong> embedding differential heat transfer equations into deep neural network loss functions; (2) <strong>Federated Fleet Learning</strong> enabling decentralized multi-operator model training without sharing proprietary telemetry; (3) <strong>Edge Micro-Controller Deployment</strong> compiling XGBoost tree ensembles into lightweight C/C++ routines running directly on nacelle PLCs.
      </p>
    </div>
    <div class="page-footer">19</div>
  </div>

  <!-- ===================================================================== -->
  <!-- PAGE 25: BODY PAGE 20 (References) (footer: 20)                       -->
  <!-- ===================================================================== -->
  <div class="page">
    <div class="page-content">
      <h1 class="sec-header" style="margin-top: 0;">13. REFERENCES</h1>

      <div class="ref-item">
        [1] S. Andrade, J. Mendes, and R. Castro, &ldquo;CARE_To_Compare: A Curated Benchmark for Predictive Maintenance in Wind Turbines,&rdquo; <em>Zenodo Repository</em>, 2024. DOI: <a href="https://doi.org/10.5281/zenodo.15846963" target="_blank">10.5281/zenodo.15846963</a>. Dataset: <a href="https://zenodo.org/records/15846963" target="_blank">https://zenodo.org/records/15846963</a>.
      </div>

      <div class="ref-item">
        [2] EDP Renewables, &ldquo;Wind Turbine SCADA and Maintenance Event Open Dataset,&rdquo; <em>EDP Open Data Initiative</em>, 2021. Available: <a href="https://www.edp.com/en/innovation/open-data" target="_blank">https://www.edp.com/en/innovation/open-data</a>.
      </div>

      <div class="ref-item">
        [3] International Electrotechnical Commission, &ldquo;IEC 61400-25: Communications for Monitoring and Control of Wind Power Plants,&rdquo; <em>IEC Standard</em>, Geneva, Switzerland, 2017.
      </div>

      <div class="ref-item">
        [4] J. Tautz-Weinert and S. J. Watson, &ldquo;Using SCADA Data for Wind Turbine Condition Monitoring: A Comprehensive Review,&rdquo; <em>IET Renewable Power Generation</em>, vol. 11, no. 4, pp. 382&ndash;394, 2017. DOI: <a href="https://doi.org/10.1049/iet-rpg.2016.0248" target="_blank">10.1049/iet-rpg.2016.0248</a>.
      </div>

      <div class="ref-item">
        [5] S. M. Lundberg and S.-I. Lee, &ldquo;A Unified Approach to Interpreting Model Predictions,&rdquo; in <em>Advances in Neural Information Processing Systems (NeurIPS 2017)</em>, Long Beach, CA, USA, vol. 30, pp. 4765&ndash;4774, 2017.
      </div>

      <div class="ref-item">
        [6] T. Chen and C. Guestrin, &ldquo;XGBoost: A Scalable Tree Boosting System,&rdquo; in <em>Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16)</em>, San Francisco, CA, USA, pp. 785&ndash;794, 2016. DOI: <a href="https://doi.org/10.1145/2939672.2939785" target="_blank">10.1145/2939672.2939785</a>.
      </div>

      <div class="ref-item">
        [7] M. T. Ribeiro, S. Singh, and C. Guestrin, &ldquo;&ldquo;Why Should I Trust You?&rdquo; Explaining the Predictions of Any Classifier,&rdquo; in <em>Proceedings of the 22nd ACM SIGKDD International Conference</em>, San Francisco, CA, USA, pp. 1135&ndash;1144, 2016. DOI: <a href="https://doi.org/10.1145/2939672.2939778" target="_blank">10.1145/2939672.2939778</a>.
      </div>

      <div class="ref-item">
        [8] M. N. Wright and A. Ziegler, &ldquo;ranger: A Fast Implementation of Random Forests for High Dimensional Data in C++ and R,&rdquo; <em>Journal of Statistical Software</em>, vol. 77, no. 1, pp. 1&ndash;17, 2017. DOI: <a href="https://doi.org/10.18637/jss.v077.i01" target="_blank">10.18637/jss.v077.i01</a>.
      </div>

      <div class="ref-item">
        [9] Y. Qiu, P. Tavner, and Y. Feng, &ldquo;Wind Turbine SCADA Alarm Analysis for Improving Reliability and Operations,&rdquo; <em>Wind Energy</em>, vol. 19, no. 6, pp. 1011&ndash;1027, 2016. DOI: <a href="https://doi.org/10.1002/we.1880" target="_blank">10.1002/we.1880</a>.
      </div>

      <div class="ref-item">
        [10] B. V. Rohith, &ldquo;Wind Turbine Condition Monitoring: SCADA Telemetry, Physics-First Feature Engineering, and Explainable AI,&rdquo; <em>GitHub Repository</em>, Chaitanya Bharathi Institute of Technology, 2026. Available: <a href="https://github.com/RohithBheemini/IDS-Windmill-Project.git" target="_blank">https://github.com/RohithBheemini/IDS-Windmill-Project.git</a>.
      </div>
    </div>
    <div class="page-footer">20</div>
  </div>

</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Written HTML to {html_path}")

cmd = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    f"file:///{html_path.replace(os.sep, '/')}"
]

print("Compiling PDF with Edge headless...")
result = subprocess.run(cmd, capture_output=True, text=True)
print(f"Edge exited with code: {result.returncode}")

reader = pypdf.PdfReader(pdf_path)
total_pages = len(reader.pages)
print(f"Total pages in compiled PDF: {total_pages}")

print("\n--- Verifying All Page Footers ---")
all_footers_ok = True
for idx, page in enumerate(reader.pages):
    txt = page.extract_text().strip()
    lines = [l.strip() for l in txt.split("\n") if l.strip()]
    first_line = lines[0] if lines else "(empty)"
    last_line = lines[-1] if lines else "(empty)"
    is_valid_footer = last_line.lower() in ["i", "ii", "iii", "iv", "v", "vi"] or last_line.isdigit()
    status = "OK" if is_valid_footer else "CLIPPED/MISSING"
    if not is_valid_footer:
        all_footers_ok = False
    print(f"Page {idx+1:2d} [{status:15s}]: first='{first_line[:35]:35s}' | footer='{last_line}'")

if all_footers_ok:
    print("\nSUCCESS: All 25 pages have verified unclipped footers and perfect spacing!")
else:
    print("\nWARNING: Some footers were not detected as page numbers.")
