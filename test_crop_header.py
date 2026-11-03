import pypdfium2 as pdfium
from PIL import Image

pdf = pdfium.PdfDocument(r'C:\Users\HP\.gemini\antigravity\brain\59c5f5b3-9843-4a89-97f6-2493997eb1db\.user_uploaded\media_1793627146257_13dc13a7.pdf')
p2 = pdf[1] # Page 2

# Render at 4x resolution
img = p2.render(scale=4).to_pil()
w, h = img.size
print("Rendered size:", w, h)

# A4 is 595.28 x 841.89 pt
# The top header is from top of page down to the cyan bar
# In points: height is from 841.89 down to ~735 pt, which is ~107 pt.
# 107 / 841.89 * h:
header_px_h = int((107 / 841.89) * h)
header_crop = img.crop((0, 0, w, header_px_h))
header_crop.save(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\template_extracted\exact_template_header_a4.png')

print("exact_template_header_a4.png saved:", header_crop.size)

