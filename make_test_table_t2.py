with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Automatically trigger clicking Hall Table T-2 (H-T2)
custom_html = html.replace(
    "window.addEventListener('DOMContentLoaded', () => {",
    "window.addEventListener('DOMContentLoaded', () => {\n      setTimeout(() => {\n        seatStationAndBill('H-T2');\n      }, 100);"
)

with open('test_table_t2.html', 'w', encoding='utf-8') as f:
    f.write(custom_html)

print('Created test_table_t2.html')

