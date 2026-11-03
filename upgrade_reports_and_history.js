const fs = require('fs');

let html = fs.readFileSync('template.html', 'utf8');

// =========================================================================
// 1. UPGRADE SALES & PNL REPORT HTML VIEW
// =========================================================================
const oldReportHeader = `<section id="view-reports" class="tab-content hidden space-y-6">
      
      <div class="theme-surface p-5 rounded-2xl shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 class="text-lg font-extrabold gold-gradient-text font-brand uppercase tracking-wide">Talking Tables Sales &amp; PnL Audit Report</h2>
          <p class="text-xs text-slate-400">Download branded PDF and automatically send binary PDF document to owner's WhatsApp</p>
        </div>
        <div class="flex items-center gap-2">
          <input type="date" id="reportDate" onchange="generateReportPreview()" class="text-xs px-3 py-1.5 theme-input rounded-xl focus:outline-none">
          <button onclick="downloadReportPdf()" class="px-3.5 py-1.5 gold-gradient-btn text-slate-950 font-bold rounded-xl text-xs flex items-center gap-1.5 shadow">
            <i class="fa-solid fa-file-pdf"></i> Download PDF
          </button>
          <button onclick="sendPdfToWhatsApp()" class="px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl text-xs flex items-center gap-1.5 shadow">
            <i class="fa-brands fa-whatsapp"></i> Send to WhatsApp (+91 9346477777)
          </button>
        </div>
      </div>`;

const newReportHeader = `<section id="view-reports" class="tab-content hidden space-y-6">
      
      <div class="theme-surface p-5 rounded-2xl shadow-sm space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 class="text-lg font-extrabold gold-gradient-text font-brand uppercase tracking-wide">Talking Tables Sales &amp; PnL Audit Report</h2>
            <p class="text-xs text-slate-400">Filter across custom date ranges or throughout the entire year. Automatically downloads PDF &amp; dispatches to WhatsApp at a time.</p>
          </div>
          <!-- Download & Send Action (Simultaneous) -->
          <button onclick="downloadAndWhatsAppReport()" class="px-5 py-2.5 gold-gradient-btn text-slate-950 font-black rounded-xl text-xs flex items-center gap-2 shadow-lg shadow-amber-500/25 transform active:scale-95 transition">
            <i class="fa-solid fa-file-pdf text-sm"></i>
            <span>Download PDF &amp; Send to WhatsApp</span>
          </button>
        </div>

        <!-- Date Range Filter Bar with Quick Presets -->
        <div class="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-white/5 text-xs">
          <div class="flex flex-wrap items-center gap-1.5 bg-black/30 p-1.5 rounded-xl border border-white/5">
            <span class="text-slate-400 font-bold text-[11px] px-2">Preset:</span>
            <button onclick="setReportPreset('today')" id="rptPreset-today" class="px-2.5 py-1 rounded-lg font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">Today</button>
            <button onclick="setReportPreset('yesterday')" id="rptPreset-yesterday" class="px-2.5 py-1 rounded-lg font-medium text-slate-300 hover:text-white">Yesterday</button>
            <button onclick="setReportPreset('week')" id="rptPreset-week" class="px-2.5 py-1 rounded-lg font-medium text-slate-300 hover:text-white">This Week</button>
            <button onclick="setReportPreset('month')" id="rptPreset-month" class="px-2.5 py-1 rounded-lg font-medium text-slate-300 hover:text-white">This Month</button>
            <button onclick="setReportPreset('year')" id="rptPreset-year" class="px-2.5 py-1 rounded-lg font-medium text-slate-300 hover:text-white">Full Year (2026)</button>
          </div>

          <div class="flex items-center gap-2">
            <span class="text-slate-400 font-semibold">From:</span>
            <input type="date" id="reportFromDate" onchange="generateReportPreview()" class="text-xs px-2.5 py-1.5 theme-input rounded-xl focus:outline-none">
            <span class="text-slate-400 font-semibold">To:</span>
            <input type="date" id="reportToDate" onchange="generateReportPreview()" class="text-xs px-2.5 py-1.5 theme-input rounded-xl focus:outline-none">
          </div>
        </div>
      </div>`;

if (html.includes(oldReportHeader)) {
  html = html.replace(oldReportHeader, newReportHeader);
  console.log('1. Upgraded Sales & PnL Report UI header with Date Range presets and combined Download/WhatsApp action');
}

// Upgrade Metric Boxes in Report to include Daily, Monthly, and Yearly Expenses
const oldReportMetrics = `        <!-- 4 Summary Metric Boxes -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
          <div class="p-3 rounded-2xl bg-black/40 border border-white/5">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Gross Food Sales</span>
            <p class="text-lg font-black text-amber-300 font-mono mt-1" id="rptGrossSales">₹0</p>
          </div>
          <div class="p-3 rounded-2xl bg-black/40 border border-white/5">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Discounts Granted</span>
            <p class="text-lg font-black text-slate-300 font-mono mt-1" id="rptDiscounts">₹0</p>
          </div>
          <div class="p-3 rounded-2xl bg-black/40 border border-white/5">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Daily Expenses</span>
            <p class="text-lg font-black text-rose-400 font-mono mt-1" id="rptExpenses">₹0</p>
          </div>
          <div class="p-3 rounded-2xl bg-black/40 border border-emerald-500/30">
            <span class="text-[10px] text-emerald-400 uppercase font-bold">Net Operating Profit</span>
            <p class="text-lg font-black text-emerald-400 font-mono mt-1" id="rptNetProfit">₹0</p>
          </div>
        </div>`;

