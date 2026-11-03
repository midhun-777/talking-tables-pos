import pypdfium2 as pdfium
from PIL import Image

pdf = pdfium.PdfDocument(r'C:\Users\HP\.gemini\antigravity\brain\59c5f5b3-9843-4a89-97f6-2493997eb1db\.user_uploaded\media_1793627146257_13dc13a7.pdf')
p1 = pdf[0]
img = p1.render(scale=4).to_pil()
img.save(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\template_extracted\template_p1_hi.png')
print("High-res page 1 saved:", img.size)

