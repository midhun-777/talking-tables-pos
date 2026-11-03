import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, NextPageTemplate, Image as RLImage
)
from reportlab.pdfgen import canvas
import pypdfium2 as pdfium

PAGE_WIDTH, PAGE_HEIGHT = A4 # 595.28 x 841.89

HEADER_IMG_PATH = r"C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\template_extracted\exact_template_header_a4.png"
COVER_KORAXA_LOGO = r"C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\template_extracted\koraxa_clean_logo.png"
TT_LOGO_TRANSPARENT = r"C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\template_extracted\talking_tables_logo_transparent.png"

class ExactMasterCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        
        # Pages 2 to 10 have the exact template running header & footer
        if self._pageNumber > 1:
            # --- 1. RUNNING HEADER ---
            header_h = 107.0
            header_y = PAGE_HEIGHT - header_h
            if os.path.exists(HEADER_IMG_PATH):
                self.drawImage(HEADER_IMG_PATH, 0, header_y, width=PAGE_WIDTH, height=header_h, preserveAspectRatio=False)

            # Draw the Client Restaurant Logo (Talking Tables) in the header
            if os.path.exists(TT_LOGO_TRANSPARENT):
                tt_w = 46.0
                tt_h = 29.0
                tt_x = 352.0
                tt_y = header_y + 40.0
                self.drawImage(TT_LOGO_TRANSPARENT, tt_x, tt_y, width=tt_w, height=tt_h, mask='auto', preserveAspectRatio=True)

            # --- 2. RUNNING FOOTER ---
            footer_line_y = 40.0
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(45.64, footer_line_y, PAGE_WIDTH - 45.64, footer_line_y)

            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(45.64, 27, "KORAXA TECHNOLOGIES | Enterprise Software & Next-Gen POS Engineering • info@koraxa.in • +91 9491957756 • www.koraxa.in")
            
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#0f172a"))
            self.drawRightString(PAGE_WIDTH - 45.64, 27, f"Page {self._pageNumber} of {page_count}")

        self.restoreState()

def build_signature_block(styles):
    """Standard 2-Column Signatory Block for Koraxa Technologies & Talking Tables (Zero mention of V. Phani)"""
    left_flow = [
        Paragraph("<b>FOR KORAXA TECHNOLOGIES:</b>", styles['SignTitle']),
        Spacer(1, 14),
        Paragraph("____________________________________________", styles['SignLine']),
        Paragraph("<b>Authorized Signatory</b>", styles['SignBodyBold']),
        Paragraph("<b>Name:</b> K. Midhun", styles['SignBody']),
        Paragraph("<b>Title:</b> Startup Owner, Principal Enterprise Architect &amp; Lead Developer", styles['SignBody']),
        Paragraph("<b>Date:</b> 2nd November 2026", styles['SignBody']),
        Paragraph("<font color='#0284c7'>[Corporate Seal &amp; Digital Verification Stamp]</font>", styles['SignStamp'])
    ]

    right_flow = [
        Paragraph("<b>ACCEPTED &amp; CONFIRMED BY TALKING TABLES:</b>", styles['SignTitle']),
        Spacer(1, 14),
        Paragraph("____________________________________________", styles['SignLine']),
        Paragraph("<b>Authorized Signatory</b>", styles['SignBodyBold']),
        Paragraph("<b>Name:</b> Authorized Signatory", styles['SignBody']),
        Paragraph("<b>Title:</b> Managing Director &amp; Proprietor, Talking Tables", styles['SignBody']),
        Paragraph("<b>Date:</b> 2nd November 2026", styles['SignBody']),
        Paragraph("<font color='#d97706'>[Authorized Company Seal / Stamp]</font>", styles['SignStamp'])
    ]

    sig_table = Table([[left_flow, right_flow]], colWidths=[248, 256])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    return sig_table

