import pypdfium2 as pdfium
import os

pdf_path = r"C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\Talking_Tables_Complete_Project_Documents_Bundle_Koraxa.pdf"
out_dir = r"C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\pdf_preview_pages"
os.makedirs(out_dir, exist_ok=True)

pdf = pdfium.PdfDocument(pdf_path)
for i, page in enumerate(pdf):
    image = page.render(scale=2).to_pil()
    image.save(os.path.join(out_dir, f"page_{i+1}.png"))

print(f"Rendered {len(pdf)} pages to {out_dir}")

