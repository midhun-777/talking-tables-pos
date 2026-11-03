from PIL import Image

img = Image.open(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\talking_tables_logo.jpg').convert('RGBA')
datas = img.getdata()

new_data = []
for item in datas:
    # If the pixel is white or near white, make it transparent
    if item[0] > 240 and item[1] > 240 and item[2] > 240:
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)

img.putdata(new_data)
# Crop to content bounding box
bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)

img.save(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\template_extracted\talking_tables_logo_transparent.png')
print("talking_tables_logo_transparent.png saved:", img.size)

