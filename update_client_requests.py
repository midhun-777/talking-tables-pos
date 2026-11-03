import sys

with open('template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Cart UI: Remove Guest Details input from Cart
old_cart_inputs = '''            <!-- Customer & Station Quick Input -->
            <div class="p-3 border-b border-white/5 grid grid-cols-2 gap-2 text-xs">
              <div>
                <label class="text-slate-400 font-semibold block mb-1">Customer Mobile / Name</label>
                <input type="text" id="customerPhone" placeholder="Mobile Number / Customer Name" class="w-full px-2.5 py-1.5 theme-input rounded-lg text-xs focus:outline-none">
              </div>
              <div>
                <label class="text-slate-400 font-semibold block mb-1">Assigned Table / Cabin</label>
                <input type="text" id="orderTableNo" value="Hall Table T-1" placeholder="Table / Cabin / Parcel" class="w-full px-2.5 py-1.5 theme-input rounded-lg text-xs focus:outline-none">
              </div>
            </div>'''

new_cart_inputs = '''            <!-- Station & Order Location Quick Bar (Streamlined: No Guest Details Required) -->
            <div class="p-3 border-b border-white/5 flex items-center justify-between gap-3 text-xs">
              <div class="flex-1">
                <label class="text-slate-400 font-semibold block mb-1">Assigned Table / Cabin / Location</label>
                <input type="text" id="orderTableNo" value="Hall Table T-1" placeholder="Table / Cabin / Parcel" class="w-full px-3 py-1.5 theme-input rounded-xl text-xs font-bold text-amber-400 focus:outline-none">
              </div>
              <!-- Hidden to ensure backward JS compatibility with zero errors -->
              <input type="hidden" id="customerPhone" value="">
            </div>'''

if old_cart_inputs in content:
    content = content.replace(old_cart_inputs, new_cart_inputs)
    print('SUCCESS: Updated Cart UI (Guest Details input removed).')
else:
    print('WARNING: old_cart_inputs not found.')

# 2. Update Bill Print: Remove GUEST row from generateThermalReceiptHtml
old_receipt_meta = '''          <!-- BILL METADATA (WITH RIGHT-EDGE SAFETY PADDING) -->
          <div style="font-size: 9px; line-height: 1.3;">
            <div style="display: flex; justify-content: space-between;">
              <span>BILL: <b>${bill.id || "#TT-1001"}</b></span>
              <span style="padding-right: 1.5mm;">${bill.date || getTodayISO()} ${bill.time || ''}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span>STATION: <b>${bill.table || "Dine-in"}</b></span>
              <span style="padding-right: 1.5mm;">GUEST: <b>${bill.customer || "Walk-in"}</b></span>
            </div>
          </div>'''

new_receipt_meta = '''          <!-- BILL METADATA (CLEAN BILL: ZERO GUEST DETAILS PER CLIENT SPECIFICATION) -->
          <div style="font-size: 9px; line-height: 1.3;">
            <div style="display: flex; justify-content: space-between;">
              <span>BILL: <b>${bill.id || "#TT-1001"}</b></span>
              <span style="padding-right: 1.5mm;">${bill.date || getTodayISO()} ${bill.time || ''}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span>STATION: <b>${bill.table || "Dine-in"}</b></span>
              <span style="padding-right: 1.5mm;">TYPE: <b>${bill.orderType || bill.mode || "Dine-In"}</b></span>
            </div>
          </div>'''

if old_receipt_meta in content:
    content = content.replace(old_receipt_meta, new_receipt_meta)
    print('SUCCESS: Updated Thermal Receipt (Guest details removed from bill print).')
else:
    print('WARNING: old_receipt_meta not found.')

# 3. Add Easy Expense Entry Widget in Sales Section (view-reports)
target_reports_anchor = '''        </div>
      </div>

      <!-- EXACT ATTACHED PDF TEMPLATE UI PREVIEW (CLEAN A4 WHITE SHEET) -->'''

easy_expense_widget = '''        </div>
      </div>

      <!-- ========================================================
           EASY DIRECT EXPENSE ENTRY WIDGET (SALES SECTION)
           ======================================================== -->
      <div class="theme-surface p-4 sm:p-5 rounded-3xl shadow-lg border border-rose-500/30 space-y-3.5 bg-gradient-to-r from-rose-950/20 via-black/40 to-black/20">
        
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse"></span>
            <h3 class="text-sm font-extrabold uppercase tracking-wide text-rose-400 font-brand">
              Easy Expense Entry
            </h3>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-500/15 text-rose-300 border border-rose-500/30">
              Instant P&amp;L Sync
            </span>
          </div>
          <span class="text-[11px] text-slate-400">
            Click 1-tap chip or enter amount to record directly into Sales Report:
          </span>
        </div>

        <!-- 1-Tap Quick Fill Category & Item Chips -->
        <div class="flex flex-wrap items-center gap-1.5">
          <button type="button" onclick="quickSelectExpenseCat('Meat & Poultry', '18kg Fresh Chicken & Tender Lamb')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-rose-950/40 hover:bg-rose-600/30 text-rose-200 border border-rose-500/30 active:scale-95 transition flex items-center gap-1.5">
            <span>🍗 Chicken &amp; Meat</span>
          </button>
          <button type="button" onclick="quickSelectExpenseCat('Groceries & Vegetables', 'Basmati Rice 50kg, Ghee & Spices')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-amber-950/40 hover:bg-amber-600/30 text-amber-200 border border-amber-500/30 active:scale-95 transition flex items-center gap-1.5">
            <span>🍚 Rice &amp; Groceries</span>
          </button>
          <button type="button" onclick="quickSelectExpenseCat('Commercial Gas & Fuel', 'Commercial 19kg LPG Cylinder')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-blue-950/40 hover:bg-blue-600/30 text-blue-200 border border-blue-500/30 active:scale-95 transition flex items-center gap-1.5">
            <span>⛽ LPG Gas Cylinder</span>
          </button>
          <button type="button" onclick="quickSelectExpenseCat('Staff Salaries & Wages', 'Daily Mandi Master Chef & Staff Wages')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-emerald-950/40 hover:bg-emerald-600/30 text-emerald-200 border border-emerald-500/30 active:scale-95 transition flex items-center gap-1.5">
            <span>👨‍🍳 Chef &amp; Staff Wages</span>
          </button>
          <button type="button" onclick="quickSelectExpenseCat('Maintenance & Utilities', 'Mandi Takeaway Boxes & Cleaning')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-purple-950/40 hover:bg-purple-600/30 text-purple-200 border border-purple-500/30 active:scale-95 transition flex items-center gap-1.5">
            <span>📦 Mandi Packaging</span>
          </button>
          <button type="button" onclick="quickSelectExpenseCat('Miscellaneous', 'Daily Operational Expense')" class="px-3 py-1.5 rounded-xl text-xs font-bold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-white/10 active:scale-95 transition flex items-center gap-1.5">
            <span>⚡ Other / Misc</span>
          </button>
        </div>

        <!-- Easy Entry Form (1 Clean Responsive Row) -->
        <div class="grid grid-cols-1 sm:grid-cols-12 gap-2.5 items-end pt-1">
          <div class="sm:col-span-3">
            <label class="text-[10px] uppercase font-bold text-slate-400 block mb-1">Expense Category</label>
            <select id="quickExpCategory" class="w-full px-3 py-2 theme-input rounded-xl text-xs font-semibold focus:outline-none">
              <option value="Meat & Poultry">Meat &amp; Poultry</option>
              <option value="Groceries & Vegetables">Groceries &amp; Vegetables</option>
              <option value="Commercial Gas & Fuel">Commercial Gas &amp; Fuel</option>
              <option value="Staff Salaries & Wages">Staff Salaries &amp; Wages</option>
              <option value="Maintenance & Utilities">Maintenance &amp; Utilities</option>
              <option value="Miscellaneous">Miscellaneous</option>
            </select>
          </div>

          <div class="sm:col-span-4">
            <label class="text-[10px] uppercase font-bold text-slate-400 block mb-1">Description / Vendor / Item</label>
            <input type="text" id="quickExpDesc" placeholder="e.g. 20kg Chicken from Wholesale" class="w-full px-3 py-2 theme-input rounded-xl text-xs focus:outline-none" onkeydown="if(event.key==='Enter') document.getElementById('quickExpAmount').focus()">
          </div>

          <div class="sm:col-span-3">
            <label class="text-[10px] uppercase font-bold text-slate-400 block mb-1">Amount (₹)</label>
            <div class="relative">
              <span class="absolute left-3 top-2 text-rose-400 font-extrabold text-xs">₹</span>
              <input type="number" id="quickExpAmount" placeholder="Amount (e.g. 3500)" class="w-full pl-6 pr-3 py-2 theme-input rounded-xl text-xs font-mono font-black text-rose-400 focus:outline-none" onkeydown="if(event.key==='Enter') submitQuickExpense()">
            </div>
          </div>

          <div class="sm:col-span-2">
            <button type="button" onclick="submitQuickExpense()" class="w-full py-2 bg-gradient-to-r from-rose-600 via-rose-500 to-amber-600 hover:from-rose-500 hover:to-amber-500 text-white font-black rounded-xl text-xs uppercase tracking-wider flex items-center justify-center gap-1.5 shadow-lg shadow-rose-600/30 active:scale-95 transition">
              <i class="fa-solid fa-plus text-xs"></i>
              <span>+ Add Expense</span>
            </button>
          </div>
        </div>

      </div>

      <!-- EXACT ATTACHED PDF TEMPLATE UI PREVIEW (CLEAN A4 WHITE SHEET) -->'''

if target_reports_anchor in content:
    content = content.replace(target_reports_anchor, easy_expense_widget)
    print('SUCCESS: Added Easy Expense Entry Widget in Sales Section.')
else:
    print('WARNING: target_reports_anchor not found.')

# 4. Add JS functions: quickSelectExpenseCat and submitQuickExpense, and update deleteExpense
new_js_funcs = '''    function quickSelectExpenseCat(category, defaultDesc) {
      const catEl = document.getElementById('quickExpCategory') || document.getElementById('expenseCategoryInput');
      const descEl = document.getElementById('quickExpDesc') || document.getElementById('expenseDescInput');
      const amtEl = document.getElementById('quickExpAmount') || document.getElementById('expenseAmountInput');
      
      if (catEl) catEl.value = category;
      if (descEl) descEl.value = defaultDesc;
      if (amtEl) {
        amtEl.focus();
        amtEl.select();
      }
    }

    function submitQuickExpense() {
      const cat = document.getElementById('quickExpCategory')?.value || 'Meat & Poultry';
      const desc = document.getElementById('quickExpDesc')?.value.trim();
      const amount = parseFloat(document.getElementById('quickExpAmount')?.value) || 0;
      const date = document.getElementById('reportToDate')?.value || document.getElementById('expenseFilterDate')?.value || getTodayISO();

      if (amount <= 0) {
        showToast("Please enter an expense amount (₹)", "error");
        document.getElementById('quickExpAmount')?.focus();
        return;
      }

      const finalDesc = desc || (cat + ' expense');
      const newExp = {
        id: "EXP-" + (Date.now().toString().slice(-6)),
        date: date,
        category: cat,
        description: finalDesc,
        amount: amount,
        paidBy: "Counter Cash"
      };

      appData.expenses.unshift(newExp);
      saveAppData();

      // Reset inputs
      if (document.getElementById('quickExpAmount')) document.getElementById('quickExpAmount').value = '';
      if (document.getElementById('quickExpDesc')) document.getElementById('quickExpDesc').value = '';

      // Refresh all views instantly
      if (typeof generateReportPreview === 'function') generateReportPreview();
      if (typeof renderExpensesTable === 'function') renderExpensesTable();
      if (typeof renderDashboard === 'function') renderDashboard();

      showToast(`₹${amount.toLocaleString('en-IN')} ${cat} expense recorded!`, "success");
      playBeep(900);
    }
'''

content = content.replace('function renderExpensesTable() {', new_js_funcs + '\n    function renderExpensesTable() {')

# Update deleteExpense to also call generateReportPreview
old_delete_exp = '''    function deleteExpense(expId) {
      if (!confirm("Delete this expense voucher?")) return;
      appData.expenses = appData.expenses.filter(e => e.id !== expId);
      saveAppData();
      renderExpensesTable();
      renderDashboard();
      showToast("Expense voucher removed", "info");
    }'''

new_delete_exp = '''    function deleteExpense(expId) {
      if (!confirm("Delete this expense voucher?")) return;
      appData.expenses = appData.expenses.filter(e => e.id !== expId);
      saveAppData();
      renderExpensesTable();
      renderDashboard();
      if (typeof generateReportPreview === 'function') generateReportPreview();
      showToast("Expense voucher removed", "info");
    }'''

if old_delete_exp in content:
    content = content.replace(old_delete_exp, new_delete_exp)
    print('SUCCESS: Updated deleteExpense with instant report sync.')

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('template.html successfully updated!')

