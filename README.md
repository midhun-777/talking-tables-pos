# Talking Tables - Restaurant POS & Daily Expense Ledger System
> **Engineered by KORAXA TECHNOLOGIES**
>
> **Client:** Talking Tables Restaurant  
> **Location:** Beside Vignan University Main Gate, Vadlamudi, AP – 522213  
> **Contact:** +91 9346477777

---

## 🎯 Specific Requirements Implemented

1. **POS Terminal with Customized Menu**:
   - Touch/keyboard billing terminal with rapid dish search, live cart, and categories (Biryani, Starters, Curries, Rotis, Beverages).
2. **KOT Completely Suppressed**:
   - Zero Kitchen Order Tickets (KOT) generated; orders finalize directly to customer receipts to eliminate campus lunch-rush bottleneck.
3. **Clean Customer Bill (No Payment Breakdown)**:
   - **No UPI, CASH, or CARD options printed on the main bill**.
   - Standard 80mm thermal receipt with Bill No, Date & Time, Item Details, Rates, and Grand Total.
4. **Interactive Dashboard**:
   - Real-time Gross Sales, Total Orders, Daily Expenses, and Net Operating Margin (`Sales - Expenses`).
5. **Bill History**:
   - Searchable archive of past invoices with one-click thermal re-print.
6. **Daily Expenses Management**:
   - Integrated expense tracking: **Meat & Poultry, Groceries & Vegetables, Staff Salaries & Wages, Gas & Fuel, Maintenance**.
7. **Direct PDF File Download & WhatsApp Send (NOT TEXT)**:
   - Generates an official, branded **Talking Tables Daily Audit Report PDF**.
   - Downloads the `.pdf` file directly to the local billing PC.
   - **Directly sends the actual binary `.pdf` document file** (not plain text) to the owner's WhatsApp self-chat (`+91 9346477777`) via:
     - **Web Share API Document Passing** (attaches the `.pdf` file natively to WhatsApp on Windows/Mobile), and
     - **Local Automated WhatsApp Dispatcher Daemon** (`whatsapp_pdf_service.js`).
8. **Settings & Menu Manager**:
   - Edit restaurant details, WhatsApp dispatch number, and dynamic dish pricing.

---

## 🚀 How to Run the Software Demo

1. Open File Explorer to:
   ```
   C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\
   ```
2. Double-click **`index.html`** to launch it in your browser.
3. To test the direct WhatsApp background dispatcher:
   ```powershell
   node whatsapp_pdf_service.js
   ```

---

## 📄 Official PDF Documents

- **Technical Architecture Specification:**  
  [Talking_Tables_Architecture_Specification.pdf](file:///C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/Talking_Tables_Architecture_Specification.pdf)
- **Client Requirements Specification (SRS):**  
  [Talking_Tables_Requirements_Specification.pdf](file:///C:/Users/HP/.gemini/antigravity/scratch/sadasiva-karthikeya-pos/Talking_Tables_Requirements_Specification.pdf)
