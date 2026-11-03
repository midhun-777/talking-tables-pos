const fs = require('fs');

let html = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/index.html', 'utf8');

const triggerCode = `
      // Auto-open modal with sample bill for visual verification
      setTimeout(() => {
        const sampleBill = {
          id: "#TT-1002",
          date: getTodayISO(),
          time: "12:35 PM",
          table: "Hall Mandi Cabin M-1",
          customer: "Walk-in Guest",
          items: [
            { id: "TT-096", name: "Chicken Dum Mandi (Full - 5 Pcs)", qty: 2, price: 650, total: 1300 },
            { id: "TT-022", name: "Chicken 65", qty: 1, price: 250, total: 250 }
          ],
          subtotal: 1550,
          discount: 0
        };
        populateReceiptModal(sampleBill);
        document.getElementById('receiptModal').classList.remove('hidden');
        document.getElementById('receiptModal').classList.add('flex');
      }, 500);
`;

html = html.replace('applySettingsToUI();', 'applySettingsToUI();\n' + triggerCode);

fs.writeFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/test_modal.html', html, 'utf8');
console.log('test_modal.html updated');
