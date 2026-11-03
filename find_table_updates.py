with open('template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'appData.tables' in l or 'status =' in l or 'status:' in l:
        print(f"{i+1}: {l.strip()[:100]}")

