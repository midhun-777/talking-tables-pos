const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/index.html', 'utf8');

// Extract script
const scriptContent = html.substring(html.indexOf('<script>') + 8, html.lastIndexOf('</script>'));

// Create mock DOM environment
const context = {
  console: console,
  document: {
    getElementById: (id) => ({
      value: id === 'settingPaperWidth' ? '80mm' : '14',
      innerText: '',
      innerHTML: '',
      style: {},
      classList: { add: () => {}, remove: () => {} }
    }),
    createElement: (tag) => ({
      querySelector: () => null,
      appendChild: () => {}
    })
  },
  window: {},
  localStorage: {
    getItem: () => null,
    setItem: () => {}
  },
  setTimeout: () => {},
  setInterval: () => {},
  addEventListener: () => {}
};

vm.createContext(context);
try {
  vm.runInContext(scriptContent, context);
  console.log('Script ran successfully');
  const sampleBill = {
    id: "#TT-1002",
    date: "2026-11-02",
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
  const res = context.generateThermalReceiptHtml(sampleBill);
  console.log('generateThermalReceiptHtml output length:', res.length);
  console.log('Contains SCAN TO PAY:', res.includes('SCAN TO PAY VIA UPI'));
  console.log('Contains TALKING TABLES:', res.includes('TALKING TABLES'));
  console.log('Contains Net Payable:', res.includes('NET PAYABLE:'));
} catch (e) {
  console.error('VM Error:', e);
}

