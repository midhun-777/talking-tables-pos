with open('template.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('whatsappPhone: "+919346477777",', 'whatsappPhone: "+919642567777",\n      whatsappPhone2: "+919346477777",')

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated DEFAULT_SETTINGS with whatsappPhone2!')

