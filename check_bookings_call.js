const fs = require('fs');

const html = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/index.html', 'utf8');

// Find renderBookingsTable in index.html
const p = html.indexOf('function renderBookingsTable');
console.log('renderBookingsTable defined:', p !== -1);

// Find calls to renderBookingsTable
let count = 0;
let pos = 0;
while ((pos = html.indexOf('renderBookingsTable()', pos + 1)) !== -1) {
  count++;
  console.log('Call at:', pos);
}
console.log('Total calls:', count);

