const fs = require('fs');
const html = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/test_modal.html', 'utf8');

const p = html.indexOf('id="printableReceipt"');
console.log(html.substring(p - 300, p + 500));

