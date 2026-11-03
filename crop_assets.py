import pypdfium2 as pdfium
from PIL import Image
import os

pdf_path = r"C:\Users\HP\.gemini\antigravity\brain\59c5f5b3-9843-4a89-97f6-2493997eb1db\.user_uploaded\media_1793627146257_13dc13a7.pdf"
out_dir = r"C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\template_extracted"

# Let's crop the Koraxa logo from template_p1.png and template_p2.png
p1_img = Image.open(os.path.join(out_dir, "template_p1.png"))
w, h = p1_img.size

# In template_p1, the Koraxa logo is at the top center
# Let's crop it precisely
logo_p1 = p1_img.crop((int(w * 0.35), int(h * 0.10), int(w * 0.65), int(h * 0.28)))
logo_p1.save(os.path.join(out_dir, "koraxa_cover_logo.png"))

# In template_p2, the Koraxa header logo is top left
p2_img = Image.open(os.path.join(out_dir, "template_p2.png"))
w2, h2 = p2_img.size
header_left = p2_img.crop((int(w2 * 0.05), int(h2 * 0.02), int(w2 * 0.55), int(h2 * 0.105)))
header_left.save(os.path.join(out_dir, "koraxa_header_logo.png"))

header_right = p2_img.crop((int(w2 * 0.68), int(h2 * 0.02), int(w2 * 0.95), int(h2 * 0.105)))
header_right.save(os.path.join(out_dir, "executive_header_box.png"))

print("Cropped header assets saved")

