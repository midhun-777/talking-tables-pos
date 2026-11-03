with open('template.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function seatStationAndBill' in l:
        print(''.join(lines[i-10:i+35]))
        break

