# scripts/create_presentation.py
# Generates a minimal, humanized, large-font PPTX presentation for the Wind Turbine Case Study
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path="presentation_wind_turbine_ids.pptx"):
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Palette
    C_BG = RGBColor(248, 250, 252)         # Off-white / slate 50
    C_CARD = RGBColor(255, 255, 255)       # Pure white
    C_CARD_BORDER = RGBColor(226, 232, 240) # Slate 200
    C_TEXT_MAIN = RGBColor(15, 23, 42)     # Slate 900
    C_TEXT_MUTED = RGBColor(71, 85, 105)   # Slate 600
    C_PRIMARY = RGBColor(2, 132, 199)      # Sky 600
    C_NAVY = RGBColor(30, 58, 138)         # Blue 900
    C_DANGER = RGBColor(220, 38, 38)       # Red 600
    C_SUCCESS = RGBColor(22, 163, 74)      # Green 600
    C_WARNING = RGBColor(217, 119, 6)      # Amber 600
    
    blank_layout = prs.slide_layouts[6]
    
    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background() # no line
        return bg

    def add_header(slide, tag_text, title_text, subtitle_text=None):
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(13)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_PRIMARY
        
        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(30)
        p_title.font.bold = True
        p_title.font.color.rgb = C_TEXT_MAIN
        
        # Subtitle
        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(11.7), Inches(0.45))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle_text
            p_sub.font.size = Pt(17)
            p_sub.font.color.rgb = C_TEXT_MUTED

    def add_card(slide, left, top, width, height, border_color=C_CARD_BORDER, bg_color=C_CARD):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Clean, Minimal, High-Impact)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    
    # Hero Title Box
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.0))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    
    p0 = tf1.paragraphs[0]
    p0.text = "WIND TURBINE CONDITION MONITORING"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = C_PRIMARY
    p0.space_after = Pt(16)
    
    p1 = tf1.add_paragraph()
    p1.text = "Saving Millions in the Wind"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT_MAIN
    
    p2 = tf1.add_paragraph()
    p2.text = "How Physics, Machine Learning & Explainable AI Spot Failures Weeks in Advance"
    p2.font.size = Pt(22)
    p2.font.color.rgb = C_TEXT_MUTED
    p2.space_before = Pt(12)
    p2.space_after = Pt(28)
    
    p3 = tf1.add_paragraph()
    p3.text = "A Simplified Case Study: Foundations, Realized Approaches & Alternative Paths"
    p3.font.size = Pt(16)
    p3.font.bold = True
    p3.font.color.rgb = C_NAVY

    # =========================================================================
    # SLIDE 2: THE REAL-WORLD PROBLEM (Why This Matters)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Operational Reality", "The High Stakes of Wind Turbine Breakdowns", 
               "Why traditional reactive maintenance fails catastrophically at sea")
    
    # 3 Column Cards
    col_w = Inches(3.64)
    h_top = Inches(2.1)
    c_h = Inches(4.7)
    
    # Card 1: The Mechanical Monster
    add_card(s2, Inches(0.8), h_top, col_w, c_h)
    tb = s2.shapes.add_textbox(Inches(1.0), h_top + Inches(0.2), col_w - Inches(0.4), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "The Machine"
    p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_NAVY; p.space_after = Pt(14)
    
    bullets = [
        "Turbines are 300-ft tall robotic power plants with 80-meter blades.",
        "Internal components operate under titanic mechanical torque & cyclic stress.",
        "A 20-ton gearbox steps up rotor speed from 15 RPM to 1,500 RPM for the generator."
    ]
    for b in bullets:
        bp = tf.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(16); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(10)
        
    # Card 2: The Catastrophic Cost
    add_card(s2, Inches(4.84), h_top, col_w, c_h, border_color=C_DANGER)
    tb = s2.shapes.add_textbox(Inches(5.04), h_top + Inches(0.2), col_w - Inches(0.4), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "The Catastrophe"
    p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_DANGER; p.space_after = Pt(14)
    
    bullets = [
        "Offshore crane ships cost $30,000+ per day just to mobilize.",
        "Replacing shattered gearboxes costs $150,000 to $250,000+ in parts.",
        "Rough winter seas can delay repairs for 6 to 8 weeks, losing hundreds of thousands in green power."
    ]
    for b in bullets:
        bp = tf.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(16); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(10)
        
    # Card 3: The Mission
    add_card(s2, Inches(8.88), h_top, col_w, c_h, border_color=C_SUCCESS)
    tb = s2.shapes.add_textbox(Inches(9.08), h_top + Inches(0.2), col_w - Inches(0.4), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "The Goal"
    p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_SUCCESS; p.space_after = Pt(14)
    
    bullets = [
        "Spot component degradation 2 to 4 weeks before catastrophic failure.",
        "Use existing SCADA temperature and speed sensors without new hardware.",
        "Avoid false alarm fatigue so technicians genuinely trust the alerts."
    ]
    for b in bullets:
        bp = tf.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(16); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(10)

    # =========================================================================
    # SLIDE 3: DATASET COMPLETE DETAILS (What Data We Had)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Dataset Anatomy", "Understanding the Benchmark (CARE_To_Compare)",
               "89 years of real-world operational SCADA telemetry across 36 wind turbines")
    
    # 2 Wide Cards
    top_c = Inches(2.1)
    card_w = Inches(5.66)
    card_h = Inches(4.7)
    
    # Left Card: The Data Scale & Farms
    add_card(s3, Inches(0.8), top_c, card_w, card_h)
    tb = s3.shapes.add_textbox(Inches(1.1), top_c + Inches(0.3), card_w - Inches(0.6), card_h - Inches(0.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "The Multi-Farm Architecture"
    p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_NAVY; p.space_after = Pt(16)
    
    items = [
        ("Wind Farm A (Portugal, Onshore):", "5 turbines, 22 datasets, 86 sensor channels. Transparent component breakdown from EDP Open Data."),
        ("Wind Farm B (Germany, Offshore):", "15 datasets, 257 sensor channels. Severe marine environment, rotor bearing & transformer cell issues."),
        ("Wind Farm C (Germany, Offshore):", "58 datasets, 957 sensor channels. Deep telemetry (pitch motors, converter IGBTs, blade heaters)."),
        ("10-Minute Averaging (IEC 61400-25):", "Raw milliseconds are aggregated into 10-minute average, min, max, and std deviation.")
    ]
    for title, desc in items:
        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(16); p1.font.bold = True; p1.font.color.rgb = C_PRIMARY; p1.space_before = Pt(6)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(15); p2.font.color.rgb = C_TEXT_MAIN; p2.space_after = Pt(8)

    # Right Card: The Events & Ground Truth
    add_card(s3, Inches(6.86), top_c, card_w, card_h)
    tb = s3.shapes.add_textbox(Inches(7.16), top_c + Inches(0.3), card_w - Inches(0.6), card_h - Inches(0.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Structure of Each Monitored Event"
    p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_NAVY; p.space_after = Pt(16)
    
    items_r = [
        ("Historical Baseline (train):", "Exactly 1 full year (~52,000 observations) of normal healthy historical operation for that specific turbine."),
        ("Evaluation Window (prediction):", "The subsequent 2 to 4 weeks. In anomaly datasets, degradation worsens leading to failure; in normal datasets, turbine keeps running."),
        ("Component Failure Modes:", "Ground-truth failure logs catalog Gearbox breakdowns, Generator bearing wear, Transformer surges, and Hydraulic valve failures."),
        ("Balanced Benchmark:", "44 labeled anomaly failure cases vs. 51 healthy normal control cases across the full repository.")
    ]
    for title, desc in items_r:
        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(16); p1.font.bold = True; p1.font.color.rgb = C_SUCCESS; p1.space_before = Pt(6)
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(15); p2.font.color.rgb = C_TEXT_MAIN; p2.space_after = Pt(8)

    # =========================================================================
    # SLIDE 4: THEORETICAL CHALLENGE 1 — STATUS CODE LEAKAGE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Theoretical Challenge 1", "The 'Status Code' Trap (Data Leakage)",
               "Why a naive machine learning model achieves 99.9% accuracy but fails in operations")
    
    # 2 Comparison Boxes
    c_w = Inches(5.66)
    add_card(s4, Inches(0.8), Inches(2.1), c_w, Inches(4.7), border_color=C_DANGER)
    tb = s4.shapes.add_textbox(Inches(1.1), Inches(2.4), c_w - Inches(0.6), Inches(4.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "The Naive Shortcut (The Cheat)"; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_DANGER; p.space_after = Pt(14)
    
    bullets = [
        "In raw SCADA files, 'status_type_id' records turbine states: 0 = Normal, 3 = Service, 4 = Downtime.",
        "When an anomaly dataset reaches breakdown, the status flips to 4 (Turbine is halted).",
        "A standard AI automatically latches onto status_type_id == 4 and claims 99.9% accuracy.",
        "WHY THIS IS USELESS: The wind farm already knows the turbine is down when it trips! Predicting downtime after the machine stops spinning has zero business value."
    ]
    for b in bullets:
        bp = tf.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(16); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(10)

    add_card(s4, Inches(6.86), Inches(2.1), c_w, Inches(4.7), border_color=C_SUCCESS)
    tb = s4.shapes.add_textbox(Inches(7.16), Inches(2.4), c_w - Inches(0.6), Inches(4.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "How We Resolved It (True Physics)"; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_SUCCESS; p.space_after = Pt(14)
    
    bullets_res = [
        "We strictly erased status_type_id from all predictive features.",
        "The model must learn failure signatures exclusively from thermodynamic temperatures, vibrations, and aerodynamics.",
        "The entire prediction period is evaluated to detect early degradation while status is STILL 0 (Normal operation).",
        "OPERATIONAL OUTCOME: The model provides genuine early warning days before the emergency control system ever trips."
    ]
    for b in bullets_res:
        bp = tf.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(16); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(10)

    # =========================================================================
    # SLIDE 5: THEORETICAL CHALLENGE 2 — WEATHER CONVOLUTION
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Theoretical Challenge 2", "The Weather Trap & The 'Rising Fever' Fix",
               "Is the bearing overheating, or is it just a sunny afternoon in July?")
    
    add_card(s5, Inches(0.8), Inches(2.1), c_w, Inches(4.7), border_color=C_WARNING)
    tb = s5.shapes.add_textbox(Inches(1.1), Inches(2.4), c_w - Inches(0.6), Inches(4.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "The Weather Confounding Problem"; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_WARNING; p.space_after = Pt(14)
    
    bullets = [
        "A healthy gearbox bearing naturally runs at 60°C on a hot 38°C summer afternoon.",
        "A dying gearbox bearing might only reach 45°C on a freezing 2°C winter morning.",
        "If you feed raw temperatures to an AI, it classifies summer as an anomaly and misses winter failures!",
        "THE SCIENTIFIC CHALLENGE: How do we isolate genuine internal mechanical friction from external weather?"
    ]
    for b in bullets:
        bp = tf.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(16); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(10)

    add_card(s5, Inches(6.86), Inches(2.1), c_w, Inches(4.7), border_color=C_PRIMARY)
    tb = s5.shapes.add_textbox(Inches(7.16), Inches(2.4), c_w - Inches(0.6), Inches(4.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "The Thermodynamic Solution (ΔT)"; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_PRIMARY; p.space_after = Pt(14)
    
    bullets_dt = [
        "Just like a doctor checks fever above normal room temperature, we engineered Differential Temperatures:",
        "ΔT = Component Temperature − Outside Ambient Temperature",
        "Subtracting ambient weather eliminates summer/winter bias and directly exposes bearing friction.",
        "Added Causal 6-Hour Moving Averages (RollMean 6h) to track sustained heat accumulation without future data leakage."
    ]
    for b in bullets_dt:
        bp = tf.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(16); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(10)

    # =========================================================================
    # SLIDE 6: THEORETICAL CHALLENGE 3 — UNSEEN TURBINES
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Theoretical Challenge 3", "Generalizing to Unseen Strangers (Turbines)",
               "Why random train/test splits lie, and how Leave-One-Turbine-Out validation proves reality")
    
    add_card(s6, Inches(0.8), Inches(2.1), c_w, Inches(4.7), border_color=C_DANGER)
    tb = s6.shapes.add_textbox(Inches(1.1), Inches(2.4), c_w - Inches(0.6), Inches(4.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "The Flaw of Random Splitting"; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_DANGER; p.space_after = Pt(14)
    
    bullets = [
        "Turbines are like human beings: each has slight individual baselines.",
        "Turbine #11 might naturally run 1.5°C warmer than Turbine #0 due to its position on a ridge.",
        "If you randomly shuffle 10-minute records, the AI simply memorizes individual turbine IDs rather than universal physics.",
        "When deployed on a newly installed turbine, such models fail completely."
    ]
    for b in bullets:
        bp = tf.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(16); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(10)

    add_card(s6, Inches(6.86), Inches(2.1), c_w, Inches(4.7), border_color=C_SUCCESS)
    tb = s6.shapes.add_textbox(Inches(7.16), Inches(2.4), c_w - Inches(0.6), Inches(4.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Leave-One-Turbine-Out Validation"; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_SUCCESS; p.space_after = Pt(14)
    
    bullets_loto = [
        "We erased turbine ID (asset_id) from all model input features.",
        "Enforced Leave-One-Turbine-Out Group Cross-Validation: Train on Turbines 0, 10, 11, 13 and evaluate on held-out Turbine 21.",
        "The model is forced to learn universal physical wear signatures that apply to ANY turbine.",
        "PROVEN RESULT: Achieved 0.83 Test AUC on completely unseen turbines in held-out validation."
    ]
    for b in bullets_loto:
        bp = tf.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(16); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(10)

    # =========================================================================
    # SLIDE 7: OUR IMPLEMENTED APPROACH
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Solution Architecture", "How We Built the Production System",
               "A streamlined, high-speed pipeline combining physics, ensembles, and explainability")
    
    # 4 Sequential Cards horizontally
    c4_w = Inches(2.72)
    c4_h = Inches(4.7)
    
    steps = [
        ("1. Data Hygiene", C_NAVY, [
            "Parsed semicolon delimiters.",
            "Audited 102M data points.",
            "Sparse NAs (<0.00004%) forward-filled with locf.",
            "Zero artificial values (no SMOTE)."
        ]),
        ("2. Physics Features", C_PRIMARY, [
            "Delta T differentials for Gearbox, Generator, Transformer.",
            "Causal 6h rolling averages.",
            "Gear ratio (Gen RPM / Rotor RPM).",
            "Cp power conversion proxy."
        ]),
        ("3. High-Speed Models", C_SUCCESS, [
            "Benchmarked GLM, Random Forest, and XGBoost.",
            "Sub-second training (<1 sec).",
            "Compact memory footprint (109 MB RAM).",
            "Group CV across turbines."
        ]),
        ("4. Explainability & UI", C_WARNING, [
            "Exact TreeSHAP attributions.",
            "LIME local decision rules.",
            "Physical consistency verification.",
            "Production Shiny dashboard."
        ])
    ]
    
    for i, (stitle, scolor, sbullets) in enumerate(steps):
        left_pos = Inches(0.8) + i * Inches(2.98)
        add_card(s7, left_pos, Inches(2.1), c4_w, c4_h, border_color=scolor)
        tb = s7.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.3), c4_w - Inches(0.4), c4_h - Inches(0.4))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = stitle; p.font.size = Pt(19); p.font.bold = True; p.font.color.rgb = scolor; p.space_after = Pt(14)
        for sb in sbullets:
            bp = tf.add_paragraph(); bp.text = "• " + sb; bp.font.size = Pt(15); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(10)

    # =========================================================================
    # SLIDE 8: OTHER APPROACHES CONSIDERED
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Alternative Approaches", "What Other Approaches Could We Consider?",
               "Evaluating deep learning, autoencoders, vibration FFTs, and synthetic sampling")
    
    # 4 Grid Cards (2x2)
    grid_w = Inches(5.66)
    grid_h = Inches(2.25)
    
    grid_items = [
        ("Approach A: Deep Time-Series (LSTM / GRU / Transformers)", Inches(0.8), Inches(2.1), C_NAVY,
         "Recurrent or attention networks modeling long sequential dependencies directly from raw time-steps."),
        ("Approach B: Unsupervised Autoencoders (Normal Behavior Modeling)", Inches(6.86), Inches(2.1), C_PRIMARY,
         "Neural networks trained only on healthy data to predict expected values; high reconstruction error signals fault."),
        ("Approach C: Classical Vibration Signal Processing (FFT / Envelope)", Inches(0.8), Inches(4.55), C_WARNING,
         "Fourier transforms and spectral analysis on high-frequency (kHz) accelerometers placed on bearing housings."),
        ("Approach D: Synthetic Minority Oversampling (SMOTE / GANs)", Inches(6.86), Inches(4.55), C_DANGER,
         "Algorithmic generation of artificial failure samples to balance positive and negative class ratios.")
    ]
    
    for atitle, aleft, atop, acolor, adesc in grid_items:
        add_card(s8, aleft, atop, grid_w, grid_h, border_color=acolor)
        tb = s8.shapes.add_textbox(aleft + Inches(0.25), atop + Inches(0.2), grid_w - Inches(0.5), grid_h - Inches(0.4))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = atitle; p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = acolor; p.space_after = Pt(8)
        p2 = tf.add_paragraph(); p2.text = adesc; p2.font.size = Pt(15); p2.font.color.rgb = C_TEXT_MAIN

    # =========================================================================
    # SLIDE 9: WHY WE REJECTED THEM & FUTURE SCOPE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Critical Evaluation", "Why We Didn't Choose Them & What Is Future Scope",
               "Clear justification of design trade-offs: what was rejected vs. what is a valuable future upgrade")
    
    # 2 Big Cards: Left = Rejected; Right = Future Scope
    add_card(s9, Inches(0.8), Inches(2.1), c_w, Inches(4.7), border_color=C_DANGER)
    tb = s9.shapes.add_textbox(Inches(1.1), Inches(2.4), c_w - Inches(0.6), Inches(4.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Rejected / Not Recommended"; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_DANGER; p.space_after = Pt(14)
    
    rej = [
        ("Synthetic Data (SMOTE/GANs): REJECTED", "Fabricates physically impossible operating states (e.g., power at zero wind). Ruled out to preserve physical validity."),
        ("Unsupervised Clustering (K-Means/PCA): NOT WORTH IT", "Produced intolerable false alarm rates on offshore weather outliers. Simple clustering lacks temporal context."),
        ("End-to-End Deep Learning for 10-Min SCADA: REJECTED", "With 22 total events, deep neural nets severely overfit, require heavy compute, and destroy interpretability.")
    ]
    for rtitle, rdesc in rej:
        p1 = tf.add_paragraph(); p1.text = rtitle; p1.font.size = Pt(16); p1.font.bold = True; p1.font.color.rgb = C_TEXT_MAIN; p1.space_before = Pt(4)
        p2 = tf.add_paragraph(); p2.text = rdesc; p2.font.size = Pt(14); p2.font.color.rgb = C_TEXT_MUTED; p2.space_after = Pt(8)

    add_card(s9, Inches(6.86), Inches(2.1), c_w, Inches(4.7), border_color=C_PRIMARY)
    tb = s9.shapes.add_textbox(Inches(7.16), Inches(2.4), c_w - Inches(0.6), Inches(4.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Valuable Future Scope"; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_PRIMARY; p.space_after = Pt(14)
    
    fut = [
        ("Physics-Informed Neural Networks (PINNs): FUTURE SCOPE", "Embedding Navier-Stokes and heat diffusion differential equations directly into loss functions for thermodynamic modeling."),
        ("High-Frequency Vibration Telemetry: FUTURE SCOPE", "Integrating 10-kHz accelerometer streams for bearing inner/outer race defect frequency analysis (BPFO/BPFI)."),
        ("Cross-Farm Transfer Learning: FUTURE SCOPE", "Domain-adaptation models transferring failure patterns learned from Farm A (Portugal) to offshore Farm C (Germany).")
    ]
    for ftitle, fdesc in fut:
        p1 = tf.add_paragraph(); p1.text = ftitle; p1.font.size = Pt(16); p1.font.bold = True; p1.font.color.rgb = C_PRIMARY; p1.space_before = Pt(4)
        p2 = tf.add_paragraph(); p2.text = fdesc; p2.font.size = Pt(14); p2.font.color.rgb = C_TEXT_MAIN; p2.space_after = Pt(8)

    # =========================================================================
    # SLIDE 10: THEORETICAL CHALLENGE 4 — EXPLAINABLE AI
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Theoretical Challenge 4", "The Black-Box Trust Problem: SHAP & LIME",
               "Why operators reject unexplained alerts and how XAI proved physical fidelity")
    
    # 3 Cards
    add_card(s10, Inches(0.8), Inches(2.1), col_w, c_h)
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.3), col_w - Inches(0.4), c_h - Inches(0.4))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "The Operator's Dilemma"; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = C_NAVY; p.space_after = Pt(12)
    bullets = [
        "If an AI flags a turbine as '90% Risk' without explanation, maintenance crews will ignore it.",
        "Technicians must know WHICH component to inspect: the gearbox, the generator, or the transformer?",
        "Black box predictions create distrust and alert fatigue."
    ]
    for b in bullets:
        bp = tf.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(15); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(8)

    add_card(s10, Inches(4.84), Inches(2.1), col_w, c_h, border_color=C_PRIMARY)
    tb = s10.shapes.add_textbox(Inches(5.04), Inches(2.3), col_w - Inches(0.4), c_h - Inches(0.4))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "How SHAP Solves It"; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = C_PRIMARY; p.space_after = Pt(12)
    bullets = [
        "TreeSHAP calculates exact additive Shapley values based on game theory.",
        "Allocates exact risk 'points' to every individual sensor channel.",
        "Global SHAP reveals fleet-wide thermal drift drivers.",
        "Local SHAP waterfalls explain the exact alert moment for a specific turbine."
    ]
    for b in bullets:
        bp = tf.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(15); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(8)

    add_card(s10, Inches(8.88), Inches(2.1), col_w, c_h, border_color=C_SUCCESS)
    tb = s10.shapes.add_textbox(Inches(9.08), Inches(2.3), col_w - Inches(0.4), c_h - Inches(0.4))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Ground Truth Match"; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = C_SUCCESS; p.space_after = Pt(12)
    bullets = [
        "GEARBOX (Ev 72): Top SHAP feature was gearbox bearing temperature (+4.3°C rise).",
        "GENERATOR (Ev 0): Drive-end bearing temperature surged to 76°C-94°C, triggering alarm.",
        "TRANSFORMER (Ev 68): Phase L1 reached 117°C, dominating local SHAP attributions.",
        "HEALTHY (Ev 25): Negative scores across all components (zero alarm)."
    ]
    for b in bullets:
        bp = tf.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(15); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(8)

    # =========================================================================
    # SLIDE 11: THEORETICAL CHALLENGE 5 — ASYMMETRIC COSTS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Theoretical Challenge 5", "Asymmetric Financial Economics & Thresholding",
               "Why standard 50% accuracy fails in operations, and how cost matrices save millions")
    
    add_card(s11, Inches(0.8), Inches(2.1), c_w, Inches(4.7), border_color=C_DANGER)
    tb = s11.shapes.add_textbox(Inches(1.1), Inches(2.4), c_w - Inches(0.6), Inches(4.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "The Asymmetric Cost Matrix"; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_DANGER; p.space_after = Pt(14)
    
    bullets = [
        "MISSED FAILURE (False Negative): $150,000 - $300,000. Shattered gearbox, offshore vessel chartering, 6 weeks lost power.",
        "FALSE ALARM (False Positive): $3,500. Remote log diagnostics and routine technician inspection visit.",
        "PLANNED REPAIR (True Positive): $8,000. Uptower bearing replacement during scheduled calm weather window.",
        "CRITICAL REALITY: Missing a breakdown is 40 TIMES MORE EXPENSIVE than sending a technician on a false alarm!"
    ]
    for b in bullets:
        bp = tf.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(16); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(10)

    add_card(s11, Inches(6.86), Inches(2.1), c_w, Inches(4.7), border_color=C_SUCCESS)
    tb = s11.shapes.add_textbox(Inches(7.16), Inches(2.4), c_w - Inches(0.6), Inches(4.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "The Cost-Optimal Threshold"; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_SUCCESS; p.space_after = Pt(14)
    
    bullets_opt = [
        "In textbooks, models use a 0.50 (50%) decision threshold.",
        "In wind energy, a 50% threshold allows too many catastrophic gearboxes to slip through.",
        "By plotting the Total Fleet Cost Curve, we discovered the economically optimal threshold is 0.30 - 0.35.",
        "This sweet spot catches impending failures 8 to 34 days early while keeping technician inspection costs under control."
    ]
    for b in bullets_opt:
        bp = tf.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(16); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(10)

    # =========================================================================
    # SLIDE 12: DEPLOYMENT & THE SHINY APPLICATION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Decision Support", "Deployment: The Production Shiny Dashboard",
               "Empowering wind farm operators and financial executives with interactive analytics")
    
    # 2 Cards: Left = Dashboard Features; Right = Architecture & Launcher
    add_card(s12, Inches(0.8), Inches(2.1), c_w, Inches(4.7), border_color=C_NAVY)
    tb = s12.shapes.add_textbox(Inches(1.1), Inches(2.4), c_w - Inches(0.6), Inches(4.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "5 Operational Dashboard Tabs"; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_NAVY; p.space_after = Pt(14)
    
    tabs = [
        ("1. Fleet Overview:", "Live status cards across 3 wind farms, turbine catalog & event registry."),
        ("2. SCADA Telemetry Studio:", "Multi-sensor time-series plots (Delta T, wind, power) + real-time risk timeline."),
        ("3. Model Benchmark & CARE:", "Leave-One-Turbine-Out validation stats, confusion matrix & lead times."),
        ("4. Explainable AI Studio:", "Interactive SHAP waterfall and LIME rules for every failure mode."),
        ("5. Business ROI Calculator:", "Interactive cost sliders calculating net fleet dollar savings.")
    ]
    for tname, tdesc in tabs:
        p1 = tf.add_paragraph(); p1.text = tname; p1.font.size = Pt(16); p1.font.bold = True; p1.font.color.rgb = C_PRIMARY; p1.space_before = Pt(4)
        p2 = tf.add_paragraph(); p2.text = tdesc; p2.font.size = Pt(14); p2.font.color.rgb = C_TEXT_MAIN; p2.space_after = Pt(6)

    add_card(s12, Inches(6.86), Inches(2.1), c_w, Inches(4.7), border_color=C_SUCCESS)
    tb = s12.shapes.add_textbox(Inches(7.16), Inches(2.4), c_w - Inches(0.6), Inches(4.1))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Deployment & Running Locally"; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = C_SUCCESS; p.space_after = Pt(14)
    
    bullets_run = [
        "BUILT WITH R & BSLIB: Modern industrial Darkly theme with responsive cards and SVG icons.",
        "INSTANT LAUNCH: One-click launcher script in the project root:",
        "  Rscript run_app.R",
        "Or inside an active R session / RStudio:",
        "  shiny::runApp('shiny_app')",
        "Runs on http://127.0.0.1:3838 with instant reactive plots, requiring zero cloud dependencies."
    ]
    for b in bullets_run:
        bp = tf.add_paragraph(); bp.text = b; bp.font.size = Pt(15); bp.font.color.rgb = C_TEXT_MAIN; bp.space_after = Pt(8)

    # =========================================================================
    # SLIDE 13: SUMMARY & PRESENTER CHEAT SHEET
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Summary & Key Takeaways", "The 5-Point Presenter's Cheat Sheet",
               "Everything you need to deliver a convincing, memorable presentation")
    
    # 5 Horizontal Cards
    card_take_h = Inches(0.85)
    points = [
        ("1. Real Physics, Not Fake Data", "Rejected synthetic SMOTE and purged post-trip status codes; 100% genuine sensor telemetry."),
        ("2. The 'Rising Fever' Method", "Differential temperatures (Delta T) subtracted weather fluctuations and exposed true mechanical friction."),
        ("3. Sub-Second Speed", "XGBoost trains in 0.67 seconds on 100k rows (109 MB RAM), reaching 0.83 AUC on completely unseen turbines."),
        ("4. 8 to 34 Days Lead Time", "Achieved multi-week early warning across gearboxes, generator bearings, transformers, and hydraulics."),
        ("5. Explainable & Actionable", "SHAP and LIME prove alerts match physical components; Shiny dashboard empowers operators with ROI calculators.")
    ]
    
    for i, (ptitle, pdesc) in enumerate(points):
        top_pos = Inches(2.05) + i * Inches(1.02)
        add_card(s13, Inches(0.8), top_pos, Inches(11.7), card_take_h, border_color=C_PRIMARY)
        tb = s13.shapes.add_textbox(Inches(1.1), top_pos + Inches(0.12), Inches(11.1), card_take_h - Inches(0.24))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = ptitle + "  —  "
        p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = C_NAVY
        # append description in same paragraph
        run = p.add_run()
        run.text = pdesc
        run.font.size = Pt(16); run.font.bold = False; run.font.color.rgb = C_TEXT_MAIN

    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    out_file = "presentation_wind_turbine_ids.pptx" if len(sys.argv) < 2 else sys.argv[1]
    build_presentation(out_file)
