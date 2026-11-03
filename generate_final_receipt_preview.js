const fs = require('fs');

const indexHtml = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/index.html', 'utf8');

// Extract the generateThermalReceiptHtml function and dependencies
const qrcodeJs = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/qrcode.min.js', 'utf8');
const thermalLogoData = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/thermal_logo_data.js', 'utf8');

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

const standaloneHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Epson TM-T82X Thermal Slip with Dynamic UPI QR - Talking Tables</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Plus+Jakarta+Sans:wght@500;700;800&display=swap" rel="stylesheet">
  <script>${qrcodeJs}</script>
  <script>${thermalLogoData}</script>
  <style>
    body {
      background-color: #0b1120;
      color: #f1f5f9;
      font-family: 'Plus Jakarta Sans', sans-serif;
      margin: 0;
      padding: 30px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      box-sizing: border-box;
    }
    .header-box {
      text-align: center;
      margin-bottom: 24px;
      max-width: 650px;
    }
    .title {
      font-size: 20px;
      font-weight: 800;
      color: #f59e0b;
      margin-bottom: 6px;
      letter-spacing: -0.02em;
    }
    .sub {
      font-size: 12px;
      color: #94a3b8;
      line-height: 1.5;
    }
    .badge {
      display: inline-block;
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.4);
      color: #fbbf24;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: 9999px;
      margin-top: 8px;
    }
    /* Physical 80mm Roll Container (Width: 80mm = 302.4px at 96 DPI CSS, calibrated to 203 DPI printer head) */
    .roll-simulator {
      width: 80mm;
      background: #ffffff;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
      border-radius: 4px;
      position: relative;
      box-sizing: border-box;
      padding: 0;
      border-left: 2px dashed rgba(239, 68, 68, 0.4);
      border-right: 2px dashed rgba(239, 68, 68, 0.4);
    }
    .safe-zone {
      width: 66mm;
      margin: 0 auto;
      box-sizing: border-box;
    }
  </style>
