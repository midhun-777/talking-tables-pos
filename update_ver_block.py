with open('template.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_ver_block = '''    // Auto-upgrade storage to guarantee 134 authentic dishes and 22 seating stations
    const POS_STORAGE_VERSION = 'tt_pos_v2.5_table_cart_sync_dual_whatsapp';
    if (localStorage.getItem('tt_pos_ver') !== POS_STORAGE_VERSION) {
      localStorage.setItem('tt_pos_ver', POS_STORAGE_VERSION);
      localStorage.setItem('tt_pos_menu', JSON.stringify(SEED_MENU));
      localStorage.setItem('tt_pos_tables', JSON.stringify(SEED_TABLES));
      localStorage.setItem('tt_pos_settings', JSON.stringify(DEFAULT_SETTINGS));
      localStorage.setItem('tt_pos_expenses', JSON.stringify(SEED_EXPENSES));
      localStorage.setItem('tt_pos_bookings', JSON.stringify(SEED_BOOKINGS));
      localStorage.setItem('tt_pos_bills', JSON.stringify(SEED_BILLS));
    }'''

new_ver_block = '''    // Auto-upgrade storage to guarantee 134 authentic dishes and 22 seating stations with active items
    const POS_STORAGE_VERSION = 'tt_pos_v2.5_table_cart_sync_dual_whatsapp';
    if (localStorage.getItem('tt_pos_ver') !== POS_STORAGE_VERSION) {
      localStorage.setItem('tt_pos_ver', POS_STORAGE_VERSION);
      localStorage.setItem('tt_pos_menu', JSON.stringify(SEED_MENU));
      localStorage.setItem('tt_pos_tables', JSON.stringify(SEED_TABLES));
      const existingSettings = JSON.parse(localStorage.getItem('tt_pos_settings') || 'null');
      const mergedSettings = Object.assign({}, DEFAULT_SETTINGS, existingSettings || {});
      localStorage.setItem('tt_pos_settings', JSON.stringify(mergedSettings));
      if (!localStorage.getItem('tt_pos_expenses')) localStorage.setItem('tt_pos_expenses', JSON.stringify(SEED_EXPENSES));
      if (!localStorage.getItem('tt_pos_bills')) localStorage.setItem('tt_pos_bills', JSON.stringify(SEED_BILLS));
    }'''

if old_ver_block in text:
    text = text.replace(old_ver_block, new_ver_block)
    with open('template.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated version block with safe settings merge!")
else:
    print("WARNING: old_ver_block not matched directly.")

