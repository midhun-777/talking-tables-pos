import re

with open(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\index.html', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'<div id="receiptModal"[^>]*>', text)
if match:
    print("Found tag:", match.group(0))

# Also check test_modal.html
with open(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\test_modal.html', encoding='utf-8') as f:
    test_text = f.read()

match2 = re.search(r'populateReceiptModal\(sampleBill\)', test_text)
print("Found trigger in test_modal:", bool(match2))

