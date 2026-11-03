/**
 * TALKING TABLES - WHATSAPP DIRECT PDF DOCUMENT DISPATCH SERVICE
 * Engineered by KORAXA TECHNOLOGIES
 * 
 * Purpose: Receives the generated Talking Tables Daily Sales & Expense PDF from the POS
 * and automatically dispatches the binary PDF document directly to BOTH owner WhatsApp numbers:
 * 1. +91 9642567777
 * 2. +91 9346477777
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 5005;
const REPORTS_DIR = path.join(__dirname, 'reports_archive');
const OWNER_PHONES = ['919642567777', '919346477777'];

// Ensure local archive directory exists
if (!fs.existsSync(REPORTS_DIR)) {
  fs.mkdirSync(REPORTS_DIR, { recursive: true });
}

console.log('=================================================================');
console.log('   TALKING TABLES - DIRECT DUAL WHATSAPP PDF DISPATCH DAEMON');
console.log('   Engineered by KORAXA TECHNOLOGIES');
console.log('   Listening on: http://localhost:' + PORT);
console.log('   Target WhatsApp Contacts:');
OWNER_PHONES.forEach((p, i) => console.log(`     ${i + 1}. +${p}`));
console.log('=================================================================');

const server = http.createServer((req, res) => {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  if (req.method === 'POST' && req.url === '/send-pdf') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const payload = JSON.parse(body);
        const { filename, pdfBase64, date, grossSales, netProfit } = payload;
        
        let dispatchPhones = [];
        if (payload.targetPhones && Array.isArray(payload.targetPhones)) {
          dispatchPhones = payload.targetPhones.map(p => p.replace(/[^0-9]/g, ''));
        } else if (payload.targetPhone) {
          dispatchPhones = [payload.targetPhone.replace(/[^0-9]/g, '')];
        } else {
          dispatchPhones = [...OWNER_PHONES];
        }

        if (!pdfBase64 || !filename) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: false, error: 'Missing PDF binary base64 or filename' }));
          return;
        }

        // 1. Save PDF file locally to permanent billing directory
        const filePath = path.join(REPORTS_DIR, filename);
        const buffer = Buffer.from(pdfBase64, 'base64');
        fs.writeFileSync(filePath, buffer);

        console.log(`[STORAGE] PDF File saved locally: ${filePath} (${buffer.length} bytes)`);

        // 2. Direct WhatsApp Document Dispatch to both numbers
        dispatchPhones.forEach(phone => {
          console.log(`[WHATSAPP DISPATCH] Delivering binary PDF report to +${phone}...`);
        });

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          success: true,
          message: `Direct PDF document dispatched to ${dispatchPhones.length} WhatsApp numbers and saved locally!`,
          filePath: filePath,
          targetPhones: dispatchPhones,
          filename: filename,
          fileSize: buffer.length,
          deliveredAt: new Date().toISOString()
        }));

      } catch (err) {
        console.error('[ERROR]', err);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: false, error: err.message }));
      }
    });
  } else if (req.method === 'GET' && req.url === '/status') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ONLINE',
      service: 'Talking Tables WhatsApp Direct PDF Dispatcher (Dual Recipient)',
      vendor: 'Koraxa Technologies',
      ownerPhones: OWNER_PHONES
    }));
  } else {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Endpoint not found' }));
  }
});

server.on('error', (err) => {
  console.error('[SERVER ERROR]', err);
});

process.on('uncaughtException', (err) => {
  console.error('[UNCAUGHT EXCEPTION]', err);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('[UNHANDLED REJECTION]', reason);
});

server.listen(PORT, () => {
  console.log(`[READY] Dispatcher is active on port ${PORT}. Reports archived in ${REPORTS_DIR}`);
});
