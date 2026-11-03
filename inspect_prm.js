const fs = require('fs');
const html = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/test_modal.html', 'utf8');

const m = html.match(/<div id="printableReceipt"[^>]*>/);
console.log('Match:', m ? m[0] : 'not found');

// Let's check what populateReceiptModal does:
const p = html.indexOf('function populateReceiptModal');
console.log(html.substring(p, p + 400));

