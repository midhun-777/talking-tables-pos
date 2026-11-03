import json

with open('menu_and_seating_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Parse SEATING_STATIONS
start_idx = text.find('SEATING_STATIONS = [')
prefix = text[:start_idx + len('SEATING_STATIONS = ')]
end_idx = text.rfind('];')
stations_json_str = text[start_idx + len('SEATING_STATIONS = '):end_idx + 1]
suffix = text[end_idx + 1:]

stations = json.loads(stations_json_str)

items_map = {
    "H-T2": [
        { "id": "TT-001", "name": "Chilli Paneer", "price": 230, "qty": 1, "total": 230 },
        { "id": "TT-036", "name": "Butter Naan", "price": 40, "qty": 4, "total": 160 },
        { "id": "TT-041", "name": "Paneer Butter Masala", "price": 250, "qty": 1, "total": 250 },
        { "id": "TT-065", "name": "Veg Dum Biryani", "price": 320, "qty": 1, "total": 320 }
    ],
    "H-M1": [
        { "id": "TT-127", "name": "Chicken Dum Mandi (Full - 5 Pcs)", "price": 650, "qty": 2, "total": 1300 },
        { "id": "TT-018", "name": "Chicken 65", "price": 250, "qty": 1, "total": 250 },
        { "id": "TT-011", "name": "Tandoori Chicken (1/2)", "price": 250, "qty": 1, "total": 250 },
        { "id": "TT-036", "name": "Butter Naan", "price": 40, "qty": 1, "total": 40 },
        { "id": "TT-034", "name": "Tandoori Roti", "price": 10, "qty": 1, "total": 10 }
    ],
    "H-M5": [
        { "id": "TT-129", "name": "Chicken Special Mandi All Mixed (Full - 6 Pcs)", "price": 800, "qty": 2, "total": 1600 },
        { "id": "TT-020", "name": "Chicken Manchuria", "price": 250, "qty": 1, "total": 250 },
        { "id": "TT-022", "name": "Lollipop Starter (5 pcs)", "price": 250, "qty": 1, "total": 250 },
        { "id": "TT-080", "name": "Chicken Fried Rice", "price": 200, "qty": 1, "total": 200 },
        { "id": "TT-036", "name": "Butter Naan", "price": 40, "qty": 3, "total": 120 },
        { "id": "TT-034", "name": "Tandoori Roti", "price": 30, "qty": 1, "total": 30 }
    ],
    "C1-M2": [
        { "id": "TT-128", "name": "Chicken Special Mandi All Mixed (Half - 3 Pcs)", "price": 450, "qty": 1, "total": 450 },
        { "id": "TT-131", "name": "Mutton Juicy Mandi (Full - 5 Pcs)", "price": 850, "qty": 1, "total": 850 },
        { "id": "TT-011", "name": "Tandoori Chicken (1/2)", "price": 250, "qty": 1, "total": 250 },
        { "id": "TT-080", "name": "Chicken Fried Rice", "price": 200, "qty": 1, "total": 200 }
    ],
    "C2-M2": [
        { "id": "TT-131", "name": "Mutton Juicy Mandi (Full - 5 Pcs)", "price": 850, "qty": 2, "total": 1700 },
        { "id": "TT-080", "name": "Chicken Fried Rice", "price": 200, "qty": 2, "total": 400 }
    ]
}

for s in stations:
    if s["id"] in items_map:
        s["items"] = items_map[s["id"]]
    else:
        s["items"] = []

new_text = prefix + json.dumps(stations, indent=2) + suffix
with open('menu_and_seating_data.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Updated menu_and_seating_data.js with station items!')

