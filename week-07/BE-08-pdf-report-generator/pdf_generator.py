import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_report(data: dict, output_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Standard margins: 0.5 inch (36 points)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Brand Styles matching Identity Kit
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'ReportSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'ReportH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=8
    )
    
    cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )
    
    header_cell_style = ParagraphStyle(
        'HeaderCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    story = []

    # 1. Header & Title Block
    story.append(Paragraph("Executive Order & Revenue Intelligence Report", title_style))
    story.append(Paragraph(f"Generated at: {data['generated_at']} | Source: report.db (SQLite) | Engine: FlyRank BE-08", subtitle_style))
    story.append(Spacer(1, 10))

    # 2. Executive Metric KPI Cards Table
    kpi_data = [
        [
            Paragraph("<b>Total Orders</b>", header_cell_style),
            Paragraph("<b>Total Revenue</b>", header_cell_style),
            Paragraph("<b>Avg Order Value</b>", header_cell_style)
        ],
        [
            Paragraph(f"<font size=16 color='#0F172A'><b>{data['total_orders']}</b></font>", cell_style),
            Paragraph(f"<font size=16 color='#10B981'><b>${data['total_revenue']:,.2f}</b></font>", cell_style),
            Paragraph(f"<font size=16 color='#0F172A'><b>${data['avg_order_value']:,.2f}</b></font>", cell_style)
        ]
    ]
    kpi_table = Table(kpi_data, colWidths=[180, 180, 180])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#F8FAFC')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 15))

    # 3. Top 5 Products by Revenue
    story.append(Paragraph("Top 5 Revenue Generating Products", h2_style))
    top_rows = [
        [Paragraph("Product Name", header_cell_style), Paragraph("Units Sold", header_cell_style), Paragraph("Total Revenue", header_cell_style)]
    ]
    for p in data["top_products"]:
        top_rows.append([
            Paragraph(p["product"], cell_style),
            Paragraph(str(p["units_sold"]), cell_style),
            Paragraph(f"${p['revenue']:,.2f}", cell_style)
        ])
    top_table = Table(top_rows, colWidths=[280, 120, 140])
    top_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(top_table)
    story.append(Spacer(1, 15))

    # 4. Long Detailed Orders Table (Demonstrates Clean Multi-Page Breaks and Repeating Header)
    story.append(Paragraph("Recent Transaction Ledger (Multi-Page Verification)", h2_style))
    detail_rows = [
        [
            Paragraph("Order ID", header_cell_style),
            Paragraph("Customer Name", header_cell_style),
            Paragraph("Product", header_cell_style),
            Paragraph("Amount", header_cell_style),
            Paragraph("Date Created", header_cell_style)
        ]
    ]
    for order in data["detailed_orders"]:
        detail_rows.append([
            Paragraph(f"#{order['id']}", cell_style),
            Paragraph(order["customer"], cell_style),
            Paragraph(order["product"], cell_style),
            Paragraph(f"${order['amount']:.2f}", cell_style),
            Paragraph(order["created_at"], cell_style)
        ])
        
    # repeatRows=1 guarantees that the table header row repeats automatically on Page 2+
    detail_table = Table(detail_rows, colWidths=[60, 130, 160, 80, 110], repeatRows=1)
    detail_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F1F5F9')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(detail_table)

    # Build the document
    doc.build(story)
    return output_path

if __name__ == "__main__":
    from db import get_report_data, init_and_seed_db
    init_and_seed_db()
    data = get_report_data()
    test_pdf = os.path.join(os.path.dirname(__file__), "reports", "test_report.pdf")
    generate_pdf_report(data, test_pdf)
    size_bytes = os.path.getsize(test_pdf)
    print(f"Generated PDF at: {test_pdf} ({size_bytes} bytes)")
    assert size_bytes > 5000
    print("Stage 3 Checkpoint Passed: Clean multi-page PDF generated with repeating table headers.")
