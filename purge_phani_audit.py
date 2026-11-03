with open(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\generate_deep_audit_pdf.py', encoding='utf-8') as f:
    text = f.read()

# Completely purge any mention of Phani
text = text.replace("&amp; Phani V. (Talking Tables)", "")
text = text.replace("Phani V.", "Talking Tables Management")
text = text.replace("Phani", "")

with open(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\generate_deep_audit_pdf.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("generate_deep_audit_pdf.py purged of Phani")

