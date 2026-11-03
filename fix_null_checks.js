const fs = require('fs');

let template = fs.readFileSync('template.html', 'utf8');

// Safeguard renderBookingsTable
template = template.replace(
  'function renderBookingsTable() {',
  'function renderBookingsTable() {\n      const tbody = document.getElementById(\'bookingsTableBody\');\n      if (!tbody) return;'
);

// Also remove renderBookingsTable() call from DOMContentLoaded if present
template = template.replace('renderBookingsTable();', '// Bookings removed');

fs.writeFileSync('template.html', template, 'utf8');
console.log('template.html safeguarded');

