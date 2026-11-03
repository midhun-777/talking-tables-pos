const fs = require('fs');

let template = fs.readFileSync('template.html', 'utf8');

// Safeguard old generateReportPreview
template = template.replace(
  "document.getElementById('rptGrossSales').innerText = '₹' + grossSales.toLocaleString('en-IN');",
  "if (document.getElementById('rptGrossSales')) document.getElementById('rptGrossSales').innerText = '₹' + grossSales.toLocaleString('en-IN');"
);
template = template.replace(
  "document.getElementById('rptDiscounts').innerText = '₹' + discounts.toLocaleString('en-IN');",
  "if (document.getElementById('rptDiscounts')) document.getElementById('rptDiscounts').innerText = '₹' + discounts.toLocaleString('en-IN');"
);
template = template.replace(
  "document.getElementById('rptExpenses').innerText = '₹' + expenses.toLocaleString('en-IN');",
  "if (document.getElementById('rptExpenses')) document.getElementById('rptExpenses').innerText = '₹' + expenses.toLocaleString('en-IN');\n      if (document.getElementById('rptDailyExpenses')) document.getElementById('rptDailyExpenses').innerText = '₹' + expenses.toLocaleString('en-IN');"
);
template = template.replace(
  "document.getElementById('rptNetProfit').innerText = '₹' + netProfit.toLocaleString('en-IN');",
  "if (document.getElementById('rptNetProfit')) document.getElementById('rptNetProfit').innerText = '₹' + netProfit.toLocaleString('en-IN');"
);
template = template.replace(
  "const expBody = document.getElementById('rptExpenseListBody');\n      if (dayExpenses.length === 0) {",
  "const expBody = document.getElementById('rptExpenseListBody');\n      if (expBody && dayExpenses.length === 0) {"
);

fs.writeFileSync('template.html', template, 'utf8');
console.log('generateReportPreview safeguarded');

