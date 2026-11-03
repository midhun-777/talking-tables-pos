import re

with open(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\generate_deep_audit_pdf.py', encoding='utf-8') as f:
    text = f.read()

# Replace any old architect name with K. Midhun
text = text.replace("LEAD ARCHITECT: Phani V.", "STARTUP OWNER &amp; LEAD ARCHITECT: K. Midhun<br/><b>CLIENT EXECUTIVE:</b> Phani V.")
text = text.replace("Phani V.", "K. Midhun (Koraxa Technologies) &amp; Phani V. (Talking Tables)")

with open(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\generate_deep_audit_pdf.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("generate_deep_audit_pdf.py updated")

