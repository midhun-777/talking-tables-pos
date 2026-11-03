with open('template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== SETTINGS CARDS (LINES 1240-1340) ===')
print(''.join(lines[1240:1340]))

