const fs = require('fs');

const html = fs.readFileSync('template.html', 'utf8');

const regex = /document\.getElementById\(['"]([a-zA-Z0-9_-]+)['"]\)\.([a-zA-Z0-9_]+)/g;
let match;
const suspicious = [];
while ((match = regex.exec(html)) !== null) {
  const [full, id, prop] = match;
  // Check if id exists in html
  if (!html.includes(`id="${id}"`) && !html.includes(`id='${id}'`)) {
    suspicious.push({ id, prop, full });
  }
}

console.log('Suspicious unguarded accesses:', suspicious);

