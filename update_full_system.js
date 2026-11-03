const fs = require('fs');

let html = fs.readFileSync('template.html', 'utf8');

// =========================================================================
// 1. UPDATE generateThermalReceiptHtml WITH DYNAMIC UPI PAYMENT QR CODE
// =========================================================================
const thermalReceiptMarker = `            <!-- NET PAYABLE AMOUNT (NO UPI, NO CASH, NO CARD) -->
            <div style="border-top: 1.5px dashed #000; border-bottom: 2px solid #000; padding: 3px 0; margin: 4px 0; display: flex; justify-content: space-between; font-size: 13px; font-weight: 800;">
              <span>NET PAYABLE:</span>
              <span style="padding-right: 1.5mm;">₹\${grandTotal.toFixed(2)}</span>
            </div>
          </div>`;

const thermalReceiptQrReplacement = `            <!-- NET PAYABLE AMOUNT (NO UPI, NO CASH, NO CARD OPTIONS ON BILL) -->
            <div style="border-top: 1.5px dashed #000; border-bottom: 2px solid #000; padding: 3px 0; margin: 4px 0; display: flex; justify-content: space-between; font-size: 13px; font-weight: 800;">
              <span>NET PAYABLE:</span>
              <span style="padding-right: 1.5mm;">₹\${grandTotal.toFixed(2)}</span>
            </div>
          </div>

          <!-- DYNAMIC UPI PAYMENT QR CODE (EXACT BILL AMOUNT) -->
          \${qrHtml}`;

// QR code generation logic inside generateThermalReceiptHtml
const qrGenLogic = `
      // Dynamic UPI Payment QR Code for exact bill amount
      let qrHtml = '';
      try {
        const upiId = settings.upiId || '9346477777@upi';
        const payee = (settings.restaurantName || 'TALKING TABLES').replace(/[^a-zA-Z0-9 ]/g, '');
        const upiUrl = \`upi://pay?pa=\${upiId}&pn=\${encodeURIComponent(payee)}&am=\${grandTotal.toFixed(2)}&cu=INR&tn=Bill-\${bill.id || 'TT'}\`;
        
        if (typeof QRCode !== 'undefined') {
          const tempDiv = document.createElement('div');
          new QRCode(tempDiv, {
            text: upiUrl,
            width: 140,
            height: 140,
            colorDark: "#000000",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.M
          });
          const canvas = tempDiv.querySelector('canvas');
          const qrDataUrl = canvas ? canvas.toDataURL('image/png') : (tempDiv.querySelector('img')?.src || '');
          if (qrDataUrl) {
            qrHtml = \`
              <div style="text-align: center; margin: 5px 0 2px 0;">
                <div style="font-size: 9px; font-weight: 800; letter-spacing: 0.3px; margin-bottom: 2px;">SCAN TO PAY VIA UPI (₹\${grandTotal.toFixed(2)})</div>
                <img src="\${qrDataUrl}" alt="UPI QR" style="width: 30mm; height: 30mm; margin: 0 auto; display: block; image-rendering: pixelated;" />
                <div style="font-size: 7.5px; font-weight: 700; margin-top: 1.5px;">GPay &bull; PhonePe &bull; Paytm &bull; BHIM</div>
                <div style="font-size: 7px; color: #333;">UPI: \${upiId}</div>
              </div>
              <div style="border-top: 1px dashed #000; margin: 3px 0;"></div>
            \`;
          }
        }
      } catch (err) {
        console.warn("Thermal QR gen error:", err);
      }
`;

if (html.includes(thermalReceiptMarker)) {
  html = html.replace(thermalReceiptMarker, thermalReceiptQrReplacement);
  // Also insert qrGenLogic before rowsHtml or logoHtml
  html = html.replace(
    'const totalItemsCount = (bill.items || []).length;',
    'const totalItemsCount = (bill.items || []).length;\n' + qrGenLogic
  );
  console.log('1. Embedded Dynamic UPI Payment QR Code generator into thermal receipt');
}

