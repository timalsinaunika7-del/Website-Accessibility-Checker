
import os
import html
from datetime import datetime

from accessibility_checker import fetch_webpage, analyze_accessibility


def display_report(results):
    """
    Displays the accessibility report in the terminal.
    """

    total_issues = 0

    print("\n" + "=" * 55)
    print("       WEBSITE ACCESSIBILITY REPORT")
    print("=" * 55)

    for category, issues in results.items():
        print(f"\n{category}:")

        if issues:
            for issue in issues:
                print(f"  [!] {issue}")
                total_issues += 1
        else:
            print("  [OK] No issues found.")

    print("\n" + "-" * 55)
    print(f"Total accessibility issues found: {total_issues}")
    print("-" * 55)


def generate_html_report(url, results):
    """
    Generates an HTML accessibility report.
    """

    total_issues = sum(len(issues) for issues in results.values())
    total_checks = len(results)
    passed_checks = total_checks - sum(
        1 for issues in results.values() if issues
    )

    report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    report_sections = ""

    for category, issues in results.items():
        safe_category = html.escape(category)

        if issues:
            status = "Issues Found"
            status_class = "warning"

            issue_items = "".join(
                f"<li>{html.escape(issue)}</li>"
                for issue in issues
            )

            details = f"<ul>{issue_items}</ul>"

        else:
            status = "Passed"
            status_class = "success"
            details = "<p>No potential issues detected.</p>"

        report_sections += f"""
        <section class="result-card">
            <div class="section-heading">
                <h2>{safe_category}</h2>
                <span class="{status_class}">{status}</span>
            </div>
            {details}
        </section>
        """

    safe_url = html.escape(url, quote=True)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Website Accessibility Report</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f9;
                color: #222;
                margin: 0;
                padding: 30px;
            }}

            .container {{
                max-width: 900px;
                margin: auto;
            }}

            header {{
                background-color: #263b55;
                color: white;
                padding: 25px;
                border-radius: 10px;
                margin-bottom: 25px;
            }}

            header h1 {{
                margin-top: 0;
            }}

            .summary {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
                margin-bottom: 25px;
            }}

            .summary-card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }}

            .summary-card h2 {{
                font-size: 30px;
                margin: 5px;
            }}

            .result-card {{
                background: white;
                padding: 20px;
                margin-bottom: 15px;
                border-radius: 10px;
                border-left: 5px solid #ccc;
            }}

            .section-heading {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 10px;
            }}

            .success {{
                color: #16803c;
                font-weight: bold;
            }}

            .warning {{
                color: #b45309;
                font-weight: bold;
            }}

            footer {{
                margin-top: 30px;
                color: #666;
                font-size: 13px;
                text-align: center;
            }}

            @media (max-width: 600px) {{
                body {{
                    padding: 15px;
                }}

                .summary {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>

    <body>
        <main class="container">

            <header>
                <h1>Website Accessibility Report</h1>
                <p><strong>Website:</strong> {safe_url}</p>
                <p><strong>Generated:</strong> {report_date}</p>
            </header>

            <div class="summary">

                <div class="summary-card">
                    <h2>{total_checks}</h2>
                    <p>Total Checks</p>
                </div>

                <div class="summary-card">
                    <h2>{passed_checks}</h2>
                    <p>Passed Checks</p>
                </div>

                <div class="summary-card">
                    <h2>{total_issues}</h2>
                    <p>Potential Issues</p>
                </div>

            </div>

            <h2>Detailed Results</h2>

            {report_sections}

            <footer>
                <p>
                    Generated by Website Accessibility Checker.
                    Automated results are preliminary and do not
                    establish full WCAG compliance.
                </p>
            </footer>

        </main>
    </body>
    </html>
    """

    # Create the reports folder if it does not exist.
    os.makedirs("reports", exist_ok=True)

    report_path = os.path.join(
        "reports",
        "accessibility_report.html"
    )

    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(html_content)

    print("\nHTML report successfully generated!")
    print(f"Report location: {os.path.abspath(report_path)}")


def main():
    print("\nWelcome to Website Accessibility Checker!")

    url = input("\nEnter a website URL: ").strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print("\nChecking website... Please wait.")

    webpage_html = fetch_webpage(url)

    if webpage_html is None:
        print("Could not analyze the website.")
        return

    results = analyze_accessibility(webpage_html)

    # Display results in the terminal.
    display_report(results)

    # Generate the HTML report.
    generate_html_report(url, results)


if __name__ == "__main__":
    main()
