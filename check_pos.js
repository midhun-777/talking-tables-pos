const fs = require('fs');
const html = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/test_modal.html', 'utf8');

const p = html.indexOf('populateReceiptModal(sampleBill)');
console.log('Position:', p);
console.log('Context:\n', html.substring(p - 150, p + 250));

