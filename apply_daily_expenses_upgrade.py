import sys

with open('template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the entire <section id="view-expenses"> with the upgraded easy-entry version
old_section_expenses = '''    <section id="view-expenses" class="tab-content hidden space-y-6">
      
      <div class="theme-surface p-5 rounded-2xl shadow-sm flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 class="text-lg font-extrabold gold-gradient-text font-brand uppercase tracking-wide">Talking Tables Daily Expense Ledger</h2>
          <p class="text-xs text-slate-400">Track Meat, Poultry, Groceries, Salaries &amp; LPG cylinders for net PnL</p>
        </div>
        <div class="flex items-center gap-2">
          <input type="date" id="expenseFilterDate" onchange="renderExpensesTable()" class="text-xs px-3 py-1.5 theme-input rounded-xl focus:outline-none">
          <button onclick="openExpenseModal()" class="px-3.5 py-1.5 gold-gradient-btn text-slate-950 font-bold rounded-xl text-xs flex items-center gap-1.5 shadow">
            <i class="fa-solid fa-plus"></i> Record Expense
          </button>
        </div>
      </div>

      <div class="theme-surface rounded-2xl shadow overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-black/30 border-b border-white/10 uppercase text-slate-400 font-bold tracking-wider">
              <tr>
                <th class="px-4 py-3">Date</th>
                <th class="px-4 py-3">Expense Category</th>
                <th class="px-4 py-3">Description / Vendor</th>
                <th class="px-4 py-3">Disbursed By</th>
                <th class="px-4 py-3 text-right">Amount (₹)</th>
                <th class="px-4 py-3 text-center">Action</th>
              </tr>
            </thead>
            <tbody id="expensesTableBody" class="divide-y divide-white/5">
              <!-- Injected via JS -->
            </tbody>
            <tfoot class="bg-black/40 border-t border-white/10 font-bold">
              <tr>
                <td colspan="4" class="px-4 py-3 uppercase text-right text-slate-300">Total Shift Expenses:</td>
                <td class="px-4 py-3 text-right text-rose-400 text-sm font-mono" id="expenseTotalAmount">₹0</td>
                <td></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

    </section>'''

new_section_expenses = '''    <section id="view-expenses" class="tab-content hidden space-y-6">
      
      <!-- Top Title & Date Filter Bar -->
      <div class="theme-surface p-5 rounded-3xl shadow-lg border border-rose-500/20 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="flex items-center gap-2">
            <h2 class="text-lg font-extrabold gold-gradient-text font-brand uppercase tracking-wide">Talking Tables Daily Expense Ledger</h2>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-500/15 text-rose-300 border border-rose-500/30">Easy Entry Enabled</span>
          </div>
          <p class="text-xs text-slate-400 mt-0.5">Quickly record Meat, Groceries, Chef Wages &amp; LPG cylinders with 1-tap presets</p>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs text-slate-400 font-semibold">Filter Date:</span>
          <input type="date" id="expenseFilterDate" onchange="renderExpensesTable()" class="text-xs px-3 py-1.5 theme-input rounded-xl focus:outline-none">
          <button onclick="openExpenseModal()" class="px-3.5 py-1.5 theme-card hover:border-amber-400 text-slate-300 hover:text-white font-bold rounded-xl text-xs flex items-center gap-1.5 transition">
            <i class="fa-solid fa-sliders text-amber-400"></i> Advanced Form
          </button>
        </div>
      </div>

      <!-- ========================================================
           EASY DIRECT EXPENSE ENTRY WIDGET (DAILY EXPENSES TAB)
           ======================================================== -->
      <div class="theme-surface p-4 sm:p-5 rounded-3xl shadow-lg border border-rose-500/30 space-y-3.5 bg-gradient-to-r from-rose-950/20 via-black/40 to-black/20">
        
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse"></span>
            <h3 class="text-sm font-extrabold uppercase tracking-wide text-rose-400 font-brand">
              Easy Expense Entry
            </h3>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-rose-500/15 text-rose-300 border border-rose-500/30">
              Instant Ledger Sync
            </span>
          </div>
          <span class="text-[11px] text-slate-400">
            Click 1-tap chip or enter amount to add expense voucher immediately:
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
            <select id="quickExpCategoryExpensesTab" class="quick-exp-category-input w-full px-3 py-2 theme-input rounded-xl text-xs font-semibold focus:outline-none">
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
            <input type="text" id="quickExpDescExpensesTab" placeholder="e.g. 20kg Chicken from Wholesale" class="quick-exp-desc-input w-full px-3 py-2 theme-input rounded-xl text-xs focus:outline-none" onkeydown="if(event.key==='Enter') document.getElementById('quickExpAmountExpensesTab').focus()">
          </div>

          <div class="sm:col-span-3">
            <label class="text-[10px] uppercase font-bold text-slate-400 block mb-1">Amount (₹)</label>
            <div class="relative">
              <span class="absolute left-3 top-2 text-rose-400 font-extrabold text-xs">₹</span>
              <input type="number" id="quickExpAmountExpensesTab" placeholder="Amount (e.g. 3500)" class="quick-exp-amount-input w-full pl-6 pr-3 py-2 theme-input rounded-xl text-xs font-mono font-black text-rose-400 focus:outline-none" onkeydown="if(event.key==='Enter') submitQuickExpense()">
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

      <!-- Expenses Ledger Table -->
      <div class="theme-surface rounded-3xl shadow overflow-hidden border border-white/5">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="bg-black/40 border-b border-white/10 uppercase text-slate-400 font-bold tracking-wider">
              <tr>
                <th class="px-4 py-3">Date</th>
                <th class="px-4 py-3">Expense Category</th>
                <th class="px-4 py-3">Description / Vendor</th>
                <th class="px-4 py-3">Disbursed By</th>
                <th class="px-4 py-3 text-right">Amount (₹)</th>
                <th class="px-4 py-3 text-center">Action</th>
              </tr>
            </thead>
            <tbody id="expensesTableBody" class="divide-y divide-white/5">
              <!-- Injected via JS -->
            </tbody>
            <tfoot class="bg-black/50 border-t border-white/10 font-bold">
              <tr>
                <td colspan="4" class="px-4 py-3 uppercase text-right text-slate-300">Total Shift Expenses:</td>
                <td class="px-4 py-3 text-right text-rose-400 text-sm font-mono" id="expenseTotalAmount">₹0</td>
                <td></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>

    </section>'''

if old_section_expenses in content:
    content = content.replace(old_section_expenses, new_section_expenses)
    print('SUCCESS: Replaced <section id="view-expenses"> with Easy Expense Entry widget.')
else:
    print('WARNING: old_section_expenses not found.')

# 2. Update quickSelectExpenseCat and submitQuickExpense JS functions to support both tabs
old_js_funcs = '''    function quickSelectExpenseCat(category, defaultDesc) {
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
    }'''

new_js_funcs = '''    function quickSelectExpenseCat(category, defaultDesc) {
      // Synchronize in both Daily Expenses tab and Sales P&L tab
      const catEls = document.querySelectorAll('.quick-exp-category-input, #quickExpCategory, #expenseCategoryInput');
      const descEls = document.querySelectorAll('.quick-exp-desc-input, #quickExpDesc, #expenseDescInput');
      const amtEls = document.querySelectorAll('.quick-exp-amount-input, #quickExpAmount, #expenseAmountInput');
      
      catEls.forEach(el => { el.value = category; });
      descEls.forEach(el => { el.value = defaultDesc; });

      // Focus the currently visible Amount input
      for (const el of amtEls) {
        if (el && el.offsetParent !== null) {
          el.focus();
          el.select();
          return;
        }
      }
      if (amtEls[0]) amtEls[0].focus();
    }

    function submitQuickExpense() {
      // Find the active tab's inputs
      const activeTab = document.querySelector('.tab-content:not(.hidden)');
      let catEl = activeTab?.querySelector('.quick-exp-category-input') || document.getElementById('quickExpCategoryExpensesTab') || document.getElementById('quickExpCategory');
      let descEl = activeTab?.querySelector('.quick-exp-desc-input') || document.getElementById('quickExpDescExpensesTab') || document.getElementById('quickExpDesc');
      let amtEl = activeTab?.querySelector('.quick-exp-amount-input') || document.getElementById('quickExpAmountExpensesTab') || document.getElementById('quickExpAmount');
      let dateEl = document.getElementById('expenseFilterDate') || document.getElementById('reportToDate');

      const cat = catEl?.value || 'Meat & Poultry';
      const desc = descEl?.value.trim();
      const amount = parseFloat(amtEl?.value) || 0;
      const date = dateEl?.value || getTodayISO();

      if (amount <= 0) {
        showToast("Please enter an expense amount (₹)", "error");
        if (amtEl) amtEl.focus();
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

      // Reset all amount and desc inputs across tabs
      document.querySelectorAll('.quick-exp-amount-input, #quickExpAmount, #quickExpAmountExpensesTab').forEach(el => el.value = '');
      document.querySelectorAll('.quick-exp-desc-input, #quickExpDesc, #quickExpDescExpensesTab').forEach(el => el.value = '');

      // Refresh all views instantly
      if (typeof renderExpensesTable === 'function') renderExpensesTable();
      if (typeof generateReportPreview === 'function') generateReportPreview();
      if (typeof renderDashboard === 'function') renderDashboard();

      showToast(`₹${amount.toLocaleString('en-IN')} ${cat} expense recorded!`, "success");
      playBeep(900);
    }'''

if old_js_funcs in content:
    content = content.replace(old_js_funcs, new_js_funcs)
    print('SUCCESS: Updated quickSelectExpenseCat and submitQuickExpense.')
else:
    print('WARNING: old_js_funcs not found.')

# 3. Add classes quick-exp-category-input, quick-exp-desc-input, quick-exp-amount-input to view-reports widget
content = content.replace('id="quickExpCategory" class="w-full', 'id="quickExpCategory" class="quick-exp-category-input w-full')
content = content.replace('id="quickExpDesc" placeholder="', 'id="quickExpDesc" class="quick-exp-desc-input w-full px-3 py-2 theme-input rounded-xl text-xs focus:outline-none" placeholder="')
content = content.replace('id="quickExpAmount" placeholder="', 'id="quickExpAmount" class="quick-exp-amount-input w-full pl-6 pr-3 py-2 theme-input rounded-xl text-xs font-mono font-black text-rose-400 focus:outline-none" placeholder="')

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('template.html successfully updated with Daily Expenses easy-entry!')

