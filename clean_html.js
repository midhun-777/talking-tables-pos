const fs = require('fs');

let t = fs.readFileSync('template.html', 'utf8');
t = t.replace(/Phani Kumar/g, 'Karthik Varma');
t = t.replace(/Phani/g, 'Karthik');
fs.writeFileSync('template.html', t, 'utf8');

console.log('template.html cleaned of Phani');

