import pypdfium2 as pdfium
import os

pdf_path = r"C:\Users\HP\.gemini\antigravity\brain\59c5f5b3-9843-4a89-97f6-2493997eb1db\.user_uploaded\media_1793627146257_13dc13a7.pdf"
out_dir = r"C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\template_extracted"
os.makedirs(out_dir, exist_ok=True)

pdf = pdfium.PdfDocument(pdf_path)
print("Template page count:", len(pdf))

# Render page 1 and page 2 at 300 DPI (scale=4.16) to see ultra crisp details
p1 = pdf[0].render(scale=3).to_pil()
p1.save(os.path.join(out_dir, "template_p1.png"))

p2 = pdf[1].render(scale=3).to_pil()
p2.save(os.path.join(out_dir, "template_p2.png"))

print("Rendered template pages 1 and 2")

