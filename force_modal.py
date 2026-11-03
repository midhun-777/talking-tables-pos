with open(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\test_modal.html', encoding='utf-8') as f:
    html = f.read()

# Make receiptModal visible directly in markup
html = html.replace('id="receiptModal" class="fixed inset-0 bg-black/85 backdrop-blur-sm z-50 hidden flex', 'id="receiptModal" class="fixed inset-0 bg-black/85 backdrop-blur-sm z-50 flex')

with open(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\test_modal.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated test_modal.html with visible modal")

