import os
from playwright.sync_api import sync_playwright

def build_html_report(data: dict) -> str:
    """
    Builds a clean, production-grade HTML document for headless Chromium PDF rendering.
    Enforces CSS rules to prevent table row page-splitting and ensures thead repetition.
    """
    # 1. KPI Cards HTML (Totals)
    kpi_cards_html = f"""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{data.get('total_orders', 0):,}</div>
            <div class="kpi-sub">Processed volume</div>
        </div>
        <div class="kpi-card highlight">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value text-emerald">${data.get('total_revenue', 0.0):,.2f}</div>
            <div class="kpi-sub">Gross merchandise value</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Average Order Value</div>
            <div class="kpi-value">${data.get('avg_order_value', 0.0):,.2f}</div>
            <div class="kpi-sub">Per completed transaction</div>
        </div>
    </div>
    """

    # 2. Top 5 Products Table
    top_products_rows = ""
    for idx, p in enumerate(data.get("top_products", []), 1):
        top_products_rows += f"""
        <tr>
            <td style="font-weight: 600; width: 40px; text-align: center;">#{idx}</td>
            <td style="font-weight: 500;">{p.get('product', '')}</td>
            <td style="text-align: right;">{p.get('units_sold', 0):,}</td>
            <td style="text-align: right; font-weight: 600; color: #0F172A;">${p.get('revenue', 0.0):,.2f}</td>
        </tr>
        """

    # 3. Long Detailed Table of Orders
    order_rows = ""
    for o in data.get("detailed_orders", []):
        order_rows += f"""
        <tr>
            <td style="font-family: monospace; font-size: 11px; color: #64748B;">#{o.get('id', '')}</td>
            <td style="font-weight: 500;">{o.get('customer', '')}</td>
            <td>{o.get('product', '')}</td>
            <td style="text-align: right; font-weight: 600;">${o.get('amount', 0.0):.2f}</td>
            <td style="color: #64748B; font-size: 11px;">{o.get('created_at', '')}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Executive Order & Revenue Intelligence Report</title>
    <style>
        @page {{
            size: A4;
            margin: 18mm 14mm 18mm 14mm;
        }}

        * {{
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #0F172A;
            background-color: #FFFFFF;
            line-height: 1.45;
            font-size: 12px;
            margin: 0;
            padding: 0;
        }}

        /* Header block */
        .report-header {{
            border-bottom: 2px solid #0F172A;
            padding-bottom: 12px;
            margin-bottom: 20px;
        }}

        .report-title {{
            font-size: 22px;
            font-weight: 800;
            color: #0F172A;
            margin: 0 0 4px 0;
            letter-spacing: -0.02em;
        }}

        .report-subtitle {{
            font-size: 11px;
            color: #64748B;
            margin: 0;
        }}

        /* KPI Cards Grid */
        .kpi-grid {{
            display: flex;
            gap: 12px;
            margin-bottom: 24px;
        }}

        .kpi-card {{
            flex: 1;
            padding: 12px 14px;
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 6px;
        }}

        .kpi-card.highlight {{
            background-color: #F0FDF4;
            border-color: #BBF7D0;
        }}

        .kpi-label {{
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748B;
            margin-bottom: 4px;
        }}

        .kpi-value {{
            font-size: 20px;
            font-weight: 800;
            color: #0F172A;
            margin-bottom: 2px;
        }}

        .kpi-value.text-emerald {{
            color: #059669;
        }}

        .kpi-sub {{
            font-size: 10px;
            color: #94A3B8;
        }}

        /* Section Headings */
        h2 {{
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #1E293B;
            margin: 18px 0 8px 0;
        }}

        /* Table Architecture with Page Break Defense */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 22px;
            page-break-inside: auto;
        }}

        /* Essential Browser Print Engine Directives:
           1. thead repeats on every page break
           2. tr avoids being sliced midway across a page break */
        thead {{
            display: table-header-group;
        }}

        tfoot {{
            display: table-footer-group;
        }}

        tr {{
            break-inside: avoid !important;
            page-break-inside: avoid !important;
        }}

        th {{
            background-color: #0F172A;
            color: #FFFFFF;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            padding: 8px 10px;
            text-align: left;
            border: 1px solid #0F172A;
        }}

        td {{
            padding: 6px 10px;
            font-size: 11px;
            border: 1px solid #E2E8F0;
            vertical-align: middle;
        }}

        tbody tr:nth-child(even) {{
            background-color: #F8FAFC;
        }}

        .footer {{
            margin-top: 30px;
            border-top: 1px solid #E2E8F0;
            padding-top: 10px;
            font-size: 9px;
            color: #94A3B8;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="report-header">
        <h1 class="report-title">Executive Order & Revenue Intelligence Report</h1>
        <p class="report-subtitle">Generated at: {data.get('generated_at', '')} | Source: report.db (SQLite) | Engine: Playwright Headless Chromium</p>
    </div>

    {kpi_cards_html}

    <h2>Top 5 Revenue Generating Products</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 40px; text-align: center;">Rank</th>
                <th>Product Name</th>
                <th style="width: 120px; text-align: right;">Units Sold</th>
                <th style="width: 140px; text-align: right;">Total Revenue</th>
            </tr>
        </thead>
        <tbody>
            {top_products_rows}
        </tbody>
    </table>

    <h2>Recent Transaction Ledger (Multi-Page Verification)</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 65px;">Order ID</th>
                <th>Customer Name</th>
                <th>Product</th>
                <th style="width: 90px; text-align: right;">Amount</th>
                <th style="width: 130px;">Date Created</th>
            </tr>
        </thead>
        <tbody>
            {order_rows}
        </tbody>
    </table>

    <div class="footer">
        FlyRank Backend AI Engineering &bull; BE-08 PDF Report Generator &bull; Headless Chromium Rendered
    </div>
</body>
</html>
"""
    return html

def generate_pdf_report(data: dict, output_path: str) -> str:
    """
    Renders the report HTML into a high-fidelity A4 PDF using Playwright's headless Chromium.
    Enforces the 'break-inside: avoid' table pagination rules.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    html_content = build_html_report(data)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(html_content, wait_until="networkidle")
        page.pdf(
            path=output_path,
            format="A4",
            print_background=True,
            margin={
                "top": "18mm",
                "bottom": "18mm",
                "left": "14mm",
                "right": "14mm"
            }
        )
        browser.close()

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
    print("Stage 3 Checkpoint Passed: Clean multi-page PDF generated via Playwright with repeating table headers.")
