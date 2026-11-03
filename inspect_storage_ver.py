with open('template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'POS_STORAGE_VERSION' in l:
        print(''.join(lines[i-5:i+30]))
        break