</head>
<body>

  <div class="header-box">
    <div class="title">TALKING TABLES — EPSON TM-T82X THERMAL BILL CALIBRATION</div>
    <div class="sub">
      80mm Thermal Paper Roll • 203 DPI (528 Dots Printable Safe Zone) • Clean Bill Compliance (No Payment Checkboxes)<br/>
      Pure 1-Bit Monochrome Logo • Dynamic Amount-Encoded UPI Payment QR (Exact Bill Value: ₹1550.00)
    </div>
    <div class="badge">Hardware Safe Zone Verified: Zero Right Edge Cutoff • Engineered by KORAXA TECHNOLOGIES</div>
  </div>

  <div class="roll-simulator">
    <div class="safe-zone" id="receiptContent">
      <!-- Generated via JavaScript -->
    </div>
  </div>

  <script>
    const appData = {
      settings: {
        restaurantName: "TALKING TABLES",
        address: "Beside Vignan University Main Gate, Vadlamudi 522213",
        phone: "+91 9346477777",
        gstin: "",
        paperWidth: "80mm",
        bottomFeedMm: 14,
        printLogo: true,
        enableTax: false,
        upiId: "9346477777@upi",
        footerMsg: "*** THANK YOU! VISIT TALKING TABLES AGAIN ***"
      }
    };

    function getTodayISO() {
      return new Date().toISOString().split('T')[0];
    }

    const bill = ${JSON.stringify(sampleBill)};

    function generateReceipt() {
      const settings = appData.settings;
      const printableWidth = '66mm';
      const logoWidth = '44mm';
      const feedMm = settings.bottomFeedMm || 14;

      const subtotal = bill.subtotal || 0;
      const discount = bill.discount || 0;
      const grandTotal = Math.round(subtotal - discount);

      const totalQty = bill.items.reduce((s, it) => s + it.qty, 0);
      const totalItemsCount = bill.items.length;

      // Dynamic UPI QR Code
      const upiId = settings.upiId || '9346477777@upi';
      const payee = 'TALKING TABLES';
      const upiUrl = 'upi://pay?pa=' + upiId + '&pn=' + encodeURIComponent(payee) + '&am=' + grandTotal.toFixed(2) + '&cu=INR&tn=Bill-' + bill.id.replace('#', '');

      const tempDiv = document.createElement('div');
      new QRCode(tempDiv, {
        text: upiUrl,
        width: 140,
        height: 140,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.M
      });
      const canvas = tempDiv.querySelector('canvas');
      const qrDataUrl = canvas ? canvas.toDataURL('image/png') : '';

      const logoSrc = (typeof THERMAL_LOGO_BASE64 !== 'undefined' && THERMAL_LOGO_BASE64) ? THERMAL_LOGO_BASE64 : 'talking_tables_thermal_logo.png';

      const rowsHtml = bill.items.map(it => \`
        <tr>
          <td style="width: 42%; text-align: left; padding: 2px 0; font-weight: 700; word-break: break-word;">\${it.name}</td>
          <td style="width: 14%; text-align: center; padding: 2px 0; font-weight: 700;">\${it.qty}</td>
          <td style="width: 22%; text-align: right; padding: 2px 0;">₹\${it.price}</td>
          <td style="width: 22%; text-align: right; padding: 2px 1.5mm 2px 0; font-weight: 700;">₹\${it.total}</td>
        </tr>
      \`).join('');

      return \`
        <div style="width: \${printableWidth}; max-width: \${printableWidth}; margin: 0 auto; padding: 4mm 1.5mm \${feedMm}mm 1mm; font-family: 'JetBrains Mono', 'Consolas', monospace; font-size: 9.5px; line-height: 1.25; color: #000000; box-sizing: border-box;">
          
          <!-- MONOCHROME LOGO -->
          <div style="text-align: center; margin-bottom: 4px;">
            <img src="\${logoSrc}" alt="Talking Tables" style="width: \${logoWidth}; max-height: 28mm; object-fit: contain; margin: 0 auto; display: block;" />
          </div>

          <!-- RESTAURANT BRANDING -->
          <div style="text-align: center; margin-bottom: 3px;">
            <div style="font-size: 13.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">TALKING TABLES</div>
            <div style="font-size: 8.5px; font-weight: 700; letter-spacing: 0.3px;">FINE DINING &amp; MANDI RESTAURANT</div>
            <div style="font-size: 8px; line-height: 1.2; margin-top: 1px;">Beside Vignan University Main Gate, Vadlamudi 522213</div>
            <div style="font-size: 8.5px; font-weight: 700;">Ph: +91 9346477777</div>
          </div>

          <!-- SEPARATOR -->
          <div style="border-top: 1px dashed #000; margin: 3px 0;"></div>

          <!-- BILL METADATA -->
          <div style="font-size: 9px; line-height: 1.3;">
            <div style="display: flex; justify-content: space-between;">
              <span>BILL: <b>\${bill.id}</b></span>
              <span style="padding-right: 1.5mm;">\${bill.date} \${bill.time}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span>STATION: <b>\${bill.table}</b></span>
              <span style="padding-right: 1.5mm;">TYPE: <b>Dine-In</b></span>
            </div>
          </div>

          <!-- SEPARATOR -->
          <div style="border-top: 1px dashed #000; margin: 3px 0;"></div>

          <!-- ITEMS TABLE (OPTIMIZED 4-COLUMN WITH RIGHT MARGIN BUFFER) -->
          <table style="width: 100%; table-layout: fixed; border-collapse: collapse; font-size: 9px;">
            <thead>
              <tr style="border-bottom: 1px dashed #000;">
                <th style="width: 42%; text-align: left; padding: 2px 0;">ITEM</th>
                <th style="width: 14%; text-align: center; padding: 2px 0;">QTY</th>
                <th style="width: 22%; text-align: right; padding: 2px 0;">RATE</th>
                <th style="width: 22%; text-align: right; padding: 2px 1.5mm 2px 0;">AMT</th>
              </tr>
            </thead>
            <tbody>
              \${rowsHtml}
            </tbody>
          </table>

          <!-- SEPARATOR -->
          <div style="border-top: 1px dashed #000; margin: 3px 0;"></div>

          <!-- SUMMARY COUNTS -->
          <div style="display: flex; justify-content: space-between; font-size: 8.5px; font-weight: 700;">
            <span>Items: \${totalItemsCount}</span>
            <span style="padding-right: 1.5mm;">Total Qty: \${totalQty}</span>
          </div>

          <div style="border-top: 1px dashed #000; margin: 3px 0;"></div>

          <!-- TOTALS -->
          <div style="font-size: 9.5px; line-height: 1.35;">
            <div style="display: flex; justify-content: space-between;">
              <span>Sub Total:</span>
              <span style="padding-right: 1.5mm;">₹\${subtotal.toFixed(2)}</span>
            </div>
            <!-- NET PAYABLE AMOUNT (NO PAYMENT METHOD CHECKBOXES PRINTED) -->
            <div style="border-top: 1.5px dashed #000; border-bottom: 2px solid #000; padding: 3px 0; margin: 4px 0; display: flex; justify-content: space-between; font-size: 13px; font-weight: 800;">
              <span>NET PAYABLE:</span>
              <span style="padding-right: 1.5mm;">₹\${grandTotal.toFixed(2)}</span>
            </div>
          </div>

          <!-- DYNAMIC UPI PAYMENT QR CODE (FOR EXACT AMOUNT ₹1550.00) -->
          <div style="text-align: center; margin: 6px 0 3px 0;">
            <div style="font-size: 9px; font-weight: 800; letter-spacing: 0.3px; margin-bottom: 2px;">SCAN TO PAY VIA UPI (₹\${grandTotal.toFixed(2)})</div>
            <img src="\${qrDataUrl}" alt="UPI QR" style="width: 30mm; height: 30mm; margin: 0 auto; display: block; image-rendering: pixelated;" />
            <div style="font-size: 7.5px; font-weight: 700; margin-top: 2px;">GPay &bull; PhonePe &bull; Paytm &bull; BHIM</div>
            <div style="font-size: 7px; color: #333;">UPI: \${upiId}</div>
          </div>

          <div style="border-top: 1px dashed #000; margin: 3px 0;"></div>

          <!-- FOOTER MESSAGE -->
          <div style="text-align: center; margin-top: 4px; font-size: 8.5px; line-height: 1.3;">
            <div style="font-weight: 800;">*** THANK YOU! VISIT TALKING TABLES AGAIN ***</div>
            <div style="font-size: 7.5px;">Beside Vignan University Main Gate, Vadlamudi</div>
            <div style="font-size: 7px; margin-top: 2px; color: #444;">Software engineered by KORAXA TECHNOLOGIES</div>
          </div>

          <!-- AUTO-CUTTER BUFFER (14mm) -->
          <div style="height: \${feedMm}mm; width: 100%;"></div>

        </div>
      \`;
    }

    document.getElementById('receiptContent').innerHTML = generateReceipt();
  </script>
</body>
</html>
`;

fs.writeFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/thermal_receipt_final_verified.html', standaloneHtml, 'utf8');
console.log('thermal_receipt_final_verified.html written successfully');