const newReportMetrics = `        <!-- 6 Summary Metric Boxes (With Daily, Monthly, Yearly Expenses Breakdown) -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 text-center">
          <div class="p-3 rounded-2xl bg-black/40 border border-white/5">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Gross Sales</span>
            <p class="text-base font-black text-amber-300 font-mono mt-1" id="rptGrossSales">₹0</p>
          </div>
          <div class="p-3 rounded-2xl bg-black/40 border border-white/5">
            <span class="text-[10px] text-slate-400 uppercase font-bold">Period Discounts</span>
            <p class="text-base font-black text-slate-300 font-mono mt-1" id="rptDiscounts">₹0</p>
          </div>
          <div class="p-3 rounded-2xl bg-black/40 border border-rose-500/30">
            <span class="text-[10px] text-rose-300 uppercase font-bold">Daily Expenses</span>
            <p class="text-base font-black text-rose-400 font-mono mt-1" id="rptDailyExpenses">₹0</p>
          </div>
          <div class="p-3 rounded-2xl bg-black/40 border border-rose-500/30">
            <span class="text-[10px] text-rose-300 uppercase font-bold">Monthly Expenses</span>
            <p class="text-base font-black text-rose-400 font-mono mt-1" id="rptMonthlyExpenses">₹0</p>
          </div>
          <div class="p-3 rounded-2xl bg-black/40 border border-rose-500/30">
            <span class="text-[10px] text-rose-300 uppercase font-bold">Yearly Expenses</span>
            <p class="text-base font-black text-rose-400 font-mono mt-1" id="rptYearlyExpenses">₹0</p>
          </div>
          <div class="p-3 rounded-2xl bg-black/40 border border-emerald-500/40 bg-emerald-950/15">
            <span class="text-[10px] text-emerald-400 uppercase font-bold">Net PnL Profit</span>
            <p class="text-base font-black text-emerald-400 font-mono mt-1" id="rptNetProfit">₹0</p>
          </div>
        </div>`;

if (html.includes(oldReportMetrics)) {
  html = html.replace(oldReportMetrics, newReportMetrics);
  console.log('2. Upgraded Sales Report Metric boxes with Daily, Monthly, and Yearly Expenses');
}

// Upgrade Bill History View with Date Range selector
const oldHistoryFilter = `<div class="flex items-center gap-2">
          <div class="relative w-64">
            <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-400"></i>
            <input type="text" id="historySearchInput" oninput="renderHistoryTable()" placeholder="Bill # or Mobile..." class="w-full pl-9 pr-3 py-1.5 text-xs theme-input rounded-xl focus:outline-none">
          </div>
          <input type="date" id="historyDateFilter" onchange="renderHistoryTable()" class="text-xs px-3 py-1.5 theme-input rounded-xl focus:outline-none">
        </div>`;

const newHistoryFilter = `<div class="flex flex-wrap items-center gap-2 text-xs">
          <div class="relative w-48">
            <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-400"></i>
            <input type="text" id="historySearchInput" oninput="renderHistoryTable()" placeholder="Bill # or Mobile..." class="w-full pl-8 pr-2.5 py-1.5 text-xs theme-input rounded-xl focus:outline-none">
          </div>
          <div class="flex items-center gap-1 bg-black/30 p-1 rounded-xl border border-white/5">
            <button onclick="setHistoryPreset('today')" id="histPreset-today" class="px-2 py-1 rounded font-bold bg-amber-500/20 text-amber-300">Today</button>
            <button onclick="setHistoryPreset('month')" id="histPreset-month" class="px-2 py-1 rounded text-slate-300 hover:text-white">Month</button>
            <button onclick="setHistoryPreset('year')" id="histPreset-year" class="px-2 py-1 rounded text-slate-300 hover:text-white">Year 2026</button>
            <button onclick="setHistoryPreset('all')" id="histPreset-all" class="px-2 py-1 rounded text-slate-300 hover:text-white">All Bills</button>
          </div>
          <input type="date" id="historyDateFrom" onchange="renderHistoryTable()" class="text-xs px-2 py-1.5 theme-input rounded-xl focus:outline-none">
          <span class="text-slate-500">to</span>
          <input type="date" id="historyDateTo" onchange="renderHistoryTable()" class="text-xs px-2 py-1.5 theme-input rounded-xl focus:outline-none">
        </div>`;

if (html.includes(oldHistoryFilter)) {
  html = html.replace(oldHistoryFilter, newHistoryFilter);
  console.log('3. Upgraded Bill History header with full-year and custom date range filters');
}

fs.writeFileSync('template.html', html, 'utf8');
console.log('Saved template.html UI structure for reports and history.');

