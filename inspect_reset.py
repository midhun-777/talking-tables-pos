with open('template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== SETTINGS RESET BUTTON (LINES 1360-1400) ===')
print(''.join(lines[1360:1400]))

print('=== FACTORY RESET JS FUNCTION (LINES 4210-4245) ===')
print(''.join(lines[4210:4245]))