def build_pdf():
    pdf_path = r"C:\Users\HP\.gemini\antigravity\scratch\sadasiva-karthikeya-pos\Talking_Tables_Complete_Project_Documents_Bundle_Koraxa.pdf"
    
    # DocTemplate with two frames:
    # 1. Cover Frame (starts near top of page, no header): x=45.64, y=40, w=504, h=760
    # 2. Standard Frame (below running header of 107 pt): x=45.64, y=48, w=504, h=675
    doc = BaseDocTemplate(pdf_path, pagesize=A4)
    
    cover_frame = Frame(45.64, 38, 504, 765, id='F_Cover', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)
    std_frame = Frame(45.64, 46, 504, 678, id='F_Std', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)

    doc.addPageTemplates([
        PageTemplate(id='CoverPage', frames=[cover_frame]),
        PageTemplate(id='StandardPage', frames=[std_frame])
    ])

    styles = getSampleStyleSheet()

    c_navy = colors.HexColor("#0f172a")       # Slate 900
    c_cyan = colors.HexColor("#0284c7")       # Cyan 600
    c_border = colors.HexColor("#cbd5e1")     # Slate 300
    c_inner = colors.HexColor("#e2e8f0")      # Slate 200
    c_dark = colors.HexColor("#1e293b")       # Text Slate 800
    c_bg_light = colors.HexColor("#f8fafc")   # Slate 50
    c_bg_blue = colors.HexColor("#f0f9ff")    # Sky 50
    c_border_blue = colors.HexColor("#bae6fd")# Sky 200
    c_success = colors.HexColor("#059669")    # Emerald 600

    styles.add(ParagraphStyle(
        'MainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14.0,
        leading=18.0,
        textColor=c_navy,
        spaceBefore=0,
        spaceAfter=3.0
    ))
    styles.add(ParagraphStyle(
        'MainSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.0,
        leading=11.0,
        textColor=c_cyan,
        spaceAfter=8.0
    ))
    styles.add(ParagraphStyle(
        'SectionHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.0,
        leading=12.0,
        textColor=c_navy,
        spaceBefore=4.0,
        spaceAfter=3.0
    ))
    styles.add(ParagraphStyle(
        'BodyP',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=c_dark,
        spaceAfter=3.5
    ))
    styles.add(ParagraphStyle(
        'THead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.0,
        leading=9.0,
        textColor=colors.white
    ))
    styles.add(ParagraphStyle(
        'TCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=9.5,
        textColor=c_dark
    ))
    styles.add(ParagraphStyle(
        'TCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.0,
        leading=9.5,
        textColor=c_navy
    ))
    styles.add(ParagraphStyle(
        'TCellSuccess',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.0,
        leading=9.5,
        textColor=c_success
    ))
    styles.add(ParagraphStyle(
        'SignTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10.5,
        textColor=c_navy
    ))
    styles.add(ParagraphStyle(
        'SignLine',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.0,
        textColor=colors.HexColor("#94a3b8")
    ))
    styles.add(ParagraphStyle(
        'SignBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=9.5,
        textColor=c_dark
    ))
    styles.add(ParagraphStyle(
        'SignBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.0,
        leading=9.5,
        textColor=c_navy
    ))
    styles.add(ParagraphStyle(
        'SignStamp',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=6.5,
        leading=9.0,
        spaceBefore=2
    ))

    elements = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    # Dual Logo Header: Koraxa Technologies (Left) and Talking Tables (Right)
    logo_table_data = [
        [
            RLImage(COVER_KORAXA_LOGO, width=225, height=66),
            RLImage(TT_LOGO_TRANSPARENT, width=135, height=85)
        ]
    ]
    logo_table = Table(logo_table_data, colWidths=[270, 234])
    logo_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(logo_table)
    elements.append(Spacer(1, 14))

    # Dark Navy Engagement Suite Box
    hero_content = [
        [Paragraph("<font color='#38bdf8'><b>ENTERPRISE CLIENT ENGAGEMENT SUITE</b></font>", ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.HexColor("#38bdf8")))],
        [Spacer(1, 6)],
        [Paragraph("<b>COMPLETE PROJECT DOCUMENTS &amp;<br/>TEMPLATES BUNDLE</b>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=19, leading=24, textColor=colors.white))],
        [Spacer(1, 8)],
        [Paragraph("Engineering Proposal • Master Services Agreement • Statement of Work • Delivery Acceptance • SLA • Change Control • Tax Invoicing", ParagraphStyle('H3', fontName='Helvetica', fontSize=7.5, leading=11, textColor=colors.HexColor("#cbd5e1")))]
    ]
    hero_table = Table(hero_content, colWidths=[504])
    hero_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_navy),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
        ('TOPPADDING', (0,0), (-1,-1), 22),
        ('BOTTOMPADDING', (0,0), (-1,-1), 22),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))
    elements.append(hero_table)
    elements.append(Spacer(1, 12))

    # Metadata Grid (NO V. PHANI!)
    cover_meta = [
        [Paragraph("PROJECT CODE:", styles['TCellBold']), Paragraph("KTX-2026-POS-089 (TT-VAD-PRO)", styles['TCellBold'])],
        [Paragraph("PROJECT TITLE:", styles['TCellBold']), Paragraph("Talking Tables Enterprise Cloud POS, Mandi Management &amp; Multi-Period Accounting Platform", styles['TCell'])],
        [Paragraph("CLIENT NAME:", styles['TCellBold']), Paragraph("<b>Talking Tables Fine Dining &amp; Mandi Restaurant</b> (Beside Vignan University Main Gate, Vadlamudi, AP, India)", styles['TCell'])],
        [Paragraph("CLIENT EXECUTIVE:", styles['TCellBold']), Paragraph("<b>Managing Director &amp; Head of Retail Operations</b>, Talking Tables", styles['TCell'])],
        [Paragraph("SERVICE VENDOR:", styles['TCellBold']), Paragraph("<b>Koraxa Technologies</b> (Narasaraopet HQ, Palnadu District, AP)", styles['TCell'])],
        [Paragraph("VENDOR LEAD &amp; FOUNDER:", styles['TCellBold']), Paragraph("<b>K. Midhun</b>, Startup Owner, Principal Enterprise Architect &amp; Lead Developer", styles['TCellBold'])],
        [Paragraph("SECURITY CLASSIFICATION:", styles['TCellBold']), Paragraph("<font color='#0284c7'><b>CONFIDENTIAL / PROPRIETARY COMMERCIAL SUITE</b></font>", styles['TCellBold'])],
        [Paragraph("DATE OF COMPILATION:", styles['TCellBold']), Paragraph("2nd November 2026 (Version 2.0 Final Certified)", styles['TCell'])],
    ]
    cover_meta_table = Table(cover_meta, colWidths=[150, 354])
    cover_meta_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_inner),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (0,-1), c_bg_light),
    ]))
    elements.append(cover_meta_table)
    elements.append(Spacer(1, 10))

    # Manifesto Box
    manifesto_content = [
        [Paragraph("<b>THE KORAXA TECHNOLOGIES PRODUCT &amp; DELIVERY MANIFESTO</b>", ParagraphStyle('M0', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=c_cyan))],
        [Spacer(1, 2)],
        [Paragraph("<b>1. Ownership Over Renting:</b> Every client owns 100% of their IP, source code repositories, and deployment credentials.", styles['TCell'])],
        [Paragraph("<b>2. Offline-First Resilience:</b> Sub-second barcode/dish scanning and local SQLite caching guarantee store registers never stop during outages.", styles['TCell'])],
        [Paragraph("<b>3. Engineered Precision:</b> Clean 60 FPS interfaces, sub-0.38s scan latency, and zero recurring vendor software tax.", styles['TCell'])],
        [Paragraph("<b>4. Complete Governance:</b> Milestone billing, transparent SOW specifications, rigorous UAT sign-offs, and 99.99% uptime SLAs.", styles['TCell'])],
    ]
    manifesto_table = Table(manifesto_content, colWidths=[504])
    manifesto_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_blue),
        ('BOX', (0,0), (-1,-1), 0.5, c_border_blue),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(manifesto_table)

    # Transition to Standard Template for Pages 2 to 10
    elements.append(NextPageTemplate('StandardPage'))
    elements.append(PageBreak())

    # =========================================================================
    # PAGE 2: MASTER INDEX & EXECUTIVE OVERVIEW
    # =========================================================================
    elements.append(Paragraph("MASTER DOCUMENTATION INDEX &amp; EXECUTIVE OVERVIEW", styles['MainTitle']))
    elements.append(Paragraph("This unified master bundle contains all seven legally binding and technical documents governing the complete project lifecycle:", styles['BodyP']))
    elements.append(Spacer(1, 4))

    index_data = [
        [Paragraph("<b>Section</b>", styles['THead']), Paragraph("<b>Document Title &amp; Purpose</b>", styles['THead']), Paragraph("<b>Reference Code</b>", styles['THead']), Paragraph("<b>Lifecycle Phase</b>", styles['THead'])],
        [Paragraph("Section 1", styles['TCellBold']), Paragraph("<b>Project Estimation &amp; Commercial Quotation</b><br/>Detailed Work Breakdown Structure, module estimates, discounts, and payment milestones.", styles['TCell']), Paragraph("KTX-EST-2026-089", styles['TCellBold']), Paragraph("Pre-Project Proposal", styles['TCell'])],
        [Paragraph("Section 2", styles['TCellBold']), Paragraph("<b>Master Services Agreement (MSA)</b><br/>Legally binding master contract with 100% full source code and IP ownership covenant.", styles['TCell']), Paragraph("KTX-MSA-2026-CORP", styles['TCellBold']), Paragraph("Contractual Baseline", styles['TCell'])],
        [Paragraph("Section 3", styles['TCellBold']), Paragraph("<b>Statement of Work (SOW)</b><br/>Granular technical scope, hardware peripheral driver criteria, and acceptance definitions.", styles['TCell']), Paragraph("KTX-SOW-2026-089", styles['TCellBold']), Paragraph("Engineering Execution", styles['TCell'])],
        [Paragraph("Section 4", styles['TCellBold']), Paragraph("<b>Project Delivery &amp; Acceptance Certificate</b><br/>Deliverables audit checklist, UAT verification sign-off, and warranty activation.", styles['TCell']), Paragraph("KTX-DEL-2026-089", styles['TCellBold']), Paragraph("Handover &amp; Sign-Off", styles['TCell'])],
        [Paragraph("Section 5", styles['TCellBold']), Paragraph("<b>Service Level Agreement (SLA)</b><br/>99.99% cloud uptime guarantee, incident severity matrices, and disaster recovery.", styles['TCell']), Paragraph("KTX-SLA-2026-089", styles['TCellBold']), Paragraph("Post-Launch Maintenance", styles['TCell'])],
        [Paragraph("Section 6", styles['TCellBold']), Paragraph("<b>Change Request (CR) Order Form Template</b><br/>Formal scope variation protocol for schedule, architectural, and commercial adjustments.", styles['TCell']), Paragraph("KTX-CR-2026-001", styles['TCellBold']), Paragraph("Scope Management", styles['TCell'])],
        [Paragraph("Section 7", styles['TCellBold']), Paragraph("<b>Commercial GST Tax Invoice Template</b><br/>Statutory GST tax invoice compliant with Indian tax law (SAC 998314) and bank details.", styles['TCell']), Paragraph("KTX-INV-2026-089", styles['TCellBold']), Paragraph("Financial Settlement", styles['TCell'])],
    ]
    index_table = Table(index_data, colWidths=[65, 245, 95, 99])
    index_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_inner),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
    ]))
    for r in range(1, len(index_data)):
        if r % 2 == 0:
            index_table.setStyle(TableStyle([('BACKGROUND', (0,r), (-1,r), c_bg_light)]))
    elements.append(index_table)
    elements.append(Spacer(1, 10))

    gov_box = [
        [Paragraph("<b>LEGAL &amp; STATUTORY GOVERNANCE NOTE</b>", ParagraphStyle('GB0', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=c_cyan))],
        [Spacer(1, 2)],
        [Paragraph("<b>Document Governance Integrity:</b> Each document in this bundle can be executed independently or as part of this unified portfolio. All terms and covenants align with Indian Contract Act 1872, Information Technology Act 2000, and GST statutory norms. Designed and engineered by Startup Owner <b>K. Midhun</b> for <b>Talking Tables</b>.", styles['TCell'])]
    ]
    gov_table = Table(gov_box, colWidths=[504])
    gov_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    elements.append(gov_table)

    # =========================================================================
    # PAGE 3: SECTION 1 - PROJECT ESTIMATION & COMMERCIAL PROPOSAL
    # (Calibrated so ALL tables fit on Page 3, and signatures go to Page 4)
    # =========================================================================
    elements.append(PageBreak())

    elements.append(Paragraph("SECTION 1: PROJECT ESTIMATION &amp; COMMERCIAL PROPOSAL", styles['MainTitle']))
    elements.append(Paragraph("Reference: KTX-EST-2026-089 | Prepared For: Talking Tables Fine Dining &amp; Mandi Restaurant", styles['MainSubTitle']))

    elements.append(Paragraph("1.1 EXECUTIVE SUMMARY &amp; WORK BREAKDOWN STRUCTURE", styles['SectionHead']))
    elements.append(Paragraph("Talking Tables operates a premium dining and mandi facility beside Vignan University Main Gate, Vadlamudi, requiring sub-second order punch, zero-downtime offline transaction resilience, Epson TM-T82X APD6 thermal printing, and multi-period expense auditing. Engineered by Startup Owner &amp; Lead Architect <b>K. Midhun</b>.", styles['BodyP']))

    wbs_data = [
        [Paragraph("<b>Module / Sprint</b>", styles['THead']), Paragraph("<b>Technical Scope &amp; Deliverables</b>", styles['THead']), Paragraph("<b>Tech Stack</b>", styles['THead']), Paragraph("<b>Est. Timeline</b>", styles['THead']), Paragraph("<b>Investment (INR)</b>", styles['THead'])],
        [Paragraph("M1: Core Offline POS Engine", styles['TCellBold']), Paragraph("Sub-second dish lookup, local SQLite schema, cart queue, clean bill engine without checkboxes, continuous IDs (TT-001..134), offline cash reconciliation.", styles['TCell']), Paragraph("HTML5 / Tailwind / JS / SQLite", styles['TCell']), Paragraph("Week 1 - 2", styles['TCell']), Paragraph("INR 85,000.00", styles['TCellBold'])],
        [Paragraph("M2: Hardware Peripheral Drivers", styles['TCellBold']), Paragraph("Epson TM-T82X APD6 thermal receipt socket pool (66mm safe zone, 203 DPI, 528 dots), 1-bit monochrome logo bitmap, 14mm auto-cutter feed buffer.", styles['TCell']), Paragraph("Web Print API / APD6 / ESC/POS", styles['TCell']), Paragraph("Week 2 - 3", styles['TCell']), Paragraph("INR 40,000.00", styles['TCellBold'])],
        [Paragraph("M3: Seating &amp; Mandi Cabin Mesh", styles['TCellBold']), Paragraph("Floor layout matrix: Hall (4 tables + 6 mandi cabins), Container 1 (6 cabins), Container 2 (6 cabins). Real-time cabin occupancy status and dine-in allocation.", styles['TCell']), Paragraph("IndexedDB / LocalStore / DOM", styles['TCell']), Paragraph("Week 3 - 4", styles['TCell']), Paragraph("INR 75,000.00", styles['TCellBold'])],
        [Paragraph("M4: Multi-Period Expenses &amp; PnL", styles['TCellBold']), Paragraph("Automated Daily, Monthly, and Yearly operational expenses auditing (Meat, Groceries, Salaries, Gas, Utilities) with date-range financial summaries.", styles['TCell']), Paragraph("JSON Engine / PnL Matrix", styles['TCell']), Paragraph("Week 4 - 5", styles['TCell']), Paragraph("INR 34,999.00", styles['TCellBold'])],
        [Paragraph("M5: Dynamic UPI QR &amp; WhatsApp", styles['TCellBold']), Paragraph("Dynamic amount-encoded UPI QR code directly on thermal bill (exact amount), simultaneous local PDF download and instant WhatsApp dispatch (+91 9346477777).", styles['TCell']), Paragraph("QRCode.js / WhatsApp API / jsPDF", styles['TCell']), Paragraph("Week 5 - 6", styles['TCell']), Paragraph("INR 50,000.00", styles['TCellBold'])],
        [Paragraph("M6: Security, UAT &amp; Deploy", styles['TCellBold']), Paragraph("Role-Based Access Control, supervisor audit logs, UAT sign-off, on-premise hardware calibration for Epson TM-T82X, zero-cutoff sign-off.", styles['TCell']), Paragraph("Browser Sandbox / CI/CD", styles['TCell']), Paragraph("Week 6", styles['TCell']), Paragraph("INR 40,000.00", styles['TCellBold'])],
    ]
    wbs_table = Table(wbs_data, colWidths=[90, 195, 85, 54, 80])
    wbs_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_inner),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    for r in range(1, len(wbs_data)):
        if r % 2 == 0:
            wbs_table.setStyle(TableStyle([('BACKGROUND', (0,r), (-1,r), c_bg_light)]))
    elements.append(wbs_table)
    elements.append(Spacer(1, 4))

    elements.append(Paragraph("1.2 COMMERCIAL PROPOSAL &amp; MILESTONE SCHEDULE", styles['SectionHead']))
    
    comm_data = [
        [Paragraph("<b>Commercial Line Item</b>", styles['THead']), Paragraph("<b>Details &amp; Terms</b>", styles['THead']), Paragraph("<b>Amount (INR)</b>", styles['THead'])],
        [Paragraph("Gross Engineering Estimate", styles['TCellBold']), Paragraph("Full-scope modules M1 through M6 including hardware peripheral calibration", styles['TCell']), Paragraph("INR 3,24,999.00", styles['TCellBold'])],
        [Paragraph("Multi-Store Promotional Incentive", styles['TCellBold']), Paragraph("Special grant code: RETAILPRO15 (15% enterprise expansion discount)", styles['TCell']), Paragraph("-INR 48,750.00", styles['TCellBold'])],
        [Paragraph("Net Taxable Project Value", styles['TCellBold']), Paragraph("Base engineering fee for 6-week turnkey delivery and 100% IP code transfer", styles['TCell']), Paragraph("INR 2,76,249.00", styles['TCellBold'])],
        [Paragraph("Goods &amp; Services Tax (GST 18%)", styles['TCellBold']), Paragraph("SAC Code: 998314 (Information Technology Software Services) - CGST 9% + SGST 9%", styles['TCell']), Paragraph("INR 49,724.82", styles['TCellBold'])],
        [Paragraph("<b>TOTAL INVESTMENT (INCL. GST)</b>", ParagraphStyle('WH1', fontName='Helvetica-Bold', fontSize=7.0, leading=9, textColor=colors.white)), Paragraph("<b>Complete turnkey solution, hardware drivers, and 100% full IP ownership</b>", ParagraphStyle('WH2', fontName='Helvetica-Bold', fontSize=7.0, leading=9, textColor=colors.white)), Paragraph("<b>INR 3,25,973.82</b>", ParagraphStyle('WH3', fontName='Helvetica-Bold', fontSize=7.0, leading=9, textColor=colors.white))],
    ]
    comm_table = Table(comm_data, colWidths=[150, 244, 110])
    comm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BACKGROUND', (0,-1), (-1,-1), c_cyan),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_inner),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(comm_table)
    elements.append(Spacer(1, 3))

    mile_data = [
        [Paragraph("<b>Milestone Stage</b>", styles['THead']), Paragraph("<b>Trigger / Verification Deliverable</b>", styles['THead']), Paragraph("<b>% Share</b>", styles['THead']), Paragraph("<b>Milestone Amount (INR)</b>", styles['THead'])],
        [Paragraph("M1: Project Inception", styles['TCellBold']), Paragraph("Agreement execution, architecture blueprint, initial repo setup &amp; DB schema", styles['TCell']), Paragraph("30%", styles['TCell']), Paragraph("INR 97,792.15", styles['TCellBold'])],
        [Paragraph("M2: Core POS &amp; Hardware Alpha", styles['TCellBold']), Paragraph("Working offline checkout UI, Epson TM-T82X APD6 80mm driver calibration", styles['TCell']), Paragraph("30%", styles['TCell']), Paragraph("INR 97,792.15", styles['TCellBold'])],
        [Paragraph("M3: Multi-Period Sync &amp; Beta", styles['TCellBold']), Paragraph("Multi-period expenses engine, dynamic UPI QR generator, WhatsApp dispatch", styles['TCell']), Paragraph("20%", styles['TCell']), Paragraph("INR 65,194.76", styles['TCellBold'])],
        [Paragraph("M4: Production Go-Live &amp; Sign-off", styles['TCellBold']), Paragraph("Live store counter deployment, staff training, full IP repository handoff", styles['TCell']), Paragraph("20%", styles['TCell']), Paragraph("INR 65,194.76", styles['TCellBold'])],
    ]
    mile_table = Table(mile_data, colWidths=[120, 230, 44, 110])
    mile_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_inner),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    for r in range(1, len(mile_data)):
        if r % 2 == 0:
            mile_table.setStyle(TableStyle([('BACKGROUND', (0,r), (-1,r), c_bg_light)]))
    elements.append(mile_table)

    # =========================================================================
    # PAGE 4: COMMERCIAL ACCEPTANCE & AUTHORIZATION SIGN-OFF
    # =========================================================================
    elements.append(PageBreak())

    elements.append(Paragraph("COMMERCIAL ACCEPTANCE &amp; AUTHORIZATION SIGN-OFF", styles['MainTitle']))
    elements.append(Paragraph("Reference: KTX-EST-2026-089-SIGN | Formal Commercial Execution", styles['MainSubTitle']))

    auth_box = [
        [Paragraph("<b>FORMAL COMMERCIAL EXECUTION COVENANT</b>", ParagraphStyle('AC0', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=c_cyan))],
        [Spacer(1, 3)],
        [Paragraph("By affixing signatures below, both <b>Koraxa Technologies</b> and <b>Talking Tables Fine Dining &amp; Mandi Restaurant</b> formally agree to the Commercial Quotation, Milestone Schedule, and technical deliverables detailed in Section 1 (KTX-EST-2026-089). All deliverables shall be governed by the Master Services Agreement (MSA) and executed under the direct supervision of Startup Owner &amp; Lead Architect <b>K. Midhun</b>.", styles['TCell'])],
        [Spacer(1, 3)],
        [Paragraph("<b>Turnkey Engineering Scope:</b> Offline POS Terminal, Epson TM-T82X APD6 80mm Hardware Drivers, Mandi Seating Layout, Multi-Period Expense Reporting Engine, Dynamic Amount-Encoded UPI Payment QR Code, and Full Source Code Transfer upon Milestone M4 settlement.", styles['TCell'])]
    ]
    auth_table = Table(auth_box, colWidths=[504])
    auth_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    elements.append(auth_table)
    elements.append(Spacer(1, 24))

    # Signatures
    elements.append(build_signature_block(styles))
    elements.append(Spacer(1, 30))

    bot_note = [
        [Paragraph("<b>STATUTORY CONTRACT COMPLIANCE:</b> This execution page forms an indivisible component of Proposal KTX-EST-2026-089. Conforms with Section 10 of the Indian Contract Act 1872 and Information Technology Act 2000 digital signature norms. Issued at Narasaraopet HQ, Palnadu District, AP.", ParagraphStyle('BN', fontName='Helvetica', fontSize=7.0, leading=9.5, textColor=colors.HexColor("#64748b")))]
    ]
    bot_table = Table(bot_note, colWidths=[504])
    bot_table.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(bot_table)

    # =========================================================================
    # PAGE 5: SECTION 2 - MASTER SERVICES AGREEMENT (MSA)
    # =========================================================================
    elements.append(PageBreak())

    elements.append(Paragraph("SECTION 2: MASTER SERVICES AGREEMENT (MSA)", styles['MainTitle']))
    elements.append(Paragraph("Reference: KTX-MSA-2026-CORP | Legally Binding Master Framework", styles['MainSubTitle']))

    covenant_content = [
        [Paragraph("<b>100% FULL SOURCE CODE &amp; IP OWNERSHIP COVENANT</b>", ParagraphStyle('COV0', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=c_cyan))],
        [Spacer(1, 2)],
        [Paragraph("<b>Section 4 - Unconditional Intellectual Property Transfer:</b> Service Provider covenants and agrees that upon receipt of complete milestone payments stipulated in the associated SOW, Client shall be the sole and exclusive owner of all rights, title, and interest in and to all custom deliverables, source code, database schemas, API connectors, UI/UX designs, and documentation. No recurring vendor tax or seat license fees shall ever be levied. Architected by Startup Owner <b>K. Midhun</b>.", styles['TCell'])]
    ]
    cov_table = Table(covenant_content, colWidths=[504])
    cov_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_blue),
        ('BOX', (0,0), (-1,-1), 0.5, c_border_blue),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(cov_table)
    elements.append(Spacer(1, 5))

    msa_clauses = [
        "<b>1. SCOPE OF SERVICES &amp; SOW HIERARCHY</b><br/>Service Provider renders custom software engineering services under individual SOWs governed by this Master Agreement.",
        "<b>2. PERFORMANCE STANDARDS</b><br/>All deliverables conform to enterprise software engineering standards, undergoing automated testing and security audits.",
        "<b>3. COMMERCIAL TERMS &amp; INVOICING</b><br/>Milestone payments in INR due within 15 days of valid GST tax invoice. Late payments accrue interest at 1.5% per month.",
        "<b>4. INTELLECTUAL PROPERTY &amp; TRANSFER</b><br/>All custom code created for Client constitutes work-for-hire. 100% full source code ownership transferred on final settlement.",
        "<b>5. CONFIDENTIALITY &amp; NON-DISCLOSURE</b><br/>Both Parties strictly safeguard all proprietary technical and commercial information for five (5) years.",
        "<b>6. DATA PROTECTION &amp; PRIVACY</b><br/>Zero-trust security controls, TLS encryption, and client exclusivity over all customer transactional databases.",
        "<b>7. 30-DAY DEFECT LIABILITY WARRANTY</b><br/>Service Provider provides 30 calendar days of zero-cost bug-fixing warranty commencing on delivery sign-off.",
        "<b>8. LIMITATION OF LIABILITY</b><br/>Neither party liable for consequential damages. Aggregate liability capped at total fees paid under the relevant SOW.",
        "<b>9. TERM AND TERMINATION</b><br/>Agreement remains active until terminated with 30 days notice or immediately for uncured material breach.",
        "<b>10. GOVERNING LAW &amp; ARBITRATION</b><br/>Governed by laws of India. Arbitration seated at Narasaraopet, Palnadu District, Andhra Pradesh."
    ]

    for clause in msa_clauses:
        elements.append(Paragraph(clause, styles['BodyP']))
        elements.append(Spacer(1, 0.5))

    elements.append(Spacer(1, 5))
    elements.append(build_signature_block(styles))

    # =========================================================================
    # PAGE 6: SECTION 3 - STATEMENT OF WORK (SOW)
    # =========================================================================
    elements.append(PageBreak())

    elements.append(Paragraph("SECTION 3: STATEMENT OF WORK (SOW)", styles['MainTitle']))
    elements.append(Paragraph("Reference: KTX-SOW-2026-089 | Technical Scope &amp; Architecture Specification", styles['MainSubTitle']))

    elements.append(Paragraph("3.1 SYSTEM DELIVERABLES &amp; TECHNICAL SPECIFICATIONS", styles['SectionHead']))
    
    sow_data = [
        [Paragraph("<b>Feature Component</b>", styles['THead']), Paragraph("<b>Functional &amp; Technical Specification</b>", styles['THead']), Paragraph("<b>Acceptance Criteria (DoD)</b>", styles['THead'])],
        [Paragraph("Offline POS Terminal UI", styles['TCellBold']), Paragraph("High-speed item lookup (&lt;400ms), dual search bars (catalog &amp; cart), fast cart operations, clean bill net total without checkboxes, customer mobile/name capture.", styles['TCell']), Paragraph("Sub-second checkout flow tested with 134 authentic menu dishes. Zero lag on cart transactions.", styles['TCell'])],
        [Paragraph("Hardware Peripherals", styles['TCellBold']), Paragraph("Epson TM-T82X APD6 80mm thermal receipt calibration (66mm printable safe zone, 528 dots @ 203 DPI), pure 1-bit solid monochrome logo bitmap, 14mm cut buffer.", styles['TCell']), Paragraph("Receipt prints with zero right margin cutoff. Logo prints pitch black with high thermal transfer.", styles['TCell'])],
        [Paragraph("Dynamic UPI QR &amp; WhatsApp", styles['TCellBold']), Paragraph("Direct client-side QR generator encoding exact bill amount into standard UPI URL, simultaneous local PDF generation and instant WhatsApp dispatch.", styles['TCell']), Paragraph("Instant camera scanning across GPay, PhonePe, Paytm, CRED. Immediate WhatsApp trigger to +91 9346477777.", styles['TCell'])],
        [Paragraph("Multi-Period Expenses Engine", styles['TCellBold']), Paragraph("Granular expense recording across Meat, Groceries, Salaries, LPG Gas, and Utilities. Auto-aggregates Daily, Monthly, and Yearly operational costs.", styles['TCell']), Paragraph("Accurate multi-period PnL computation filterable across Today, Month, and Full Year 2026.", styles['TCell'])],
        [Paragraph("Floor &amp; Cabin Station Hub", styles['TCellBold']), Paragraph("Seating matrix: Hall (4 tables + 6 mandi cabins), Container 1 (6 mandi cabins), Container 2 (6 mandi cabins). Real-time occupied/vacant states.", styles['TCell']), Paragraph("Accurate visual cabin allocation and real-time station occupancy monitoring.", styles['TCell'])],
    ]
    sow_table = Table(sow_data, colWidths=[110, 234, 160])
    sow_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_inner),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    for r in range(1, len(sow_data)):
        if r % 2 == 0:
            sow_table.setStyle(TableStyle([('BACKGROUND', (0,r), (-1,r), c_bg_light)]))
    elements.append(sow_table)
    elements.append(Spacer(1, 5))

    bound_box = [
        [Paragraph("<b>EXPLICIT BOUNDARIES &amp; SCOPE CONTAINMENT</b>", ParagraphStyle('EB0', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=c_navy))],
        [Spacer(1, 2)],
        [Paragraph("<b>Explicit Out-of-Scope Items:</b> (a) Supply of physical hardware terminals, monitors, or barcode scanners; (b) Internet service provider (ISP) line troubleshooting; (c) Custom reverse-engineering of unsupported proprietary legacy accounting tools. Designed by Startup Owner &amp; Architect <b>K. Midhun</b>.", styles['TCell'])]
    ]
    bound_table = Table(bound_box, colWidths=[504])
    bound_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(bound_table)
    elements.append(Spacer(1, 6))
    elements.append(build_signature_block(styles))

    # =========================================================================
    # PAGE 7: SECTION 4 - PROJECT DELIVERY & ACCEPTANCE CERTIFICATE
    # =========================================================================
    elements.append(PageBreak())

    elements.append(Paragraph("SECTION 4: PROJECT DELIVERY &amp; ACCEPTANCE CERTIFICATE", styles['MainTitle']))
    elements.append(Paragraph("Reference: KTX-DEL-2026-089 | Final UAT &amp; Handover Sign-off", styles['MainSubTitle']))

    del_data = [
        [Paragraph("<b>Deliverable Category</b>", styles['THead']), Paragraph("<b>Asset Description &amp; Specific Handoff Method</b>", styles['THead']), Paragraph("<b>Verification Status</b>", styles['THead'])],
        [Paragraph("Source Code Repositories", styles['TCellBold']), Paragraph("Full repository transfer including production index.html, template.html, compiled assets, standalone offline runner, and entire git commit history.", styles['TCell']), Paragraph("100% TRANSFERRED", styles['TCellSuccess'])],
        [Paragraph("Cloud Infrastructure &amp; IAM", styles['TCellBold']), Paragraph("Zero-dependency local execution credentials, offline database caching, and verified local browser runtime handoff to restaurant owner.", styles['TCell']), Paragraph("CREDENTIALS TRANSFERRED", styles['TCellSuccess'])],
        [Paragraph("Database &amp; Menu Catalog", styles['TCellBold']), Paragraph("Full 134 authentic dishes initialized with continuous sequential IDs (TT-001 through TT-134), seating station schema, and dynamic auto-sequencer (TT-135+).", styles['TCell']), Paragraph("INITIALIZED &amp; VERIFIED", styles['TCellSuccess'])],
        [Paragraph("Peripheral Hardware Drivers", styles['TCellBold']), Paragraph("Epson TM-T82X APD6 thermal printer driver calibrated on Windows 11 (66mm printable safe zone, 528 dots @ 203 DPI, zero cutoff, 14mm feed buffer).", styles['TCell']), Paragraph("ON-SITE CALIBRATED", styles['TCellSuccess'])],
        [Paragraph("Accounting &amp; QR Bridge", styles['TCellBold']), Paragraph("Dynamic amount-encoded UPI payment QR synthesizer, Clean Bill engine without payment checkboxes, dual local PDF and WhatsApp report dispatcher.", styles['TCell']), Paragraph("SYNC RECONCILED", styles['TCellSuccess'])],
        [Paragraph("Staff Training &amp; Documentation", styles['TCellBold']), Paragraph("Cashier counter training, operational runbook, menu management guide, multi-period expense logging SOPs delivered by Architect <b>K. Midhun</b>.", styles['TCell']), Paragraph("TRAINING CERTIFIED", styles['TCellSuccess'])],
    ]
    del_table = Table(del_data, colWidths=[120, 264, 120])
    del_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_inner),
        ('TOPPADDING', (0,0), (-1,-1), 3.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.0),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    for r in range(1, len(del_data)):
        if r % 2 == 0:
            del_table.setStyle(TableStyle([('BACKGROUND', (0,r), (-1,r), c_bg_light)]))
    elements.append(del_table)
    elements.append(Spacer(1, 5))

    uat_box = [
        [Paragraph("<b>UAT VERIFICATION &amp; SIGN-OFF METRICS</b>", ParagraphStyle('UAT0', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=c_navy))],
        [Spacer(1, 2)],
        [Paragraph("<b>User Acceptance Testing (UAT) Verification:</b> Total test cases executed: <b>148</b> | Total Passed: <b>148</b> | Total Failed: <b>0</b>.<br/>• Severity 1 (Critical / Blocker): <b>0 Open</b> | Severity 2 (Major Defect): <b>0 Open</b> | Severity 3 (Minor UI): <b>0 Open</b>.<br/>30-Day Defect Liability Warranty active from 31-Oct-2026 to 30-Nov-2026. Certified by Startup Owner <b>K. Midhun</b>.", styles['TCell'])]
    ]
    uat_table = Table(uat_box, colWidths=[504])
    uat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(uat_table)
    elements.append(Spacer(1, 6))
    elements.append(build_signature_block(styles))

    # =========================================================================
    # PAGE 8: SECTION 5 - SERVICE LEVEL AGREEMENT (SLA)
    # =========================================================================
    elements.append(PageBreak())

    elements.append(Paragraph("SECTION 5: SERVICE LEVEL AGREEMENT (SLA)", styles['MainTitle']))
    elements.append(Paragraph("Reference: KTX-SLA-2026-089 | Maintenance &amp; Support Agreement", styles['MainSubTitle']))

    uptime_box = [
        [Paragraph("<b>99.99% ENTERPRISE UPTIME GUARANTEE</b>", ParagraphStyle('UP0', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=c_cyan))],
        [Spacer(1, 2)],
        [Paragraph("<b>Monthly Uptime Commitment:</b> Service Provider guarantees 99.99% operational availability for offline store billing registers. Local store counters operate 100% uninterrupted in offline-first mode during network disruptions with zero downtime.", styles['TCell'])]
    ]
    uptime_table = Table(uptime_box, colWidths=[504])
    uptime_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_blue),
        ('BOX', (0,0), (-1,-1), 0.5, c_border_blue),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(uptime_table)
    elements.append(Spacer(1, 5))

    sla_data = [
        [Paragraph("<b>Severity Level</b>", styles['THead']), Paragraph("<b>Impact Definition &amp; Examples</b>", styles['THead']), Paragraph("<b>Initial Response SLA</b>", styles['THead']), Paragraph("<b>Workaround / Fix Target</b>", styles['THead'])],
        [Paragraph("Priority 1 (Critical)", styles['TCellBold']), Paragraph("Complete billing counter halt; inability to process thermal receipts or dynamic UPI payments; corruption of transaction ledger.", styles['TCell']), Paragraph("<font color='#dc2626'><b>&lt; 15 Minutes</b></font>", styles['TCellBold']), Paragraph("<b>&lt; 2 Hours</b>", styles['TCellBold'])],
        [Paragraph("Priority 2 (Major)", styles['TCellBold']), Paragraph("Single terminal glitch (other registers operational); WhatsApp dispatch delayed; thermal print feed lag; degraded dish search speed.", styles['TCell']), Paragraph("<font color='#d97706'><b>&lt; 1 Hour</b></font>", styles['TCellBold']), Paragraph("<b>&lt; 6 Hours</b>", styles['TCellBold'])],
        [Paragraph("Priority 3 (Minor)", styles['TCellBold']), Paragraph("Cosmetic dashboard UI inquiries; expense categorization formatting adjustment; general non-urgent configuration questions.", styles['TCell']), Paragraph("<font color='#059669'><b>&lt; 4 Hours</b></font>", styles['TCellBold']), Paragraph("<b>&lt; 24 Hours</b>", styles['TCellBold'])],
    ]
    sla_table = Table(sla_data, colWidths=[110, 214, 90, 90])
    sla_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_inner),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    for r in range(1, len(sla_data)):
        if r % 2 == 0:
            sla_table.setStyle(TableStyle([('BACKGROUND', (0,r), (-1,r), c_bg_light)]))
    elements.append(sla_table)
    elements.append(Spacer(1, 5))

    backup_box = [
        [Paragraph("<b>5.2 BACKUP POLICY, DISASTER RECOVERY &amp; CONTACT HOTLINES</b>", ParagraphStyle('BP0', fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=c_navy))],
        [Spacer(1, 2)],
        [Paragraph("• <b>Backups &amp; RPO/RTO:</b> Local daily encrypted JSON exports, RPO &lt; 1 Hour, RTO &lt; 15 Minutes.<br/>• <b>Dedicated Hotline:</b> +91 9491957756 (24/7 WhatsApp emergency channel) | Email: support@koraxa.in.<br/>• <b>Lead Architect Hotline:</b> <b>K. Midhun</b> (Direct escalation channel for Talking Tables).<br/>• <b>On-Premise Dispatch:</b> 2-hour rapid on-site dispatch window for Vadlamudi &amp; Guntur district.<br/>• <b>Commercial Retainer:</b> INR 1,49,999 / year (Includes 20% commitment discount).", styles['TCell'])]
    ]
    backup_table = Table(backup_box, colWidths=[504])
    backup_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(backup_table)
    elements.append(Spacer(1, 6))
    elements.append(build_signature_block(styles))

    # =========================================================================
    # PAGE 9: SECTION 6 - CHANGE REQUEST (CR) ORDER FORM TEMPLATE
    # =========================================================================
    elements.append(PageBreak())

    elements.append(Paragraph("SECTION 6: CHANGE REQUEST (CR) ORDER FORM TEMPLATE", styles['MainTitle']))
    elements.append(Paragraph("Reference: KTX-CR-2026-001 | Scope Variation Management", styles['MainSubTitle']))

    cr_meta_data = [
        [Paragraph("Change Request Ref:", styles['TCellBold']), Paragraph("<b>KTX-CR-2026-001</b>", styles['TCellBold']), Paragraph("Date Proposed:", styles['TCellBold']), Paragraph("31-Oct-2026", styles['TCell'])],
        [Paragraph("Originator / Requestor:", styles['TCellBold']), Paragraph("<b>Managing Director</b> (Talking Tables)", styles['TCell']), Paragraph("Priority Level:", styles['TCellBold']), Paragraph("<font color='#0284c7'><b>HIGH / EXPEDITED</b></font>", styles['TCellBold'])],
        [Paragraph("Change Title:", styles['TCellBold']), Paragraph("<b>Automated Dynamic WhatsApp PDF Invoice Dispatch, Dynamic Amount-Encoded UPI QR &amp; Clean Bill Thermal Integration</b>", styles['TCell']), Paragraph("Project Ref:", styles['TCellBold']), Paragraph("KTX-2026-POS-089", styles['TCell'])],
    ]
    cr_meta_table = Table(cr_meta_data, colWidths=[100, 192, 80, 132])
    cr_meta_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_inner),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,0), (0,-1), c_bg_light),
        ('BACKGROUND', (2,0), (2,-1), c_bg_light),
    ]))
    elements.append(cr_meta_table)
    elements.append(Spacer(1, 5))

    elements.append(Paragraph("6.1 SCOPE MODIFICATION &amp; IMPACT SUMMARY", styles['SectionHead']))
    elements.append(Paragraph("Client requested dynamic WhatsApp PDF delivery directly to +91 9346477777, dynamic amount-encoded UPI QR code directly on thermal receipts, complete purge of payment mode checkboxes (Clean Bill), and continuous dish ID indexing. Technical architecture engineered by Startup Owner <b>K. Midhun</b>.", styles['BodyP']))
    elements.append(Spacer(1, 3))

    cr_data = [
        [Paragraph("<b>Resource / Engineering Component</b>", styles['THead']), Paragraph("<b>Estimated Effort</b>", styles['THead']), Paragraph("<b>Cost Adjustment (INR)</b>", styles['THead'])],
        [Paragraph("WhatsApp Cloud API Integration &amp; Webhook Security", styles['TCellBold']), Paragraph("16 Man-Hours", styles['TCell']), Paragraph("INR 14,000.00", styles['TCellBold'])],
        [Paragraph("Dynamic PDF Vector Invoice Renderer Template", styles['TCellBold']), Paragraph("12 Man-Hours", styles['TCell']), Paragraph("INR 10,500.00", styles['TCellBold'])],
        [Paragraph("POS UI Clean Bill Toggle &amp; Dynamic Amount UPI QR", styles['TCellBold']), Paragraph("8 Man-Hours", styles['TCell']), Paragraph("INR 7,000.00", styles['TCellBold'])],
        [Paragraph("TOTAL ADDITIONAL INVESTMENT (EXCL. GST)", styles['TCellBold']), Paragraph("<b>36 Man-Hours</b>", styles['TCellBold']), Paragraph("<b>INR 31,500.00</b>", styles['TCellBold'])],
        [Paragraph("GST @ 18% (SAC 998314)", styles['TCellBold']), Paragraph("Statutory Applicable Tax", styles['TCell']), Paragraph("INR 5,670.00", styles['TCellBold'])],
        [Paragraph("<b>NET CHANGE ORDER VALUE (INCL. GST)</b>", ParagraphStyle('WCR1', fontName='Helvetica-Bold', fontSize=7.0, leading=9, textColor=colors.white)), Paragraph("<b>Additional 3 Working Days to Timeline</b>", ParagraphStyle('WCR2', fontName='Helvetica-Bold', fontSize=7.0, leading=9, textColor=colors.white)), Paragraph("<b>INR 37,170.00</b>", ParagraphStyle('WCR3', fontName='Helvetica-Bold', fontSize=7.0, leading=9, textColor=colors.white))],
    ]
    cr_table = Table(cr_data, colWidths=[240, 154, 110])
    cr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BACKGROUND', (0,-1), (-1,-1), c_cyan),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_inner),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    for r in range(1, len(cr_data) - 1):
        if r % 2 == 0:
            cr_table.setStyle(TableStyle([('BACKGROUND', (0,r), (-1,r), c_bg_light)]))
    elements.append(cr_table)
    elements.append(Spacer(1, 8))
    elements.append(build_signature_block(styles))

    # =========================================================================
    # PAGE 10: SECTION 7 - COMMERCIAL TAX INVOICE TEMPLATE
    # =========================================================================
    elements.append(PageBreak())

    elements.append(Paragraph("SECTION 7: COMMERCIAL TAX INVOICE TEMPLATE", styles['MainTitle']))
    elements.append(Paragraph("Reference: KTX-INV-2026-089 | Statutory GST Compliance (SAC 998314)", styles['MainSubTitle']))

    # Client Box with Talking Tables Logo!
    tt_logo_inv = RLImage(TT_LOGO_TRANSPARENT, width=65, height=41) if os.path.exists(TT_LOGO_TRANSPARENT) else Paragraph("", styles['TCell'])

    client_cell_content = [
        [
            Paragraph("<b>BILLED TO (CLIENT DETAILS):</b><br/>"
                      "<b>TALKING TABLES FINE DINING &amp; MANDI</b><br/>"
                      "Beside Vignan University Main Gate, Vadlamudi<br/>"
                      "Guntur District, Andhra Pradesh - 522213, India<br/>"
                      "<b>GSTIN:</b> Unregistered / Retail Hospitality<br/>"
                      "<b>Contact:</b> Managing Director, Talking Tables<br/>"
                      "<b>Tel:</b> +91 9346477777<br/>"
                      "Place of Supply: Andhra Pradesh (State Code: 37)", styles['TCell']),
            tt_logo_inv
        ]
    ]
    client_cell_table = Table(client_cell_content, colWidths=[180, 70])
    client_cell_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    inv_party_data = [
        [
            Paragraph("<b>SERVICE PROVIDER (ISSUED BY):</b><br/>"
                      "<b>KORAXA TECHNOLOGIES</b><br/>"
                      "Registered Office: Narasaraopet, Palnadu District<br/>"
                      "Andhra Pradesh - 522601, India<br/>"
                      "<b>GSTIN:</b> 37AAHCK9491B1Z2<br/>"
                      "<b>PAN:</b> AAHCK9491B<br/>"
                      "<b>Email:</b> billing@koraxa.in | <b>Tel:</b> +91 9491957756<br/>"
                      "<b>Founder &amp; Architect:</b> K. Midhun<br/>"
                      "State: Andhra Pradesh (State Code: 37)", styles['TCell']),
            client_cell_table
        ]
    ]
    inv_party_table = Table(inv_party_data, colWidths=[250, 254])
    inv_party_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    elements.append(inv_party_table)
    elements.append(Spacer(1, 4))

    inv_line_data = [
        [Paragraph("<b>#</b>", styles['THead']), Paragraph("<b>Description of Service / Milestone</b>", styles['THead']), Paragraph("<b>HSN/SAC</b>", styles['THead']), Paragraph("<b>Qty</b>", styles['THead']), Paragraph("<b>Rate (INR)</b>", styles['THead']), Paragraph("<b>Taxable Amt (INR)</b>", styles['THead'])],
        [Paragraph("1", styles['TCellBold']), Paragraph("<b>Milestone 1: Project Inception &amp; Architecture Blueprint</b><br/>Local SQLite schema, WBS definitions, git repository initialization.", styles['TCell']), Paragraph("998314", styles['TCell']), Paragraph("1", styles['TCell']), Paragraph("INR 82,874.70", styles['TCell']), Paragraph("INR 82,874.70", styles['TCellBold'])],
        [Paragraph("2", styles['TCellBold']), Paragraph("<b>Milestone 2: Offline POS Engine &amp; Hardware Calibration</b><br/>Epson TM-T82X APD6 thermal printer drivers (66mm safe zone), 1-bit logo bitmap.", styles['TCell']), Paragraph("998314", styles['TCell']), Paragraph("1", styles['TCell']), Paragraph("INR 82,874.70", styles['TCell']), Paragraph("INR 82,874.70", styles['TCellBold'])],
        [Paragraph("3", styles['TCellBold']), Paragraph("<b>Milestone 3: Seating Mesh, PnL &amp; Dynamic UPI QR Bridge</b><br/>Mandi cabin matrix, daily/monthly/yearly expenses, amount-encoded QR.", styles['TCell']), Paragraph("998314", styles['TCell']), Paragraph("1", styles['TCell']), Paragraph("INR 55,249.80", styles['TCell']), Paragraph("INR 55,249.80", styles['TCellBold'])],
        [Paragraph("4", styles['TCellBold']), Paragraph("<b>Milestone 4: Final UAT, Production Deployment &amp; IP Transfer</b><br/>100% full IP source code ownership transfer, cashier staff training.", styles['TCell']), Paragraph("998314", styles['TCell']), Paragraph("1", styles['TCell']), Paragraph("INR 55,249.80", styles['TCell']), Paragraph("INR 55,249.80", styles['TCellBold'])],
    ]
    inv_line_table = Table(inv_line_data, colWidths=[20, 230, 44, 20, 95, 95])
    inv_line_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_inner),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    for r in range(1, len(inv_line_data)):
        if r % 2 == 0:
            inv_line_table.setStyle(TableStyle([('BACKGROUND', (0,r), (-1,r), c_bg_light)]))
    elements.append(inv_line_table)
    elements.append(Spacer(1, 3))

    # Bank Details & Summary
    bank_and_total_data = [
        [
            Paragraph("<b>AMOUNT IN WORDS:</b><br/>Three Lakh Twenty-Five Thousand Nine Hundred Seventy-Four Rupees Only<br/><br/>"
                      "<b>BANK REMITTANCE DETAILS (NEFT / RTGS / IMPS):</b><br/>"
                      "• Account Name: <b>KORAXA TECHNOLOGIES</b><br/>"
                      "• Bank Name: <b>HDFC Bank Ltd.</b><br/>"
                      "• Account Number: <b>50200084919577</b> (Current Account)<br/>"
                      "• IFSC Code: <b>HDFC0001844</b><br/>"
                      "• Branch: Narasaraopet Branch, Palnadu District, AP<br/>"
                      "• UPI ID: <b>koraxa@hdfcbank</b>", styles['TCell']),
            Table([
                [Paragraph("Subtotal (Taxable):", styles['TCellBold']), Paragraph("INR 2,76,249.00", styles['TCellBold'])],
                [Paragraph("CGST (9.0%):", styles['TCell']), Paragraph("INR 24,862.41", styles['TCell'])],
                [Paragraph("SGST (9.0%):", styles['TCell']), Paragraph("INR 24,862.41", styles['TCell'])],
                [Paragraph("IGST (0.0%):", styles['TCell']), Paragraph("INR 0.00", styles['TCell'])],
                [Paragraph("<b>TOTAL PAYABLE:</b>", ParagraphStyle('WT1', fontName='Helvetica-Bold', fontSize=7.0, leading=9, textColor=colors.white)), Paragraph("<b>INR 3,25,973.82</b>", ParagraphStyle('WT2', fontName='Helvetica-Bold', fontSize=7.0, leading=9, textColor=colors.white))],
            ], colWidths=[110, 104], style=[
                ('BOX', (0,0), (-1,-1), 0.5, c_border),
                ('INNERGRID', (0,0), (-1,-1), 0.5, c_inner),
                ('BACKGROUND', (0,-1), (-1,-1), c_cyan),
                ('TOPPADDING', (0,0), (-1,-1), 2),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ])
        ]
    ]
    bank_total_table = Table(bank_and_total_data, colWidths=[280, 224])
    bank_total_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    elements.append(bank_total_table)
    elements.append(Spacer(1, 3))

    invoice_foot = [
        [
            Paragraph("<b>TERMS &amp; CONDITIONS:</b><br/>"
                      "1. Payment due within 15 calendar days from the date of invoice.<br/>"
                      "2. Please quote invoice reference KTX-INV-2026-089 in remittance advice.<br/>"
                      "3. Full intellectual property source code transfer executed upon full settlement.<br/>"
                      "4. Subject to Narasaraopet jurisdiction.", styles['TCell']),
            Paragraph("<b>FOR KORAXA TECHNOLOGIES:</b><br/><br/>"
                      "________________________________________<br/>"
                      "<b>Authorized Signatory:</b> K. Midhun<br/>"
                      "<font size='6.0' color='#64748b'>Startup Owner, Principal Enterprise Architect &amp; Lead Developer<br/>"
                      "[Electronically Generated Tax Invoice]</font>", styles['TCell'])
        ]
    ]
    invoice_foot_table = Table(invoice_foot, colWidths=[300, 204])
    invoice_foot_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    elements.append(invoice_foot_table)

    # Build document
    doc.build(elements, canvasmaker=ExactMasterCanvas)
    print("Talking_Tables_Complete_Project_Documents_Bundle_Koraxa.pdf successfully rebuilt!")

if __name__ == '__main__':
    build_pdf()
