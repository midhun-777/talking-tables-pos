with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

custom_html = html.replace(
    "window.addEventListener('DOMContentLoaded', () => {",
    "window.addEventListener('DOMContentLoaded', () => {\n      setTimeout(() => {\n        seatStationAndBill('H-M1');\n      }, 100);"
)

with open('test_table_m1.html', 'w', encoding='utf-8') as f:
    f.write(custom_html)

print('Created test_table_m1.html')

