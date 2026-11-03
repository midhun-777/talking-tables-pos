const fs = require('fs');

const html = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/test_modal.html', 'utf8');

// Let's search for what happens in populateReceiptModal
const p = html.indexOf('function populateReceiptModal');
console.log(html.substring(p, p + 800));

