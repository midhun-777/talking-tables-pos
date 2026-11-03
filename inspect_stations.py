with open('menu_and_seating_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

st_idx = text.find('SEATING_STATIONS = [')
print(text[st_idx:st_idx + 2500])

