with open('template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'DEFAULT_SETTINGS' in l:
        print(''.join(lines[i-2:i+22]))
        break