// =========================================================================
// 2. ITEM AVAILABILITY TOGGLE & CONTINUOUS ITEM IDS IN POS CARDS
// =========================================================================
const oldRenderMenuItems = `    function renderMenuItems() {
      const query = (document.getElementById('menuSearch')?.value || '').toLowerCase().trim();
      const grid = document.getElementById('itemsGrid');

      const filtered = appData.menu.filter(item => {
        const matchCat = selectedCategory === "All" || item.category === selectedCategory;
        const matchQuery = item.name.toLowerCase().includes(query) || (item.tag && item.tag.toLowerCase().includes(query));
        const matchDiet = selectedDiet === 'all' || (selectedDiet === 'veg' && item.isVeg) || (selectedDiet === 'non-veg' && !item.isVeg);
        return matchCat && matchQuery && matchDiet;
      });

      document.getElementById('menuItemCount').innerText = filtered.length + ' dishes in menu';

      if (filtered.length === 0) {
        grid.innerHTML = \`
          <div class="col-span-full py-16 text-center text-slate-500">
            <i class="fa-solid fa-utensils text-4xl mb-2 text-slate-600"></i>
            <p class="text-sm font-bold">No dishes found</p>
            <p class="text-xs text-slate-500">Search another keyword or change category</p>
          </div>
        \`;
        return;
      }

      grid.innerHTML = filtered.map(item => {
        const inCartItem = cart.find(c => c.id === item.id);
        const inCartQty = inCartItem ? inCartItem.qty : 0;
        const isSoldOut = item.inStock === false;

        return \`
          <div class="theme-card rounded-2xl p-3 flex flex-col justify-between hover:border-amber-400 transition select-none relative \${isSoldOut ? 'opacity-40 pointer-events-none' : ''}">
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <span class="\${item.isVeg ? 'veg-dot' : 'non-veg-dot'}"></span>
                <span class="text-[9px] font-black uppercase text-amber-300/80 bg-black/40 px-2 py-0.5 rounded-md border border-white/5">
                  \${item.tag || item.category}
                </span>
              </div>
              <h4 class="font-bold text-slate-100 text-xs sm:text-sm leading-snug line-clamp-2 font-heading">
                \${item.name}
              </h4>
            </div>

            <div class="mt-3 pt-2 border-t border-white/5 flex items-center justify-between">
              <span class="text-base font-black gold-gradient-text font-mono">₹\${item.price}</span>
              
              \${inCartQty > 0 ? \`
                <div class="flex items-center border border-amber-500/50 rounded-xl overflow-hidden bg-black/60 shadow">
                  <button onclick="changeCartQty('\${item.id}', -1)" class="w-6 h-6 flex items-center justify-center text-amber-300 hover:bg-amber-500/20 font-bold">-</button>
                  <span class="w-6 text-center text-xs font-bold text-amber-300 font-mono">\${inCartQty}</span>
                  <button onclick="changeCartQty('\${item.id}', 1)" class="w-6 h-6 flex items-center justify-center text-amber-300 hover:bg-amber-500/20 font-bold">+</button>
                </div>
              \` : \`
                <button onclick="addToCart('\${item.id}')" class="px-3 py-1 rounded-xl gold-gradient-btn hover:brightness-110 text-slate-950 font-black text-xs flex items-center gap-1 shadow transition active:scale-95">
                  <i class="fa-solid fa-plus text-[10px]"></i> Add
                </button>
              \`}
            </div>
          </div>
        \`;
      }).join('');
    }`;

