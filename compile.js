const fs = require('fs');

let template = fs.readFileSync('template.html', 'utf8');

const { MENU_ITEMS, SEATING_STATIONS } = require('./menu_and_seating_data.js');
let finalHtml = template.replace('/* {{SEED_MENU}} */', JSON.stringify(MENU_ITEMS, null, 2));
finalHtml = finalHtml.replace('/* {{SEED_TABLES}} */', JSON.stringify(SEATING_STATIONS, null, 2));

// Inline jsPDF for 100% offline PDF report generation
if (fs.existsSync('jspdf.umd.min.js')) {
  const jspdfJs = fs.readFileSync('jspdf.umd.min.js', 'utf8');
  finalHtml = finalHtml.replace(
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>',
    `<script>\n${jspdfJs}\n</script>`
  );
}

// Inline autoTable plugin for 100% offline table generation
if (fs.existsSync('jspdf.plugin.autotable.min.js')) {
  const autoTableJs = fs.readFileSync('jspdf.plugin.autotable.min.js', 'utf8');
  finalHtml = finalHtml.replace(
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.8.2/jspdf.plugin.autotable.min.js"></script>',
    `<script>\n${autoTableJs}\n</script>`
  );
}

// Inline color logo data for zero-dependency standalone execution
if (fs.existsSync('logo_data.js')) {
  const logoJs = fs.readFileSync('logo_data.js', 'utf8');
  finalHtml = finalHtml.replace('<script src="logo_data.js"></script>', `<script>\n${logoJs}\n</script>`);
}

// Inline thermal logo data for zero-dependency standalone execution
if (fs.existsSync('thermal_logo_data.js')) {
  const thermalLogoJs = fs.readFileSync('thermal_logo_data.js', 'utf8');
  finalHtml = finalHtml.replace('<script src="thermal_logo_data.js"></script>', `<script>\n${thermalLogoJs}\n</script>`);
}

// Inline qrcode.min.js for 100% offline QR code generation on receipts
if (fs.existsSync('qrcode.min.js')) {
  const qrcodeJs = fs.readFileSync('qrcode.min.js', 'utf8');
  finalHtml = finalHtml.replace(
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>',
    `<script>\n${qrcodeJs}\n</script>`
  );
  finalHtml = finalHtml.replace('<script src="qrcode.min.js"></script>', `<script>\n${qrcodeJs}\n</script>`);
}

fs.writeFileSync('index.html', finalHtml, 'utf8');
console.log('Compiled index.html:', fs.statSync('index.html').size, 'bytes');
