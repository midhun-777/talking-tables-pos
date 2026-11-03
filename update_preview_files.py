with open('generate_final_receipt_preview.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if 'GUEST:' in lines[i]:
        lines[i] = '              <span style="padding-right: 1.5mm;">TYPE: <b>Dine-In</b></span>\n'

with open('generate_final_receipt_preview.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Updated generate_final_receipt_preview.js cleanly!')