const newRenderMenuItems = `    // CONTINUOUS ITEM ID GENERATOR
    function getNextItemId() {
      let maxNum = 0;
      (appData.menu || []).forEach(item => {
        const m = item.id && item.id.match(/^TT-(\\d+)$/i);
        if (m) {
          const num = parseInt(m[1], 10);
          if (num > maxNum) maxNum = num;
        }
      });
      return 'TT-' + String(maxNum + 1).padStart(3, '0');
    }

    // ITEM AVAILABILITY TOGGLER (SYNCED ACROSS POS & MENU)
    function toggleItemAvailability(dishId, event) {
      if (event) event.stopPropagation();
      const dish = (appData.menu || []).find(d => d.id === dishId);
      if (!dish) return;
      dish.isAvailable = dish.isAvailable === false ? true : false;
      dish.inStock = dish.isAvailable;
      saveAppData();
      renderMenuItems();
      if (typeof renderMenuManagerList === 'function') renderMenuManagerList();
      showToast(dish.name + ' is now ' + (dish.isAvailable ? 'In Stock' : 'Sold Out'), dish.isAvailable ? 'success' : 'warning');
      playBeep(dish.isAvailable ? 1000 : 500, 'sine', 0.05);
    }

    function renderMenuItems() {
      const query = (document.getElementById('menuSearch')?.value || '').toLowerCase().trim();
      const grid = document.getElementById('itemsGrid');

      const filtered = appData.menu.filter(item => {
        const matchCat = selectedCategory === "All" || item.category === selectedCategory;
        const matchQuery = item.name.toLowerCase().includes(query) || 
                           (item.id && item.id.toLowerCase().includes(query)) ||
                           (item.tag && item.tag.toLowerCase().includes(query));
        const matchDiet = selectedDiet === 'all' || (selectedDiet === 'veg' && item.isVeg) || (selectedDiet === 'non-veg' && !item.isVeg);
        return matchCat && matchQuery && matchDiet;
      });

      document.getElementById('menuItemCount').innerText = filtered.length + ' dishes in menu';

      if (filtered.length === 0) {
        grid.innerHTML = \`
          <div class="col-span-full py-16 text-center text-slate-500">
            <i class="fa-solid fa-utensils text-4xl mb-2 text-slate-600"></i>
            <p class="text-sm font-bold">No dishes found</p>
            <p class="text-xs text-slate-500">Search by dish name or Item ID (e.g. TT-001)</p>
          </div>
        \`;
        return;
      }

      grid.innerHTML = filtered.map(item => {
        const inCartItem = cart.find(c => c.id === item.id);
        const inCartQty = inCartItem ? inCartItem.qty : 0;
        const isAvailable = item.isAvailable !== false && item.inStock !== false;

        return \`
          <div class="theme-card rounded-2xl p-3 flex flex-col justify-between hover:border-amber-400 transition select-none relative \${!isAvailable ? 'opacity-55 border-rose-500/40 bg-rose-950/20' : ''}">
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <div class="flex items-center gap-1.5">
                  <span class="\${item.isVeg ? 'veg-dot' : 'non-veg-dot'}"></span>
                  <span class="text-[10px] font-mono font-bold text-amber-400 bg-amber-500/10 px-1.5 py-0.5 rounded border border-amber-500/30">\${item.id}</span>
                </div>
                
                <!-- Quick Item Availability Toggle on POS Card -->
                <button onclick="toggleItemAvailability('\${item.id}', event)" title="Click to toggle availability" class="text-[10px] px-2 py-0.5 rounded-full font-bold flex items-center gap-1 transition \${isAvailable ? 'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 hover:bg-rose-500/20 hover:text-rose-300' : 'bg-rose-500/20 text-rose-300 border border-rose-500/40 hover:bg-emerald-500/20 hover:text-emerald-300'}">
                  <span class="w-1.5 h-1.5 rounded-full \${isAvailable ? 'bg-emerald-400' : 'bg-rose-400'}"></span>
                  \${isAvailable ? 'In Stock' : 'Sold Out'}
                </button>
              </div>
              <h4 class="font-bold text-slate-100 text-xs sm:text-sm leading-snug line-clamp-2 font-heading">
                \${item.name}
              </h4>
              <p class="text-[10px] text-slate-400 mt-0.5">\${item.category}\${item.tag ? ' &bull; ' + item.tag : ''}</p>
            </div>

            <div class="mt-3 pt-2 border-t border-white/5 flex items-center justify-between">
              <span class="text-base font-black gold-gradient-text font-mono">₹\${item.price}</span>
              
              \${!isAvailable ? \`
                <span class="px-2.5 py-1 rounded-xl bg-rose-500/15 text-rose-400 border border-rose-500/30 font-bold text-xs">
                  Sold Out
                </span>
              \` : (inCartQty > 0 ? \`
                <div class="flex items-center border border-amber-500/50 rounded-xl overflow-hidden bg-black/60 shadow">
                  <button onclick="changeCartQty('\${item.id}', -1)" class="w-6 h-6 flex items-center justify-center text-amber-300 hover:bg-amber-500/20 font-bold">-</button>
                  <span class="w-6 text-center text-xs font-bold text-amber-300 font-mono">\${inCartQty}</span>
                  <button onclick="changeCartQty('\${item.id}', 1)" class="w-6 h-6 flex items-center justify-center text-amber-300 hover:bg-amber-500/20 font-bold">+</button>
                </div>
              \` : \`
                <button onclick="addToCart('\${item.id}')" class="px-3 py-1 rounded-xl gold-gradient-btn hover:brightness-110 text-slate-950 font-black text-xs flex items-center gap-1 shadow transition active:scale-95">
                  <i class="fa-solid fa-plus text-[10px]"></i> Add
                </button>
              \`)}
            </div>
          </div>
        \`;
      }).join('');
    }`;

if (html.includes('function renderMenuItems() {')) {
  html = html.replace(oldRenderMenuItems, newRenderMenuItems);
  console.log('2. Updated renderMenuItems with continuous Item IDs, search by ID, and In Stock/Sold Out quick toggles');
}

