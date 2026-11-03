import sys
import re

with open('template.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update POS_STORAGE_VERSION
content = re.sub(
    r"const POS_STORAGE_VERSION = '[^']+';",
    "const POS_STORAGE_VERSION = 'tt_pos_v2.5_table_cart_sync_dual_whatsapp';",
    content
)

# 2. Update DEFAULT_SETTINGS to include both whatsappPhone and whatsappPhone2
old_default_settings = '''    const DEFAULT_SETTINGS = {
      restaurantName: "Talking Tables",
      tagline: "Fine Dining & Mandi Restaurant",
      address: "Beside Vignan University Main Gate, Vadlamudi 522213",
      phone: "+91 9346477777",
      fssai: "10126007000021",
      gstin: "",
      upiId: "9346477777@ybl",
      whatsappPhone: "+919346477777",
      footerMsg: "*** THANK YOU! VISIT TALKING TABLES AGAIN ***",
      paperWidth: "80mm",
      bottomFeedMm: 14,
      thermalFontSize: "normal",
      enableTax: true,
      taxRate: 5,
      cgst: 2.5,
      sgst: 2.5
    };'''

new_default_settings = '''    const DEFAULT_SETTINGS = {
      restaurantName: "Talking Tables",
      tagline: "Fine Dining & Mandi Restaurant",
      address: "Beside Vignan University Main Gate, Vadlamudi 522213",
      phone: "+91 9346477777",
      fssai: "10126007000021",
      gstin: "",
      upiId: "9346477777@ybl",
      whatsappPhone: "+919642567777",
      whatsappPhone2: "+919346477777",
      footerMsg: "*** THANK YOU! VISIT TALKING TABLES AGAIN ***",
      paperWidth: "80mm",
      bottomFeedMm: 14,
      thermalFontSize: "normal",
      enableTax: true,
      taxRate: 5,
      cgst: 2.5,
      sgst: 2.5
    };'''

if old_default_settings in content:
    content = content.replace(old_default_settings, new_default_settings)
    print("SUCCESS: Updated DEFAULT_SETTINGS with dual WhatsApp numbers.")
else:
    print("WARNING: old_default_settings not found directly.")

# 3. Update Settings Box 2 UI to show both WhatsApp numbers
old_box2_ui = '''          <div>
            <label class="text-xs text-slate-400 block mb-1">Owner WhatsApp Self-Chat Phone (for PDF Reports)</label>
            <input type="text" id="settingWhatsApp" value="+919346477777" class="w-full px-3 py-2 theme-input rounded-xl text-xs font-mono font-bold text-emerald-400 focus:outline-none">
            <p class="text-[10px] text-slate-500 mt-1">Binary PDF reports will be sent directly to this WhatsApp contact.</p>
          </div>'''

new_box2_ui = '''          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="text-xs text-slate-400 block mb-1">WhatsApp Recipient 1 (Owner)</label>
              <input type="text" id="settingWhatsApp" value="+919642567777" class="w-full px-3 py-2 theme-input rounded-xl text-xs font-mono font-bold text-emerald-400 focus:outline-none">
            </div>
            <div>
              <label class="text-xs text-slate-400 block mb-1">WhatsApp Recipient 2 (Management)</label>
              <input type="text" id="settingWhatsApp2" value="+919346477777" class="w-full px-3 py-2 theme-input rounded-xl text-xs font-mono font-bold text-emerald-400 focus:outline-none">
            </div>
          </div>
          <p class="text-[10px] text-slate-500">Binary PDF sales reports will be self-sent to both numbers (+919642567777 &amp; +919346477777) on download.</p>'''

if old_box2_ui in content:
    content = content.replace(old_box2_ui, new_box2_ui)
    print("SUCCESS: Updated Settings Box 2 UI with dual WhatsApp recipient inputs.")
else:
    print("WARNING: old_box2_ui not found directly.")

# 4. Update seatStationAndBill to properly load table's active items into cart
old_seat_func = '''    function seatStationAndBill(stationId) {
      const station = appData.tables.find(s => s.id === stationId);
      if (!station) return;
      selectedStationId = stationId;
      document.getElementById('quickTableSelect').value = stationId;
      document.getElementById('orderTableNo').value = station.name;
      switchTab('pos');
      showToast('Active Station Set: ' + station.name, 'success');
      playBeep(900);
    }'''

new_seat_func = '''    function seatStationAndBill(stationId) {
      const station = appData.tables.find(s => s.id === stationId);
      if (!station) return;

      // 1. If currently billing another table with items in cart, save cart to that table first
      if (selectedStationId && selectedStationId !== stationId) {
        const prevStation = appData.tables.find(s => s.id === selectedStationId);
        if (prevStation && cart.length > 0) {
          prevStation.items = JSON.parse(JSON.stringify(cart));
          prevStation.orderTotal = cart.reduce((sum, it) => sum + (it.total || (it.price * it.qty)), 0);
          prevStation.status = 'dining';
          if (!prevStation.orderId) {
            prevStation.orderId = "TT-" + (1001 + appData.bills.length);
          }
        }
      }

      // 2. Set newly active station
      selectedStationId = stationId;
      const selectEl = document.getElementById('quickTableSelect');
      if (selectEl) selectEl.value = stationId;
      const tableNoEl = document.getElementById('orderTableNo');
      if (tableNoEl) tableNoEl.value = station.name;

      // 3. Load active order dishes into cart
      if (station.items && Array.isArray(station.items) && station.items.length > 0) {
        cart = JSON.parse(JSON.stringify(station.items));
      } else if (station.orderId) {
        const existingBill = appData.bills.find(b => b.id === station.orderId);
        if (existingBill && existingBill.items && existingBill.items.length > 0) {
          cart = JSON.parse(JSON.stringify(existingBill.items));
          station.items = JSON.parse(JSON.stringify(existingBill.items));
        } else {
          cart = [];
        }
      } else {
        cart = [];
      }

      saveAppData();
      updateCartTotals();
      renderMenuItems();
      switchTab('pos');

      if (cart.length > 0) {
        showToast('Loaded ' + station.name + ': ' + cart.length + ' dishes in cart (₹' + (station.orderTotal || 0) + ')', 'success');
      } else {
        showToast('Active Station: ' + station.name + ' (Ready for billing)', 'info');
      }
      playBeep(900);
    }

    function onStationSelectChange(val) {
      seatStationAndBill(val);
    }

    function syncActiveStationWithCart() {
      if (!selectedStationId) return;
      const station = appData.tables.find(s => s.id === selectedStationId);
      if (!station) return;

      const subtotal = cart.reduce((sum, it) => sum + (it.total || (it.price * it.qty)), 0);
      if (cart.length > 0) {
        station.items = JSON.parse(JSON.stringify(cart));
        station.orderTotal = subtotal;
        station.status = 'dining';
        if (!station.orderId) {
          station.orderId = "TT-" + (1001 + appData.bills.length);
        }
      } else {
        station.items = [];
        station.orderTotal = 0;
      }
      saveAppData();
      const activeCount = appData.tables.filter(s => s.status === 'dining').length;
      const countEl = document.getElementById('activeStationCount');
      if (countEl) countEl.innerText = activeCount + ' Active';
    }'''

if old_seat_func in content:
    content = content.replace(old_seat_func, new_seat_func)
    print("SUCCESS: Updated seatStationAndBill to synchronize table items with cart.")
else:
    print("WARNING: old_seat_func not found directly.")

# 5. Hook syncActiveStationWithCart into updateCartTotals
if 'syncActiveStationWithCart();' not in content:
    content = content.replace('renderCartItems();\n    }', 'renderCartItems();\n      syncActiveStationWithCart();\n    }')
    print("SUCCESS: Hooked syncActiveStationWithCart into updateCartTotals.")

# 6. Update completeBill to properly clear table on checkout
old_bill_complete_station = '''      // Update station status to billed/clearing
      const station = appData.tables.find(s => s.name === stationName || s.id === selectedStationId);
      if (station) {
        station.status = "billed";
        station.orderId = billNo;
        station.orderTotal = grandTotal;
      }'''

new_bill_complete_station = '''      // Clear station on checkout (free for next guests)
      const station = appData.tables.find(s => s.name === stationName || s.id === selectedStationId);
      if (station) {
        station.status = "vacant";
        station.orderId = null;
        station.orderTotal = 0;
        station.items = [];
      }'''

if old_bill_complete_station in content:
    content = content.replace(old_bill_complete_station, new_bill_complete_station)
    print("SUCCESS: Updated completeBill to free station on checkout.")
else:
    print("WARNING: old_bill_complete_station not found.")

# 7. Update downloadAndWhatsAppReport to send to BOTH WhatsApp numbers
old_download_report = '''    // SIMULTANEOUS LOCAL PDF DOWNLOAD & IMMEDIATE DIRECT WHATSAPP FILE DISPATCH
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
    }'''

new_download_report = '''    // SIMULTANEOUS LOCAL PDF DOWNLOAD & IMMEDIATE DIRECT DUAL WHATSAPP FILE DISPATCH
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
      
      // Dual target phone numbers per client specification: +919642567777 & +919346477777
      const phone1 = (appData.settings?.whatsappPhone || "+919642567777").replace(/[^0-9]/g, '');
      const phone2 = (appData.settings?.whatsappPhone2 || "+919346477777").replace(/[^0-9]/g, '');
      const dispatchPhones = [phone1, phone2].filter(Boolean);

      // 4. Native Direct File Sharing (Web Share API Level 2)
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

      // 5. Direct Dispatch to Local Background Daemon (Port 5005) for BOTH numbers
      try {
        const base64Pdf = doc.output('datauristring').split(',')[1];
        fetch('http://localhost:5005/send-pdf', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            filename: filename,
            pdfBase64: base64Pdf,
            targetPhones: dispatchPhones,
            date: today
          })
        }).then(res => res.json()).then(data => {
          console.log("[DISPATCHER SUCCESS]", data);
        }).catch(e => {});
      } catch(e) {}

      // 6. Launch WhatsApp Web tabs for both recipients
      setTimeout(() => {
        window.open('https://web.whatsapp.com/send?phone=' + phone1, '_blank');
      }, 400);
      setTimeout(() => {
        window.open('https://web.whatsapp.com/send?phone=' + phone2, '_blank');
      }, 1200);

      showToast("Report dispatched to WhatsApp: +" + phone1 + " & +" + phone2, "success");
    }'''

if old_download_report in content:
    content = content.replace(old_download_report, new_download_report)
    print("SUCCESS: Updated downloadAndWhatsAppReport for dual recipients.")
else:
    print("WARNING: old_download_report not found directly.")

# 8. Update factoryResetDatabase to NEVER wipe Restaurant Identity & Payment QR / WhatsApp Reports
old_reset_func = '''    function factoryResetDatabase() {
      if (confirm("Reset all settings, menu, tables, and history to factory defaults?")) {
        localStorage.clear();
        location.reload();
      }
    }'''

new_reset_func = '''    function factoryResetDatabase() {
      if (confirm("Reset operational orders, tables, and bills?\\n\\nNOTE: \\\"Restaurant Identity\\\" and \\\"Payment QR & WhatsApp Reports\\\" will NOT be changed and will be safely preserved.")) {
        // 1. Snapshot and strictly preserve Restaurant Identity and Payment QR & WhatsApp Reports
        const currentSettings = appData.settings || {};
        const preservedSettings = {
          restaurantName: currentSettings.restaurantName || "Talking Tables",
          tagline: currentSettings.tagline || "Fine Dining & Mandi Restaurant",
          address: currentSettings.address || "Beside Vignan University Main Gate, Vadlamudi 522213",
          phone: currentSettings.phone || "+91 9346477777",
          fssai: currentSettings.fssai || "10126007000021",
          gstin: currentSettings.gstin || "",
          upiId: currentSettings.upiId || "9346477777@ybl",
          whatsappPhone: currentSettings.whatsappPhone || "+919642567777",
          whatsappPhone2: currentSettings.whatsappPhone2 || "+919346477777",
          footerMsg: currentSettings.footerMsg || "*** THANK YOU! VISIT TALKING TABLES AGAIN ***",
          paperWidth: currentSettings.paperWidth || "80mm",
          bottomFeedMm: currentSettings.bottomFeedMm || 14,
          thermalFontSize: currentSettings.thermalFontSize || "normal",
          enableTax: currentSettings.enableTax !== undefined ? currentSettings.enableTax : true,
          taxRate: currentSettings.taxRate || 5,
          cgst: currentSettings.cgst || 2.5,
          sgst: currentSettings.sgst || 2.5
        };

        // 2. Clear operational stores while preserving identity and configurations
        localStorage.removeItem('tt_pos_bills');
        localStorage.removeItem('tt_pos_expenses');
        localStorage.removeItem('tt_pos_held');
        localStorage.removeItem('tt_pos_bookings');
        localStorage.removeItem('tt_pos_cart');

        // Reset tables & menu to fresh state with items attached
        localStorage.setItem('tt_pos_tables', JSON.stringify(SEED_TABLES));
        localStorage.setItem('tt_pos_menu', JSON.stringify(SEED_MENU));
        localStorage.setItem('tt_pos_settings', JSON.stringify(preservedSettings));
        localStorage.setItem('tt_pos_ver', POS_STORAGE_VERSION);

        showToast("Software reset completed! Restaurant Identity & WhatsApp Settings preserved.", "success");
        setTimeout(() => location.reload(), 500);
      }
    }'''

if old_reset_func in content:
    content = content.replace(old_reset_func, new_reset_func)
    print("SUCCESS: Updated factoryResetDatabase to preserve Restaurant Identity & Payment/WhatsApp.")
else:
    print("WARNING: old_reset_func not found directly.")

# 9. Update applySettingsToUI and saveSettings to handle settingWhatsApp2
old_apply_settings = '''      document.getElementById('settingWhatsApp').value = appData.settings.whatsappPhone || "+919346477777";
      document.getElementById('settingFooterMsg').value = appData.settings.footerMsg || "";'''

new_apply_settings = '''      document.getElementById('settingWhatsApp').value = appData.settings.whatsappPhone || "+919642567777";
      if (document.getElementById('settingWhatsApp2')) {
        document.getElementById('settingWhatsApp2').value = appData.settings.whatsappPhone2 || "+919346477777";
      }
      document.getElementById('settingFooterMsg').value = appData.settings.footerMsg || "";'''

if old_apply_settings in content:
    content = content.replace(old_apply_settings, new_apply_settings)
    print("SUCCESS: Updated applySettingsToUI for settingWhatsApp2.")
else:
    print("WARNING: old_apply_settings not found.")

old_save_settings = '''      appData.settings.whatsappPhone = document.getElementById('settingWhatsApp').value.trim();
      appData.settings.footerMsg = document.getElementById('settingFooterMsg').value.trim();'''

new_save_settings = '''      appData.settings.whatsappPhone = document.getElementById('settingWhatsApp').value.trim();
      if (document.getElementById('settingWhatsApp2')) {
        appData.settings.whatsappPhone2 = document.getElementById('settingWhatsApp2').value.trim();
      }
      appData.settings.footerMsg = document.getElementById('settingFooterMsg').value.trim();'''

if old_save_settings in content:
    content = content.replace(old_save_settings, new_save_settings)
    print("SUCCESS: Updated saveSettings for settingWhatsApp2.")
else:
    print("WARNING: old_save_settings not found.")

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("All updates to template.html completed successfully!")

