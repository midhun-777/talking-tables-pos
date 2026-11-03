import re

with open('template.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace the <section id="view-reports">...</section> block
view_reports_old_regex = r'<section id="view-reports" class="tab-content hidden space-y-6">[\s\S]*?</section>'

new_view_reports_html = """<section id="view-reports" class="tab-content hidden space-y-6">
      
      <!-- Top Control Bar -->
      <div class="theme-surface p-5 rounded-2xl shadow-sm space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 class="text-lg font-extrabold gold-gradient-text font-brand uppercase tracking-wide">Executive Sales &amp; Revenue Audit Report</h2>
            <p class="text-xs text-slate-400">Generate multi-period audit reports matching official PDF template. Downloads PDF locally and dispatches file directly to WhatsApp.</p>
          </div>
          <!-- Download & Send Action (Simultaneous PDF Document Dispatch) -->
          <button onclick="downloadAndWhatsAppReport()" class="px-5 py-2.5 gold-gradient-btn text-slate-950 font-black rounded-xl text-xs flex items-center gap-2 shadow-lg shadow-amber-500/25 transform active:scale-95 transition">
            <i class="fa-solid fa-file-pdf text-sm"></i>
            <span>Download PDF &amp; Send File to WhatsApp</span>
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
      </div>

      <!-- EXACT ATTACHED PDF TEMPLATE UI PREVIEW (CLEAN A4 WHITE SHEET) -->
      <div class="bg-white text-slate-900 rounded-3xl p-6 sm:p-10 shadow-2xl border border-slate-200 max-w-4xl mx-auto space-y-6 font-sans">
        
        <!-- Document Header -->
        <div class="flex flex-wrap items-start justify-between gap-4 pb-3 border-b-2 border-slate-900">
          <div class="flex items-center gap-3.5">
            <div class="w-12 h-12 rounded-xl overflow-hidden bg-white p-0.5 border border-slate-200 shrink-0">
              <img src="talking_tables_logo.jpg" alt="Logo" class="w-full h-full object-cover">
            </div>
            <div>
              <p class="text-[10px] font-black uppercase tracking-wider text-amber-600 font-mono">Fine Dining &amp; Mandi</p>
              <h1 class="text-2xl font-black text-slate-950 uppercase tracking-tight font-brand">TALKING TABLES</h1>
              <p class="text-xs text-slate-600 font-medium">Beside Vignan University Main Gate, Vadlamudi 522213.</p>
              <p class="text-[11px] text-slate-500 font-mono">Ph: +91 9346477777 &bull; FSSAI: 10126007000021</p>
            </div>
          </div>

          <div class="text-right">
            <span class="inline-block px-3 py-1 rounded-full bg-amber-100 text-amber-800 border border-amber-300 font-black text-[11px] uppercase tracking-wider shadow-sm" id="reportBadgeType">
              Custom Report
            </span>
            <h2 class="text-sm font-extrabold text-slate-950 uppercase tracking-wide mt-1.5">
              Executive Sales &amp; Revenue Audit Report
            </h2>
            <p class="text-xs text-slate-600 font-semibold mt-0.5" id="reportAuditPeriodDisplay">
              Period: 04 Oct 2026 to 02 Nov 2026
            </p>
            <p class="text-[10px] text-slate-400 font-mono mt-0.5" id="reportGeneratedTimestamp">
              Generated: 02/11/2026 20:52:16
            </p>
          </div>
        </div>

        <!-- 4 Top Metric Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 shadow-sm">
            <p class="text-[10px] font-bold uppercase text-slate-500 tracking-wider">Gross Sales</p>
            <p class="text-xl font-extrabold text-slate-900 mt-1 font-mono" id="rptGrossSales">&#8377;0.00</p>
            <p class="text-[10px] text-slate-500 mt-0.5 font-medium" id="rptNetSubtext">Net: &#8377;0.00</p>
          </div>
          <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 shadow-sm">
            <p class="text-[10px] font-bold uppercase text-slate-500 tracking-wider">Total Orders</p>
            <p class="text-xl font-extrabold text-slate-900 mt-1 font-mono" id="rptTotalOrders">0</p>
            <p class="text-[10px] text-slate-500 mt-0.5 font-medium">All settled</p>
          </div>
          <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 shadow-sm">
            <p class="text-[10px] font-bold uppercase text-slate-500 tracking-wider">Avg. Order Value</p>
            <p class="text-xl font-extrabold text-slate-900 mt-1 font-mono" id="rptAvgOrderValue">&#8377;0</p>
            <p class="text-[10px] text-slate-500 mt-0.5 font-medium">Per paying customer</p>
          </div>
          <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 shadow-sm">
            <p class="text-[10px] font-bold uppercase text-slate-500 tracking-wider">Items Fulfilled</p>
            <p class="text-xl font-extrabold text-amber-600 mt-1 font-mono" id="rptItemsFulfilled">0</p>
            <p class="text-[10px] text-slate-500 mt-0.5 font-medium">Total items sold across bills</p>
          </div>
        </div>

        <!-- Middle Section: Two Tables Side-By-Side (Expenses Left, Top Dishes Right) -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          <!-- LEFT TABLE: OPERATIONAL EXPENSES SUMMARY (Without Cash/UPI/Card payment breakdown!) -->
          <div class="rounded-xl overflow-hidden border border-slate-200 shadow-sm">
            <div class="bg-slate-900 text-white px-3.5 py-2.5 flex items-center justify-between">
              <span class="text-xs font-extrabold uppercase tracking-wider flex items-center gap-1.5">
                <i class="fa-solid fa-wallet text-amber-400"></i> Operational Expenses Summary
              </span>
              <span class="text-[10px] font-mono text-slate-400" id="rptExpenseCountBadge">5 Vouchers</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-slate-100 text-slate-700 font-bold border-b border-slate-200 text-[11px]">
                  <tr>
                    <th class="px-3 py-2">Category</th>
                    <th class="px-3 py-2">Description</th>
                    <th class="px-3 py-2 text-right">Amount</th>
                    <th class="px-3 py-2 text-right">Share</th>
                  </tr>
                </thead>
                <tbody id="rptExpenseSummaryBody" class="divide-y divide-slate-100 font-mono text-slate-800 text-[11px]">
                  <!-- Injected via JS -->
                </tbody>
                <tfoot class="bg-slate-100 text-slate-900 font-bold border-t border-slate-200 text-[11px]">
                  <tr>
                    <td colspan="2" class="px-3 py-2 text-slate-900 uppercase">Total Expenses:</td>
                    <td class="px-3 py-2 text-right font-mono text-rose-600" id="rptTotalExpenseVal">&#8377;0.00</td>
                    <td class="px-3 py-2 text-right font-mono" id="rptTotalExpensePct">100.0%</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>

          <!-- RIGHT TABLE: TOP 5 BEST-SELLING ITEMS -->
          <div class="rounded-xl overflow-hidden border border-slate-200 shadow-sm">
            <div class="bg-slate-900 text-white px-3.5 py-2.5 flex items-center justify-between">
              <span class="text-xs font-extrabold uppercase tracking-wider flex items-center gap-1.5">
                <i class="fa-solid fa-utensils text-amber-400"></i> Top 5 Best-Selling Items
              </span>
              <span class="text-[10px] font-mono text-slate-400">Ranked by Revenue</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-slate-100 text-slate-700 font-bold border-b border-slate-200 text-[11px]">
                  <tr>
                    <th class="px-3 py-2">Dish Name</th>
                    <th class="px-3 py-2">Category</th>
                    <th class="px-3 py-2 text-center">Qty</th>
                    <th class="px-3 py-2 text-right">Sales</th>
                  </tr>
                </thead>
                <tbody id="rptTop5Body" class="divide-y divide-slate-100 font-mono text-slate-800 text-[11px]">
                  <!-- Injected via JS -->
                </tbody>
              </table>
            </div>
          </div>

        </div>

        <!-- Bottom Table: SALES CONTRIBUTION BY CATEGORY -->
        <div class="rounded-xl overflow-hidden border border-slate-200 shadow-sm">
          <div class="bg-slate-900 text-white px-4 py-2.5 flex items-center justify-between">
            <span class="text-xs font-extrabold uppercase tracking-wider flex items-center gap-1.5">
              <i class="fa-solid fa-layer-group text-amber-400"></i> Sales Contribution by Category
            </span>
            <span class="text-[10px] font-mono text-slate-400">Category Share Analysis</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-100 text-slate-700 font-bold border-b border-slate-200 text-[11px]">
                <tr>
                  <th class="px-4 py-2">Category</th>
                  <th class="px-4 py-2 text-center">Items Sold</th>
                  <th class="px-4 py-2 text-right">Total Revenue</th>
                  <th class="px-4 py-2 text-right">Revenue Share</th>
                </tr>
              </thead>
              <tbody id="rptCategorySalesBody" class="divide-y divide-slate-100 font-mono text-slate-800 text-[11px]">
                <!-- Injected via JS -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- PAGE 2 SECTION: TRANSACTION LEDGER & EXECUTIVE SIGN-OFF -->
        <div class="pt-6 border-t-2 border-slate-200 space-y-6">
          
          <div class="rounded-xl overflow-hidden border border-slate-200 shadow-sm">
            <div class="bg-slate-900 text-white px-4 py-2.5 flex items-center justify-between">
              <span class="text-xs font-extrabold uppercase tracking-wider flex items-center gap-1.5">
                <i class="fa-solid fa-receipt text-amber-400"></i> <span id="rptLedgerTitle">Transaction Ledger (0 Bills)</span>
              </span>
              <span class="text-[10px] font-mono text-slate-400">Settled Invoices Ledger</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-slate-100 text-slate-700 font-bold border-b border-slate-200 text-[11px]">
                  <tr>
                    <th class="px-3 py-2 text-center">#</th>
                    <th class="px-3 py-2">Bill No</th>
                    <th class="px-3 py-2 text-center">Time</th>
                    <th class="px-3 py-2">Table / Type</th>
                    <th class="px-3 py-2 text-center">Items</th>
                    <th class="px-3 py-2 text-right">Subtotal</th>
                    <th class="px-3 py-2 text-right">Total</th>
                  </tr>
                </thead>
                <tbody id="rptLedgerBody" class="divide-y divide-slate-100 font-mono text-slate-800 text-[11px]">
                  <!-- Injected via JS -->
                </tbody>
                <tfoot class="bg-slate-100 text-slate-900 font-extrabold border-t border-slate-200 text-[11px]">
                  <tr>
                    <td colspan="5" class="px-3 py-2 text-right uppercase tracking-wider">Total Sum:</td>
                    <td class="px-3 py-2 text-right font-mono" id="rptLedgerSubtotalSum">&#8377;0.00</td>
                    <td class="px-3 py-2 text-right font-mono text-amber-600" id="rptLedgerTotalSum">&#8377;0.00</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>

          <!-- Signatures & Verification Section -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 items-end pt-4">
            <div class="text-center space-y-1">
              <div class="border-b border-dashed border-slate-400 pb-1 w-44 mx-auto"></div>
              <p class="text-xs font-bold text-slate-900 uppercase">Cashier / Shift Incharge</p>
              <p class="text-[10px] text-slate-500 italic">Prepared By</p>
            </div>

            <div class="text-center space-y-1">
              <div class="border-b border-dashed border-slate-400 pb-1 w-44 mx-auto"></div>
              <p class="text-xs font-bold text-slate-900 uppercase">Restaurant Manager</p>
              <p class="text-[10px] text-slate-500 italic">Audited &amp; Verified By</p>
            </div>

            <div class="p-3 border border-slate-300 rounded-xl bg-slate-50 text-center shadow-inner max-w-[200px] mx-auto w-full">
              <p class="text-[9px] font-black uppercase text-slate-400 tracking-widest">Official Seal</p>
              <p class="text-xs font-bold text-slate-900 mt-0.5">TALKING TABLES</p>
              <p class="text-[10px] text-slate-500">Vadlamudi Branch</p>
            </div>
          </div>

          <!-- Footer Note -->
          <div class="text-center pt-3 border-t border-slate-100 text-[10px] text-slate-400 font-mono">
            CONFIDENTIAL BUSINESS REPORT &bull; TALKING TABLES POS SYSTEM &bull; GENERATED BY KORAXA TECHNOLOGIES
          </div>

        </div>

      </div>

    </section>"""

text = re.sub(view_reports_old_regex, lambda m: new_view_reports_html, text, flags=re.DOTALL)

# 2. Replace the report logic functions
report_funcs_old_regex = r'    // 13\. SALES & PNL REPORT[\s\S]*?(?=    // 14\. SETTINGS & FACTORY RESET)'

new_report_funcs = """    // 13. SALES & REVENUE AUDIT REPORT (EXACT ATTACHED PDF TEMPLATE ENGINE)
    let currentReportPreset = 'today';

    function setReportPreset(preset) {
      currentReportPreset = preset;
      const today = getTodayISO();
      const fromEl = document.getElementById('reportFromDate');
      const toEl = document.getElementById('reportToDate');
      
      document.querySelectorAll('[id^="rptPreset-"]').forEach(btn => {
        btn.className = "px-2.5 py-1 rounded-lg font-medium text-slate-300 hover:text-white";
      });
      const activeBtn = document.getElementById('rptPreset-' + preset);
      if (activeBtn) activeBtn.className = "px-2.5 py-1 rounded-lg font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30";

      if (preset === 'today') {
        fromEl.value = today;
        toEl.value = today;
      } else if (preset === 'yesterday') {
        const d = new Date();
        d.setDate(d.getDate() - 1);
        const yDate = d.toISOString().split('T')[0];
        fromEl.value = yDate;
        toEl.value = yDate;
      } else if (preset === 'week') {
        const d = new Date();
        d.setDate(d.getDate() - 7);
        fromEl.value = d.toISOString().split('T')[0];
        toEl.value = today;
      } else if (preset === 'month') {
        const curMonthStart = today.substring(0, 7) + '-01';
        fromEl.value = curMonthStart;
        toEl.value = today;
      } else if (preset === 'year') {
        const curYearStart = today.substring(0, 4) + '-01-01';
        const curYearEnd = today.substring(0, 4) + '-12-31';
        fromEl.value = curYearStart;
        toEl.value = curYearEnd;
      }
      generateReportPreview();
    }

    function generateReportPreview() {
      const today = getTodayISO();
      const fromDate = document.getElementById('reportFromDate')?.value || today;
      const toDate = document.getElementById('reportToDate')?.value || today;
      
      const periodLabel = fromDate === toDate ? fromDate : (fromDate + ' to ' + toDate);
      const auditPeriodEl = document.getElementById('reportAuditPeriodDisplay');
      if (auditPeriodEl) auditPeriodEl.innerText = "Period: " + periodLabel;

      const now = new Date();
      const genStr = now.toLocaleDateString('en-GB') + ' ' + now.toLocaleTimeString('en-GB');
      const genEl = document.getElementById('reportGeneratedTimestamp');
      if (genEl) genEl.innerText = "Generated: " + genStr;

      // Filter bills and expenses within selected date range
      const periodBills = appData.bills.filter(b => b.date >= fromDate && b.date <= toDate);
      const periodExpenses = appData.expenses.filter(e => e.date >= fromDate && e.date <= toDate);

      // Financial totals
      const grossSales = periodBills.reduce((s, b) => s + (b.grandTotal || b.subtotal || 0), 0);
      const totalOrders = periodBills.length;
      const avgOrderValue = totalOrders > 0 ? Math.round(grossSales / totalOrders) : 0;
      const totalItemsFulfilled = periodBills.reduce((sum, b) => sum + (b.items || []).reduce((isum, it) => isum + (it.qty || 1), 0), 0);
      const totalExpenses = periodExpenses.reduce((s, e) => s + (e.amount || 0), 0);

      // 1. Update 4 Top Metric Cards
      if (document.getElementById('rptGrossSales')) {
        document.getElementById('rptGrossSales').innerText = '₹' + grossSales.toLocaleString('en-IN', {minimumFractionDigits: 2});
      }
      if (document.getElementById('rptNetSubtext')) {
        document.getElementById('rptNetSubtext').innerText = 'Net: ₹' + grossSales.toLocaleString('en-IN', {minimumFractionDigits: 2});
      }
      if (document.getElementById('rptTotalOrders')) {
        document.getElementById('rptTotalOrders').innerText = String(totalOrders);
      }
      if (document.getElementById('rptAvgOrderValue')) {
        document.getElementById('rptAvgOrderValue').innerText = '₹' + avgOrderValue.toLocaleString('en-IN');
      }
      if (document.getElementById('rptItemsFulfilled')) {
        document.getElementById('rptItemsFulfilled').innerText = String(totalItemsFulfilled);
      }

      // 2. Middle Left: Operational Expenses Summary (Without Cash/UPI/Card payment methods!)
      const expCatMap = {};
      periodExpenses.forEach(e => {
        const c = e.category || 'General';
        if (!expCatMap[c]) expCatMap[c] = { category: c, desc: e.description || c, amount: 0 };
        expCatMap[c].amount += e.amount;
      });
      const expCatList = Object.values(expCatMap).sort((a, b) => b.amount - a.amount);
      const expBody = document.getElementById('rptExpenseSummaryBody');
      if (expBody) {
        if (expCatList.length === 0) {
          expBody.innerHTML = '<tr><td colspan="4" class="px-3 py-3 text-slate-400 text-center font-sans">No expenses recorded for this period</td></tr>';
        } else {
          expBody.innerHTML = expCatList.map(e => `
            <tr class="hover:bg-slate-50 transition">
              <td class="px-3 py-2 font-bold text-slate-900">${e.category}</td>
              <td class="px-3 py-2 text-slate-600 truncate max-w-[130px]">${e.desc}</td>
              <td class="px-3 py-2 text-right font-bold text-rose-600">₹${e.amount.toLocaleString('en-IN', {minimumFractionDigits: 2})}</td>
              <td class="px-3 py-2 text-right font-medium text-slate-500">${totalExpenses > 0 ? ((e.amount / totalExpenses) * 100).toFixed(1) + '%' : '0.0%'}</td>
            </tr>
          `).join('');
        }
      }
      if (document.getElementById('rptTotalExpenseVal')) {
        document.getElementById('rptTotalExpenseVal').innerText = '₹' + totalExpenses.toLocaleString('en-IN', {minimumFractionDigits: 2});
      }
      if (document.getElementById('rptExpenseCountBadge')) {
        document.getElementById('rptExpenseCountBadge').innerText = periodExpenses.length + ' Vouchers';
      }

      // 3. Middle Right: Top 5 Best-Selling Items
      const dishMap = {};
      periodBills.forEach(b => {
        (b.items || []).forEach(it => {
          if (!dishMap[it.name]) dishMap[it.name] = { name: it.name, category: it.category || 'General', qty: 0, sales: 0 };
          dishMap[it.name].qty += (it.qty || 1);
          dishMap[it.name].sales += (it.total || ((it.price || 0) * (it.qty || 1)));
        });
      });
      const top5Dishes = Object.values(dishMap).sort((a, b) => b.sales - a.sales).slice(0, 5);
      const top5Body = document.getElementById('rptTop5Body');
      if (top5Body) {
        if (top5Dishes.length === 0) {
          top5Body.innerHTML = '<tr><td colspan="4" class="px-3 py-3 text-slate-400 text-center font-sans">No dish sales recorded for this period</td></tr>';
        } else {
          top5Body.innerHTML = top5Dishes.map(d => `
            <tr class="hover:bg-slate-50 transition">
              <td class="px-3 py-2 font-bold text-slate-900 truncate max-w-[130px]">${d.name}</td>
              <td class="px-3 py-2 text-slate-600">${d.category}</td>
              <td class="px-3 py-2 text-center font-bold text-slate-800">${d.qty}</td>
              <td class="px-3 py-2 text-right font-bold text-amber-700">₹${d.sales.toLocaleString('en-IN', {minimumFractionDigits: 2})}</td>
            </tr>
          `).join('');
        }
      }

      // 4. Bottom Table: Sales Contribution by Category
      const catMap = {};
      periodBills.forEach(b => {
        (b.items || []).forEach(it => {
          const cat = it.category || 'General';
          if (!catMap[cat]) catMap[cat] = { category: cat, itemsSold: 0, revenue: 0 };
          catMap[cat].itemsSold += (it.qty || 1);
          catMap[cat].revenue += (it.total || ((it.price || 0) * (it.qty || 1)));
        });
      });
      const catList = Object.values(catMap).sort((a, b) => b.revenue - a.revenue);
      const catBody = document.getElementById('rptCategorySalesBody');
      if (catBody) {
        if (catList.length === 0) {
          catBody.innerHTML = '<tr><td colspan="4" class="px-4 py-3 text-slate-400 text-center font-sans">No category sales recorded</td></tr>';
        } else {
          catBody.innerHTML = catList.map(c => `
            <tr class="hover:bg-slate-50 transition">
              <td class="px-4 py-2 font-bold text-slate-900">${c.category}</td>
              <td class="px-4 py-2 text-center font-bold text-slate-800">${c.itemsSold}</td>
              <td class="px-4 py-2 text-right font-bold text-slate-900">₹${c.revenue.toLocaleString('en-IN', {minimumFractionDigits: 2})}</td>
              <td class="px-4 py-2 text-right font-medium text-slate-600">${grossSales > 0 ? ((c.revenue / grossSales) * 100).toFixed(1) + '%' : '0.0%'}</td>
            </tr>
          `).join('');
        }
      }

      // 5. Page 2 Table: Transaction Ledger (Zero Payment Breakdown!)
      const ledgerBody = document.getElementById('rptLedgerBody');
      if (ledgerBody) {
        if (periodBills.length === 0) {
          ledgerBody.innerHTML = '<tr><td colspan="7" class="px-3 py-4 text-slate-400 text-center font-sans">No customer invoices found matching criteria</td></tr>';
        } else {
          ledgerBody.innerHTML = periodBills.map((b, idx) => {
            const itemCount = (b.items || []).reduce((sum, it) => sum + (it.qty || 1), 0);
            return `
              <tr class="hover:bg-slate-50 transition">
                <td class="px-3 py-2 text-center text-slate-400">${idx + 1}</td>
                <td class="px-3 py-2 font-bold text-slate-900">${b.id}</td>
                <td class="px-3 py-2 text-center text-slate-600">${b.time || '-'}</td>
                <td class="px-3 py-2 text-slate-800 font-medium">${b.table || 'Dine-In'}</td>
                <td class="px-3 py-2 text-center text-slate-700">${itemCount} items</td>
                <td class="px-3 py-2 text-right text-slate-800">₹${(b.subtotal || b.grandTotal || 0).toLocaleString('en-IN', {minimumFractionDigits: 2})}</td>
                <td class="px-3 py-2 text-right font-bold text-amber-700">₹${(b.grandTotal || b.subtotal || 0).toLocaleString('en-IN', {minimumFractionDigits: 2})}</td>
              </tr>
            `;
          }).join('');
        }
      }
      if (document.getElementById('rptLedgerTitle')) {
        document.getElementById('rptLedgerTitle').innerText = 'Transaction Ledger (' + periodBills.length + ' Bills)';
      }
      if (document.getElementById('rptLedgerSubtotalSum')) {
        document.getElementById('rptLedgerSubtotalSum').innerText = '₹' + grossSales.toLocaleString('en-IN', {minimumFractionDigits: 2});
      }
      if (document.getElementById('rptLedgerTotalSum')) {
        document.getElementById('rptLedgerTotalSum').innerText = '₹' + grossSales.toLocaleString('en-IN', {minimumFractionDigits: 2});
      }
    }

    // PDF GENERATION MATCHING EXACT USER ATTACHED TEMPLATE
    function createReportJsPdfDocument() {
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF('p', 'mm', 'a4');
      const pageWidth = 210;
      const pageHeight = 297;
      const margin = 14;
      const contentWidth = pageWidth - (margin * 2); // 182mm

      const today = getTodayISO();
      const fromDate = document.getElementById('reportFromDate')?.value || today;
      const toDate = document.getElementById('reportToDate')?.value || today;
      const periodStr = fromDate === toDate ? fromDate : (fromDate + " to " + toDate);
      
      const now = new Date();
      const genTimestamp = now.toLocaleDateString('en-GB') + ' ' + now.toLocaleTimeString('en-GB');

      // Filtered data
      const bills = appData.bills.filter(b => b.date >= fromDate && b.date <= toDate);
      const expenses = appData.expenses.filter(e => e.date >= fromDate && e.date <= toDate);

      // Financial Calculations
      const grossSales = bills.reduce((s, b) => s + (b.grandTotal || b.subtotal || 0), 0);
      const totalOrders = bills.length;
      const avgOrderValue = totalOrders > 0 ? Math.round(grossSales / totalOrders) : 0;
      const totalItemsFulfilled = bills.reduce((sum, b) => sum + (b.items || []).reduce((isum, it) => isum + (it.qty || 1), 0), 0);
      const totalExpenses = expenses.reduce((s, e) => s + (e.amount || 0), 0);

      // Top 5 Best-Selling Items
      const dishMap = {};
      bills.forEach(b => {
        (b.items || []).forEach(it => {
          if (!dishMap[it.name]) dishMap[it.name] = { name: it.name, category: it.category || 'General', qty: 0, sales: 0 };
          dishMap[it.name].qty += (it.qty || 1);
          dishMap[it.name].sales += (it.total || ((it.price || 0) * (it.qty || 1)));
        });
      });
      const top5Dishes = Object.values(dishMap).sort((a, b) => b.sales - a.sales).slice(0, 5);

      // Sales Contribution by Category
      const catMap = {};
      bills.forEach(b => {
        (b.items || []).forEach(it => {
          const cat = it.category || 'General';
          if (!catMap[cat]) catMap[cat] = { category: cat, itemsSold: 0, revenue: 0 };
          catMap[cat].itemsSold += (it.qty || 1);
          catMap[cat].revenue += (it.total || ((it.price || 0) * (it.qty || 1)));
        });
      });
      const catList = Object.values(catMap).sort((a, b) => b.revenue - a.revenue);

      // Expenses grouped by Category
      const expCatMap = {};
      expenses.forEach(e => {
        const c = e.category || 'General';
        if (!expCatMap[c]) expCatMap[c] = { category: c, desc: e.description || c, amount: 0 };
        expCatMap[c].amount += e.amount;
      });
      const expCatList = Object.values(expCatMap).sort((a, b) => b.amount - a.amount);

      // =========================================================================
      // PAGE 1: EXECUTIVE AUDIT REPORT
      // =========================================================================
      
      // 1. Header Left: Brand & Address
      let brandX = margin;
      if (typeof TALKING_TABLES_LOGO_B64 !== 'undefined' && TALKING_TABLES_LOGO_B64) {
        try {
          doc.addImage(TALKING_TABLES_LOGO_B64, 'JPEG', margin, 11, 14, 14);
          brandX = margin + 17;
        } catch(e) {}
      }

      doc.setFont("helvetica", "bold");
      doc.setFontSize(7);
      doc.setTextColor(217, 119, 6); // Amber 600
      doc.text("FINE DINING & MANDI", brandX, 14);

      doc.setFontSize(15);
      doc.setTextColor(17, 24, 39); // Gray 900
      doc.text("TALKING TABLES", brandX, 19.5);

      doc.setFont("helvetica", "normal");
      doc.setFontSize(7.5);
      doc.setTextColor(75, 85, 99); // Gray 600
      doc.text("Beside Vignan University Main Gate, Vadlamudi 522213.", brandX, 23.5);
      doc.setFontSize(7);
      doc.setTextColor(107, 114, 128); // Gray 500
      doc.text("Ph: +91 9346477777  \\u2022  FSSAI: 10126007000021", brandX, 27);

      // 1. Header Right: Custom Report Badge & Meta
      doc.setFillColor(254, 243, 199); // Amber 100
      doc.setDrawColor(252, 211, 77); // Amber 300
      doc.setLineWidth(0.3);
      doc.roundedRect(pageWidth - margin - 38, 11, 38, 5.5, 1.2, 1.2, 'FD');
      doc.setFont("helvetica", "bold");
      doc.setFontSize(7);
      doc.setTextColor(180, 83, 9); // Amber 700
      doc.text("CUSTOM REPORT", pageWidth - margin - 19, 14.8, { align: "center" });

      doc.setFont("helvetica", "bold");
      doc.setFontSize(10);
      doc.setTextColor(17, 24, 39);
      doc.text("EXECUTIVE SALES & REVENUE AUDIT REPORT", pageWidth - margin, 20.5, { align: "right" });

      doc.setFont("helvetica", "normal");
      doc.setFontSize(7.5);
      doc.setTextColor(75, 85, 99);
      doc.text("Period: " + periodStr, pageWidth - margin, 24.5, { align: "right" });

      doc.setFontSize(6.8);
      doc.setTextColor(156, 163, 175);
      doc.text("Generated: " + genTimestamp, pageWidth - margin, 28, { align: "right" });

      // Header Divider Line
      doc.setDrawColor(17, 24, 39);
      doc.setLineWidth(0.6);
      doc.line(margin, 31, pageWidth - margin, 31);

      // 2. Top 4 Metric Cards
      const cardW = (contentWidth - 9) / 4; // ~43.25mm
      const cardH = 19;
      const cardY = 35;
      const cardsData = [
        { label: "GROSS SALES", val: "INR " + grossSales.toLocaleString('en-IN', {minimumFractionDigits: 2}), sub: "Net: INR " + grossSales.toLocaleString('en-IN', {minimumFractionDigits: 2}), color: [17, 24, 39] },
        { label: "TOTAL ORDERS", val: String(totalOrders), sub: "All settled", color: [17, 24, 39] },
        { label: "AVG. ORDER VALUE", val: "INR " + avgOrderValue.toLocaleString('en-IN'), sub: "Per paying customer", color: [17, 24, 39] },
        { label: "ITEMS FULFILLED", val: String(totalItemsFulfilled), sub: "Total items sold across bills", color: [217, 119, 6] }
      ];

      cardsData.forEach((c, idx) => {
        const cx = margin + (idx * (cardW + 3));
        doc.setFillColor(249, 250, 251);
        doc.setDrawColor(229, 231, 235);
        doc.setLineWidth(0.25);
        doc.roundedRect(cx, cardY, cardW, cardH, 2, 2, 'FD');

        doc.setFont("helvetica", "bold");
        doc.setFontSize(6.5);
        doc.setTextColor(107, 114, 128);
        doc.text(c.label, cx + 3.5, cardY + 5);

        doc.setFontSize(12.5);
        doc.setTextColor(c.color[0], c.color[1], c.color[2]);
        doc.text(c.val, cx + 3.5, cardY + 12);

        doc.setFont("helvetica", "normal");
        doc.setFontSize(6.2);
        doc.setTextColor(107, 114, 128);
        doc.text(c.sub, cx + 3.5, cardY + 16);
      });

      // 3. Middle Section: Two Tables Side-By-Side (Expenses Left, Top Dishes Right)
      const halfW = (contentWidth - 4) / 2; // 89mm each
      const midY = 58;

      // Left Table: OPERATIONAL EXPENSES SUMMARY (Without Cash/UPI/Card payment methods!)
      const expRows = expCatList.map(e => [
        e.category,
        e.desc.length > 20 ? e.desc.substring(0, 18) + '...' : e.desc,
        "INR " + e.amount.toLocaleString('en-IN', {minimumFractionDigits: 2}),
        (totalExpenses > 0 ? ((e.amount / totalExpenses) * 100).toFixed(1) + '%' : '0.0%')
      ]);
      if (expRows.length === 0) {
        expRows.push(["General", "No expenses recorded", "INR 0.00", "0.0%"]);
      }

      doc.autoTable({
        startY: midY,
        margin: { left: margin },
        tableWidth: halfW,
        head: [[
          { content: "OPERATIONAL EXPENSES SUMMARY", colSpan: 4, styles: { fillColor: [17, 24, 39], textColor: [255, 255, 255], fontStyle: 'bold', halign: 'left', fontSize: 7.5 } }
        ], [
          "Category", "Description", "Amount", "Share"
        ]],
        body: expRows,
        foot: [[
          "TOTAL EXPENSES", "", "INR " + totalExpenses.toLocaleString('en-IN', {minimumFractionDigits: 2}), "100.0%"
        ]],
        headStyles: {
          fillColor: [243, 244, 246],
          textColor: [55, 65, 81],
          fontStyle: 'bold',
          fontSize: 6.8
        },
        bodyStyles: {
          fontSize: 6.5,
          textColor: [31, 41, 55],
          cellPadding: 1.8
        },
        footStyles: {
          fillColor: [243, 244, 246],
          textColor: [17, 24, 39],
          fontStyle: 'bold',
          fontSize: 6.8
        },
        columnStyles: {
          0: { cellWidth: 26 },
          1: { cellWidth: 28 },
          2: { cellWidth: 21, halign: 'right' },
          3: { cellWidth: 14, halign: 'right' }
        },
        theme: 'plain'
      });

      const expTableEnd = doc.lastAutoTable.finalY;

      // Right Table: TOP 5 BEST-SELLING ITEMS
      const dishRows = top5Dishes.map(d => [
        d.name.length > 20 ? d.name.substring(0, 18) + '...' : d.name,
        d.category,
        String(d.qty),
        "INR " + d.sales.toLocaleString('en-IN', {minimumFractionDigits: 2})
      ]);
      if (dishRows.length === 0) {
        dishRows.push(["No dish sales", "-", "0", "INR 0.00"]);
      }

      doc.autoTable({
        startY: midY,
        margin: { left: margin + halfW + 4 },
        tableWidth: halfW,
        head: [[
          { content: "TOP 5 BEST-SELLING ITEMS", colSpan: 4, styles: { fillColor: [17, 24, 39], textColor: [255, 255, 255], fontStyle: 'bold', halign: 'left', fontSize: 7.5 } }
        ], [
          "Dish Name", "Category", "Qty", "Sales"
        ]],
        body: dishRows,
        headStyles: {
          fillColor: [243, 244, 246],
          textColor: [55, 65, 81],
          fontStyle: 'bold',
          fontSize: 6.8
        },
        bodyStyles: {
          fontSize: 6.5,
          textColor: [31, 41, 55],
          cellPadding: 1.8
        },
        columnStyles: {
          0: { cellWidth: 34 },
          1: { cellWidth: 25 },
          2: { cellWidth: 10, halign: 'center' },
          3: { cellWidth: 20, halign: 'right', fontStyle: 'bold' }
        },
        theme: 'plain'
      });

      const dishTableEnd = doc.lastAutoTable.finalY;
      const bottomSectionY = Math.max(expTableEnd, dishTableEnd) + 8;

      // 4. Bottom Table: SALES CONTRIBUTION BY CATEGORY (Full Width 182mm)
      const catRows = catList.map(c => [
        c.category,
        String(c.itemsSold),
        "INR " + c.revenue.toLocaleString('en-IN', {minimumFractionDigits: 2}),
        (grossSales > 0 ? ((c.revenue / grossSales) * 100).toFixed(1) + '%' : '0.0%')
      ]);
      if (catRows.length === 0) {
        catRows.push(["No category sales recorded", "0", "INR 0.00", "0.0%"]);
      }

      doc.autoTable({
        startY: bottomSectionY,
        margin: { left: margin },
        tableWidth: contentWidth,
        head: [[
          { content: "SALES CONTRIBUTION BY CATEGORY", colSpan: 4, styles: { fillColor: [17, 24, 39], textColor: [255, 255, 255], fontStyle: 'bold', halign: 'left', fontSize: 8 } }
        ], [
          "Category", "Items Sold", "Total Revenue", "Revenue Share"
        ]],
        body: catRows,
        headStyles: {
          fillColor: [243, 244, 246],
          textColor: [55, 65, 81],
          fontStyle: 'bold',
          fontSize: 7.2
        },
        bodyStyles: {
          fontSize: 6.8,
          textColor: [31, 41, 55],
          cellPadding: 2
        },
        columnStyles: {
          0: { cellWidth: 70 },
          1: { cellWidth: 32, halign: 'center' },
          2: { cellWidth: 45, halign: 'right' },
          3: { cellWidth: 35, halign: 'right' }
        },
        theme: 'plain'
      });

      // Page 1 Footer
      doc.setFont("helvetica", "normal");
      doc.setFontSize(6.2);
      doc.setTextColor(156, 163, 175);
      doc.text("CONFIDENTIAL BUSINESS REPORT \\u2022 TALKING TABLES POS SYSTEM \\u2022 PAGE 1 OF 2", pageWidth / 2, pageHeight - 8, { align: "center" });

      // =========================================================================
      // PAGE 2: TRANSACTION LEDGER & EXECUTIVE SIGN-OFF
      // =========================================================================
      doc.addPage();

      // Transaction Ledger Table Header (Dark Navy)
      const ledgerRows = bills.map((b, idx) => {
        const itemCount = (b.items || []).reduce((sum, it) => sum + (it.qty || 1), 0);
        return [
          String(idx + 1),
          b.id,
          b.time || '-',
          b.table || 'Dine-In',
          itemCount + " items",
          "INR " + (b.subtotal || b.grandTotal || 0).toLocaleString('en-IN', {minimumFractionDigits: 2}),
          "INR " + (b.grandTotal || b.subtotal || 0).toLocaleString('en-IN', {minimumFractionDigits: 2})
        ];
      });
      if (ledgerRows.length === 0) {
        ledgerRows.push(["-", "No transactions recorded for this period", "-", "-", "0", "INR 0.00", "INR 0.00"]);
      }

      doc.autoTable({
        startY: 14,
        margin: { left: margin },
        tableWidth: contentWidth,
        head: [[
          { content: "TRANSACTION LEDGER (" + bills.length + " BILLS)", colSpan: 7, styles: { fillColor: [17, 24, 39], textColor: [255, 255, 255], fontStyle: 'bold', halign: 'left', fontSize: 8.5 } }
        ], [
          "#", "Bill No", "Time", "Table / Type", "Items", "Subtotal", "Total"
        ]],
        body: ledgerRows,
        foot: [[
          { content: "TOTAL SUM:", colSpan: 5, styles: { halign: 'right', fontStyle: 'bold', fontSize: 7.5 } },
          "INR " + grossSales.toLocaleString('en-IN', {minimumFractionDigits: 2}),
          "INR " + grossSales.toLocaleString('en-IN', {minimumFractionDigits: 2})
        ]],
        headStyles: {
          fillColor: [243, 244, 246],
          textColor: [55, 65, 81],
          fontStyle: 'bold',
          fontSize: 7.2
        },
        bodyStyles: {
          fontSize: 6.8,
          textColor: [31, 41, 55],
          cellPadding: 2.2
        },
        footStyles: {
          fillColor: [243, 244, 246],
          textColor: [17, 24, 39],
          fontStyle: 'bold',
          fontSize: 7.5
        },
        columnStyles: {
          0: { cellWidth: 10, halign: 'center' },
          1: { cellWidth: 35, fontStyle: 'bold' },
          2: { cellWidth: 20, halign: 'center' },
          3: { cellWidth: 42 },
          4: { cellWidth: 25, halign: 'center' },
          5: { cellWidth: 25, halign: 'right' },
          6: { cellWidth: 25, halign: 'right', fontStyle: 'bold', textColor: [217, 119, 6] }
        },
        theme: 'plain'
      });

      const ledgerFinalY = doc.lastAutoTable.finalY;
      const signY = Math.max(ledgerFinalY + 28, 215);

      // Signatures & Official Seal Block
      // Column 1: Cashier
      doc.setDrawColor(203, 213, 225);
      doc.setLineDashPattern([1.5, 1.5], 0);
      doc.line(margin, signY, margin + 50, signY);
      doc.setLineDashPattern([], 0); // reset

      doc.setFont("helvetica", "bold");
      doc.setFontSize(7.5);
      doc.setTextColor(17, 24, 39);
      doc.text("CASHIER / SHIFT INCHARGE", margin + 25, signY + 5, { align: "center" });
      doc.setFont("helvetica", "normal");
      doc.setFontSize(6.5);
      doc.setTextColor(107, 114, 128);
      doc.text("Prepared By", margin + 25, signY + 9, { align: "center" });

      // Column 2: Restaurant Manager
      const col2X = margin + 65;
      doc.setLineDashPattern([1.5, 1.5], 0);
      doc.line(col2X, signY, col2X + 50, signY);
      doc.setLineDashPattern([], 0);

      doc.setFont("helvetica", "bold");
      doc.setFontSize(7.5);
      doc.setTextColor(17, 24, 39);
      doc.text("RESTAURANT MANAGER", col2X + 25, signY + 5, { align: "center" });
      doc.setFont("helvetica", "normal");
      doc.setFontSize(6.5);
      doc.setTextColor(107, 114, 128);
      doc.text("Audited & Verified By", col2X + 25, signY + 9, { align: "center" });

      // Column 3: Official Seal Box
      const sealX = margin + 130;
      doc.setFillColor(255, 255, 255);
      doc.setDrawColor(203, 213, 225);
      doc.roundedRect(sealX, signY - 8, 48, 20, 1.5, 1.5, 'D');

      doc.setFont("helvetica", "bold");
      doc.setFontSize(6);
      doc.setTextColor(156, 163, 175);
      doc.text("OFFICIAL SEAL", sealX + 24, signY - 2, { align: "center" });
      doc.setFontSize(7.5);
      doc.setTextColor(17, 24, 39);
      doc.text("TALKING TABLES", sealX + 24, signY + 4, { align: "center" });
      doc.setFont("helvetica", "normal");
      doc.setFontSize(6.5);
      doc.setTextColor(107, 114, 128);
      doc.text("Vadlamudi Branch", sealX + 24, signY + 9, { align: "center" });

      // Page 2 Footer
      doc.setFont("helvetica", "normal");
      doc.setFontSize(6.2);
      doc.setTextColor(156, 163, 175);
      doc.text("CONFIDENTIAL BUSINESS REPORT \\u2022 TALKING TABLES POS SYSTEM \\u2022 GENERATED " + genTimestamp, pageWidth / 2, pageHeight - 11, { align: "center" });
      doc.setFontSize(5.8);
      doc.text("Software Engineered by KORAXA TECHNOLOGIES \\u2022 Startup Owner & Architect: K. Midhun", pageWidth / 2, pageHeight - 7, { align: "center" });

      return doc;
    }

    // SIMULTANEOUS LOCAL PDF DOWNLOAD & IMMEDIATE DIRECT WHATSAPP FILE DISPATCH
    function downloadAndWhatsAppReport() {
      const today = getTodayISO();
      const fromDate = document.getElementById('reportFromDate')?.value || today;
      const toDate = document.getElementById('reportToDate')?.value || today;
      const filename = 'Talking_Tables_Executive_Sales_Report_' + fromDate + '_to_' + toDate + '.pdf';

      // 1. Build Exact Attached-Template PDF
      const doc = createReportJsPdfDocument();
      
      // 2. Direct Local File Download (Immediate trigger to Downloads folder)
      doc.save(filename);
      showToast("Sales Report PDF downloaded locally to your computer!", "success");
      playBeep(900);

      // 3. Prepare Binary PDF Document File
      const pdfBlob = doc.output('blob');
      const pdfFile = new File([pdfBlob], filename, { type: 'application/pdf' });
      const targetPhone = (appData.settings && appData.settings.whatsappPhone) || "+919346477777";
      const cleanPhone = targetPhone.replace(/[^0-9]/g, '');

      // 4. Native Direct File Sharing (Web Share API Level 2 - Shares actual PDF file directly to WhatsApp)
      if (navigator.canShare && navigator.canShare({ files: [pdfFile] })) {
        navigator.share({
          title: filename,
          text: 'Talking Tables Executive Sales & Revenue Audit Report (' + fromDate + ' to ' + toDate + ')',
          files: [pdfFile]
        }).then(() => {
          showToast("PDF document shared directly to WhatsApp!", "success");
        }).catch(err => {
          if (err.name !== 'AbortError') console.log("Web Share error:", err);
        });
      }

      // 5. Direct Dispatch to Local Background Daemon (Port 5005)
      try {
        const base64Pdf = doc.output('datauristring').split(',')[1];
        fetch('http://localhost:5005/send-pdf', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            filename: filename,
            pdfBase64: base64Pdf,
            targetPhone: cleanPhone,
            date: today
          })
        }).then(res => res.json()).then(data => {
          console.log("[DISPATCHER]", data);
        }).catch(e => {
          // Daemon optional
        });
      } catch(e) {}

      // 6. Launch WhatsApp Web / Desktop for Target Owner Contact
      setTimeout(() => {
        window.open('https://web.whatsapp.com/send?phone=' + cleanPhone, '_blank');
      }, 500);
    }
"""

text = re.sub(report_funcs_old_regex, lambda m: new_report_funcs, text)

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS: template.html updated with attached template UI and report engine!")