// Update addToCart to block sold out items
html = html.replace(
  `function addToCart(dishId) {
      const dish = appData.menu.find(d => d.id === dishId);
      if (!dish) return;`,
  `function addToCart(dishId) {
      const dish = appData.menu.find(d => d.id === dishId);
      if (!dish) return;
      if (dish.isAvailable === false || dish.inStock === false) {
        showToast('"' + dish.name + '" is currently marked Sold Out!', "error");
        playBeep(400, 'sawtooth', 0.1);
        return;
      }`
);

// =========================================================================
// 3. CART SEARCH & REFINED CART RENDERING
// =========================================================================
const oldUpdateCartTotals = `    function updateCartTotals() {
      const listEl = document.getElementById('cartItemsList');
      const subtotalEl = document.getElementById('cartSubtotal');
      const discountDisplay = document.getElementById('cartDiscountDisplay');
      const taxAmountEl = document.getElementById('cartTaxAmount');
      const grandTotalEl = document.getElementById('cartGrandTotal');
      const discountInput = document.getElementById('cartDiscount');

      const subtotal = cart.reduce((sum, item) => sum + item.total, 0);
      let discount = parseFloat(discountInput?.value || 0) || 0;
      if (discount > subtotal) discount = subtotal;

      const taxableAmount = Math.max(0, subtotal - discount);
      const enableTax = appData.settings.enableTax !== false;
      const taxRate = enableTax ? (parseFloat(appData.settings.taxRate) || 5) : 0;
      const tax = (taxableAmount * taxRate) / 100;
      const grandTotal = Math.round(taxableAmount + tax);

      if (subtotalEl) subtotalEl.innerText = '₹' + subtotal.toFixed(2);
      if (discountDisplay) discountDisplay.innerText = '- ₹' + discount.toFixed(2);
      if (taxAmountEl) taxAmountEl.innerText = '₹' + tax.toFixed(2);
      if (grandTotalEl) grandTotalEl.innerText = '₹' + grandTotal.toFixed(2);

      if (cart.length === 0) {
        listEl.innerHTML = \`
          <div class="h-full flex flex-col items-center justify-center text-slate-500 py-12 text-center">
            <i class="fa-solid fa-basket-shopping text-3xl mb-2 text-slate-600"></i>
            <p class="text-xs font-bold text-slate-400">Cart is Empty</p>
            <p class="text-[10px] text-slate-500">Tap dish "+ Add" buttons to start billing</p>
          </div>
        \`;
        return;
      }

      listEl.innerHTML = cart.map(item => \`
        <div class="p-2.5 rounded-xl bg-black/30 border border-white/5 flex items-center justify-between text-xs">
          <div class="flex items-center gap-2">
            <span class="\${item.isVeg ? 'veg-dot' : 'non-veg-dot'}"></span>
            <div>
              <p class="font-bold text-slate-200 line-clamp-1 font-heading">\${item.name}</p>
              <p class="text-[10px] text-slate-400 font-mono">₹\${item.price} &times; \${item.qty}</p>
            </div>
          </div>
          <div class="flex items-center gap-2.5">
            <span class="font-mono font-bold text-amber-300">₹\${item.total}</span>
            <div class="flex items-center border border-white/10 rounded-lg overflow-hidden bg-black/40">
              <button onclick="changeCartQty('\${item.id}', -1)" class="w-5 h-5 flex items-center justify-center text-slate-300 hover:text-white">-</button>
              <span class="w-5 text-center font-mono font-bold text-[10px] text-amber-300">\${item.qty}</span>
              <button onclick="changeCartQty('\${item.id}', 1)" class="w-5 h-5 flex items-center justify-center text-slate-300 hover:text-white">+</button>
            </div>
          </div>
        </div>
      \`).join('');
    }`;

