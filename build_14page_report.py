import os
import subprocess
import pypdf

# Build and compile the 14-page Windmill submission report
html_path = os.path.abspath("IDS_HardCopy_Submission_report_Windmill.html")
pdf_path = os.path.abspath("IDS_HardCopy_Submission_report_Windmill.pdf")

if not os.path.exists(html_path):
    raise FileNotFoundError(f"Missing {html_path}")

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

if total_pages != 14:
    raise ValueError(f"ERROR: Expected 14 pages, but got {total_pages} pages!")

print("\n--- Page Breakdown ---")
for idx, page in enumerate(reader.pages):
    txt = page.extract_text().strip()
    first_line = txt.split("\n")[0] if txt else "(empty)"
    last_line = txt.split("\n")[-1] if txt else "(empty)"
    print(f"Page {idx+1:2d} (footer '{last_line[-4:].strip()}'): '{first_line[:45]}'")

print("\nReport verified successfully!")
