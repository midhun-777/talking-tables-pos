const fs = require('fs');

const html = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/index.html', 'utf8');

const p = html.indexOf('function renderBookingsTable');
console.log(html.substring(p, p + 500));

