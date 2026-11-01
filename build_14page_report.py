import os
import subprocess
import pypdf

# 1. Read test_1in.html (which has the verified layout)
with open("test_1in.html", "r", encoding="utf-8") as f:
    content = f.read()

# Ensure "academic year 2026-27" is updated to "year 2026-27" to match both reference reports
content = content.replace("during the academic year 2026-27", "during the year 2026-27")

# Write to IDS_HardCopy_Submission_report_Windmill.html
html_path = os.path.abspath("IDS_HardCopy_Submission_report_Windmill.html")
pdf_path = os.path.abspath("IDS_HardCopy_Submission_report_Windmill.pdf")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated {html_path}")

# 2. Compile to PDF using Edge headless
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

# 3. Verify PDF with pypdf
reader = pypdf.PdfReader(pdf_path)
total_pages = len(reader.pages)
print(f"Total pages in compiled PDF: {total_pages}")

if total_pages != 14:
    raise ValueError(f"ERROR: Expected 14 pages, but got {total_pages} pages!")

print("\n--- Verifying Page Breakdown ---")
for idx, page in enumerate(reader.pages):
    txt = page.extract_text().strip()
    first_line = txt.split("\n")[0] if txt else "(empty)"
    last_line = txt.split("\n")[-1] if txt else "(empty)"
    print(f"Page {idx+1:2d} (footer '{last_line[-4:].strip()}'): '{first_line[:45]}'")

print("\n--- Page 1 Details ---")
p1 = reader.pages[0]
items1 = []
def v1(text, cm, tm, font_dict, font_size):
    if text.strip():
        abs_x = cm[0]*tm[4] + cm[2]*tm[5] + cm[4]
        abs_y = cm[1]*tm[4] + cm[3]*tm[5] + cm[5]
        items1.append((abs_y, abs_x, font_size, text.strip()))
p1.extract_text(visitor_text=v1)
items1.sort(key=lambda x: -x[0])
for y, x, sz, t in items1:
    print(f"y={y:5.1f}, x={x:5.1f}, sz={sz:4.1f} | {t}")

print("\n--- Page 2 Details ---")
p2 = reader.pages[1]
items2 = []
def v2(text, cm, tm, font_dict, font_size):
    if text.strip():
        abs_x = cm[0]*tm[4] + cm[2]*tm[5] + cm[4]
        abs_y = cm[1]*tm[4] + cm[3]*tm[5] + cm[5]
        items2.append((abs_y, abs_x, font_size, text.strip()))
p2.extract_text(visitor_text=v2)
items2.sort(key=lambda x: -x[0])
for y, x, sz, t in items2:
    print(f"y={y:5.1f}, x={x:5.1f}, sz={sz:4.1f} | {t}")

print("\nCompilation and verification SUCCESSFUL!")
