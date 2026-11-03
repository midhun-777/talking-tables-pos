import pypdfium2 as pdfium

pdf = pdfium.PdfDocument(r'C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\Talking_Tables_Complete_Project_Documents_Bundle_Koraxa.pdf')
print("Total pages:", len(pdf))
for i, page in enumerate(pdf):
    text = page.get_textpage().get_text_range()
    first_line = text.split('\n')[0].strip() if text else ''
    second_line = text.split('\n')[1].strip() if len(text.split('\n')) > 1 else ''
    print(f"Page {i+1}: '{first_line}' | '{second_line}'")

