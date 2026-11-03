with open('template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function addToCart' in l:
        print(''.join(lines[i:i+80]))
        break

