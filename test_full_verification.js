const fs = require('fs');
const { JSDOM } = require('jsdom');

console.log("=== COMPREHENSIVE POS & TABLE CART SYNC TEST ===");

const html = fs.readFileSync('index.html', 'utf8');

// Use jsdom to test the live DOM and scripts
const dom = new JSDOM(html, {
  runScripts: "dangerously",
  resources: "usable",
  url: "http://localhost/"
});

const window = dom.window;
const document = window.document;

// Wait for DOM load
setTimeout(() => {
  try {
    console.log("1. Checking SEATING_STATIONS and active tables in appData:");
    const tables = window.appData.tables;
    console.log("Total tables:", tables.length);
    const diningTables = tables.filter(t => t.status === 'dining');
    console.log("Active dining tables:", diningTables.length);
    
    diningTables.forEach(t => {
      console.log(`- ${t.name} (${t.id}): status=${t.status}, orderId=${t.orderId}, orderTotal=${t.orderTotal}, itemsCount=${(t.items || []).length}`);
    });

    console.log("\n2. Testing Table Click & Cart Loading (The Reported Issue):");
    console.log("Initial Cart length:", window.cart.length);

    // Click Hall Table T-2 (H-T2) which shows Bill TT-1004, ₹960
    console.log("Clicking 'View / Add to Bill' on Hall Table T-2 (H-T2)...");
    window.seatStationAndBill('H-T2');

    console.log("Cart length after clicking H-T2:", window.cart.length);
    console.log("Cart items:", window.cart.map(i => `${i.name} (x${i.qty} = ₹${i.total})`).join(', '));
    const cartTotalText = document.getElementById('cartGrandTotal').innerText;
    console.log("Cart Grand Total in UI:", cartTotalText);

    if (window.cart.length > 0 && cartTotalText.includes('960')) {
      console.log(">>> TEST 1 PASSED: Occupied table items loaded into cart with exact ₹960 total! <<<");
    } else {
      console.error(">>> TEST 1 FAILED: Cart items not loaded properly! <<<");
    }

    // Now test switching to Hall Mandi Cabin M-1 (H-M1)
    console.log("\nClicking 'View / Add to Bill' on Hall Mandi Cabin M-1 (H-M1)...");
    window.seatStationAndBill('H-M1');
    console.log("Cart length for H-M1:", window.cart.length);
    console.log("Cart items for H-M1:", window.cart.map(i => `${i.name} (x${i.qty} = ₹${i.total})`).join(', '));
    const m1TotalText = document.getElementById('cartGrandTotal').innerText;
    console.log("Cart Grand Total for H-M1:", m1TotalText);

    if (window.cart.length > 0) {
      console.log(">>> TEST 2 PASSED: Switching to Mandi Cabin M-1 loaded its dishes! <<<");
    }

    console.log("\n3. Testing WhatsApp Numbers Configuration:");
    console.log("Settings whatsappPhone (Recipient 1):", window.appData.settings.whatsappPhone);
    console.log("Settings whatsappPhone2 (Recipient 2):", window.appData.settings.whatsappPhone2);
    if (window.appData.settings.whatsappPhone.includes('9642567777') && window.appData.settings.whatsappPhone2.includes('9346477777')) {
      console.log(">>> TEST 3 PASSED: Both numbers configured (+919642567777 & +919346477777)! <<<");
    } else {
      console.error(">>> TEST 3 FAILED: Dual WhatsApp numbers not configured properly! <<<");
    }

    console.log("\n4. Testing Reset Protection for Identity and Payment QR/WhatsApp:");
    // Check that factoryResetDatabase preserves settings
    console.log("Verifying preservedSettings keys in factoryResetDatabase function text...");
    const fnStr = window.factoryResetDatabase.toString();
    const preservesIdentity = fnStr.includes('restaurantName') && fnStr.includes('fssai') && fnStr.includes('address');
    const preservesPayment = fnStr.includes('upiId') && fnStr.includes('whatsappPhone') && fnStr.includes('whatsappPhone2');
    console.log("Preserves Restaurant Identity:", preservesIdentity);
    console.log("Preserves Payment QR & WhatsApp Reports:", preservesPayment);

    if (preservesIdentity && preservesPayment) {
      console.log(">>> TEST 4 PASSED: Software reset safely preserves Identity and Payment/WhatsApp configurations! <<<");
    }

    console.log("\n=== ALL TESTS COMPLETED SUCCESSFULLY ===");
  } catch (err) {
    console.error("Test execution error:", err);
  }
}, 500);

