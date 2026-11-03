with open('menu_and_seating_data.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'SEED_TABLES' in l:
        print(''.join(lines[i:i+60]))
        break

