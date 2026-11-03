import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function updateCartTotals' in l:
        print(''.join(lines[i:i+50]))
        break
