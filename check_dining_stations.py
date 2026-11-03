with open('menu_and_seating_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see the dining stations in SEATING_STATIONS
import re
stations = re.findall(r'\{\s*"id":\s*"([^"]+)",\s*"name":\s*"([^"]+)"[\s\S]*?"status":\s*"([^"]+)"[\s\S]*?\}', text)
for s in stations:
    if s[2] == 'dining':
        print(s)