const newUpdateCartTotals = `    function renderCartItems() {
      const listEl = document.getElementById('cartItemsList');
      const summaryEl = document.getElementById('cartItemsSummaryText');
      const q = (document.getElementById('cartSearchInput')?.value || '').toLowerCase().trim();

      const totalItemsCount = cart.length;
      const totalQty = cart.reduce((s, it) => s + it.qty, 0);
      if (summaryEl) {
        summaryEl.innerText = \`\${totalItemsCount} dish\${totalItemsCount !== 1 ? 'es' : ''} &bull; \${totalQty} total qty\`;
      }

      if (cart.length === 0) {
        listEl.innerHTML = \`
          <div class="h-full flex flex-col items-center justify-center text-slate-500 py-12 text-center">
            <i class="fa-solid fa-basket-shopping text-3xl mb-2 text-slate-600"></i>
            <p class="text-xs font-bold text-slate-400">Cart is Empty</p>
            <p class="text-[10px] text-slate-500">Tap dish "+ Add" buttons to start billing</p>
          </div>
        \`;
        return;
      }

      const filteredCart = q ? cart.filter(it => it.name.toLowerCase().includes(q) || (it.id && it.id.toLowerCase().includes(q))) : cart;

      if (filteredCart.length === 0) {
        listEl.innerHTML = \`
          <div class="py-8 text-center text-slate-500">
            <p class="text-xs font-bold text-slate-400">No matching items in cart</p>
            <p class="text-[10px] text-slate-500">Clear search query</p>
          </div>
        \`;
        return;
      }

      listEl.innerHTML = filteredCart.map(item => \`
        <div class="p-2.5 rounded-xl bg-black/30 border border-white/5 flex items-center justify-between text-xs">
          <div class="flex items-center gap-2">
            <span class="\${item.isVeg ? 'veg-dot' : 'non-veg-dot'}"></span>
            <div>
              <div class="flex items-center gap-1.5">
                <span class="text-[9px] font-mono font-bold text-amber-400/90">\${item.id}</span>
                <p class="font-bold text-slate-200 line-clamp-1 font-heading">\${item.name}</p>
              </div>
              <p class="text-[10px] text-slate-400 font-mono">₹\${item.price} &times; \${item.qty}</p>
            </div>
          </div>
          <div class="flex items-center gap-2.5">
            <span class="font-mono font-bold text-amber-300">₹\${item.total}</span>
            <div class="flex items-center border border-white/10 rounded-lg overflow-hidden bg-black/40">
              <button onclick="changeCartQty('\${item.id}', -1)" class="w-5 h-5 flex items-center justify-center text-slate-300 hover:text-white">-</button>
              <span class="w-5 text-center font-mono font-bold text-[10px] text-amber-300">\${item.qty}</span>
              <button onclick="changeCartQty('\${item.id}', 1)" class="w-5 h-5 flex items-center justify-center text-slate-300 hover:text-white">+</button>
            </div>
          </div>
        </div>
      \`).join('');
    }

    function updateCartTotals() {
      const subtotalEl = document.getElementById('cartSubtotal');
      const discountDisplay = document.getElementById('cartDiscountDisplay');
      const taxAmountEl = document.getElementById('cartTaxAmount');
      const grandTotalEl = document.getElementById('cartGrandTotal');
      const discountInput = document.getElementById('cartDiscount');

      const subtotal = cart.reduce((sum, item) => sum + item.total, 0);
      let discount = parseFloat(discountInput?.value || 0) || 0;
      if (discount > subtotal) discount = subtotal;

      const taxableAmount = Math.max(0, subtotal - discount);
      const enableTax = appData.settings.enableTax !== false;
      const taxRate = enableTax ? (parseFloat(appData.settings.taxRate) || 5) : 0;
      const tax = (taxableAmount * taxRate) / 100;
      const grandTotal = Math.round(taxableAmount + tax);

      if (subtotalEl) subtotalEl.innerText = '₹' + subtotal.toFixed(2);
      if (discountDisplay) discountDisplay.innerText = '- ₹' + discount.toFixed(2);
      if (taxAmountEl) taxAmountEl.innerText = '₹' + tax.toFixed(2);
      if (grandTotalEl) grandTotalEl.innerText = '₹' + grandTotal.toFixed(2);

      renderCartItems();
    }`;

if (html.includes('function updateCartTotals() {')) {
  html = html.replace(oldUpdateCartTotals, newUpdateCartTotals);
  console.log('3. Upgraded updateCartTotals and added renderCartItems with live in-cart search');
}

// =========================================================================
// 4. MENU SECTION CONTINUOUS ITEM IDS AND AVAILABILITY TOGGLES
// =========================================================================
html = html.replace(
  `const newId = "TT-" + (appData.menu.length + 1);`,
  `const newId = getNextItemId();`
);

// Update openAddDishModal to show continuous ID
html = html.replace(
  `function openAddDishModal() {
      document.getElementById('dishModalTitle').innerText = "Add New Dish";
      document.getElementById('dishEditId').value = "";`,
  `function openAddDishModal() {
      document.getElementById('dishModalTitle').innerText = "Add New Dish (" + getNextItemId() + ")";
      document.getElementById('dishEditId').value = "";`
);

fs.writeFileSync('template.html', html, 'utf8');
console.log('Saved template.html updates for POS cards, Cart Search, and Thermal UPI QR.');

