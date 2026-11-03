from PIL import Image

img = Image.open(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\template_extracted\template_p1_hi.png')
w, h = img.size

# The logo is roughly between 15% and 26% of height
logo_crop = img.crop((int(w * 0.35), int(h * 0.165), int(w * 0.65), int(h * 0.265)))
logo_crop.save(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\template_extracted\exact_cover_koraxa_logo.png')
print("exact_cover_koraxa_logo.png saved:", logo_crop.size)

