import config


def money(value):
    """Format a number as ₹1,23,456 (Indian grouping)."""
    value = int(round(value))
    sign = "-" if value < 0 else ""
    s = str(abs(value))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return f"{sign}{config.CURRENCY}{s}"


def build_report(summary):
    """Return formatted report text/HTML."""
    daily = summary["daily"]
    daily = daily[(daily["Income"] != 0) | (daily["Expense"] != 0)]

    # Daily rows
    daily_rows = ""
    for _, r in daily.iterrows():
        daily_rows += (
            "<tr>"
            f"<td>{r['Date']:%d-%b-%Y}</td>"
            f"<td style='text-align:right;color:#1a7f37'>{money(r['Income'])}</td>"
            f"<td style='text-align:right;color:#cf222e'>{money(r['Expense'])}</td>"
            f"<td style='text-align:right'><b>{money(r['Balance'])}</b></td>"
            "</tr>"
        )

    # Pending rows
    pending_rows = ""
    for _, r in summary["pending"].iterrows():
        pending_rows += (
            "<tr>"
            f"<td>{r['Date']:%d-%b}</td>"
            f"<td>{r['Type']}</td>"
            f"<td>{r['Description']}</td>"
            f"<td style='text-align:right'>{money(r['Amount'])}</td>"
            "</tr>"
        )

    html = f"""
       <html>
       <head><meta charset="utf-8"></head>
       <body style="font-family:Arial,sans-serif;font-size:14px">
         <h2>Income &amp; Expense Report</h2>

         <table cellpadding="6" style="border-collapse:collapse">
           <tr><td>Opening Balance</td><td style="text-align:right">{money(summary['opening_balance'])}</td></tr>
           <tr><td>Total Income</td><td style="text-align:right;color:#1a7f37">{money(summary['total_income'])}</td></tr>
           <tr><td>Total Expense</td><td style="text-align:right;color:#cf222e">{money(summary['total_expense'])}</td></tr>
           <tr style="border-top:2px solid #333"><td><b>Closing Balance</b></td>
               <td style="text-align:right"><b>{money(summary['closing_balance'])}</b></td></tr>
         </table>

         <h3>Daily Balance</h3>
         <table border="1" cellpadding="6" style="border-collapse:collapse;border-color:#ccc">
           <tr style="background:#f0f0f0"><th>Date</th><th>Income</th><th>Expense</th><th>Balance</th></tr>
           {daily_rows}
         </table>

         <h3>Pending / Upcoming (not in balance)</h3>
         <p>Income: {money(summary['pending_income'])} &nbsp;|&nbsp;
            Expense: {money(summary['pending_expense'])}</p>
         <table border="1" cellpadding="6" style="border-collapse:collapse;border-color:#ccc">
           <tr style="background:#f0f0f0"><th>Date</th><th>Type</th><th>Description</th><th>Amount</th></tr>
           {pending_rows}
         </table>
       </body></html>
       """
    return html
