import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

tabs = ['tables', 'dashboard', 'menu', 'reports', 'expenses', 'settings']
for t in tabs:
    custom_html = html.replace("window.addEventListener('DOMContentLoaded', () => {", f"window.addEventListener('DOMContentLoaded', () => {{\n      setTimeout(() => switchTab('{t}'), 50);")
    fn = f"test_tab_{t}.html"
    with open(fn, 'w', encoding='utf-8') as out:
        out.write(custom_html)
    print(f"Created {fn}")
