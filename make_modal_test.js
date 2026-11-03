const fs = require('fs');

const script = `
  window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
      if (window.appData && window.appData.bills && window.appData.bills.length > 0) {
        window.populateReceiptModal(window.appData.bills[0]);
        document.getElementById('receiptModal').classList.remove('hidden');
      }
    }, 600);
  });
`;

let html = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/index.html', 'utf8');
const testHtml = html.replace('</body>', '<script>' + script + '</script></body>');
fs.writeFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/test_modal.html', testHtml);
console.log('test_modal.html written successfully');

