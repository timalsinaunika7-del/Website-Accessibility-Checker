# Website Accessibility Checker

A Python-based tool that analyzes website HTML for potential accessibility issues and generates an HTML accessibility report.

## Features

- Checks images for missing and generic alternative text.
- Checks whether webpages have a title.
- Checks for a main H1 heading.
- Identifies links that may lack accessible text.
- Checks for an HTML language declaration.
- Checks form controls for accessible labels.
- Displays results in the terminal.
- Generates a browser-viewable HTML report.
- Includes 19 automated unit tests using Python `unittest`.

## Technologies Used

- Python
- Requests
- BeautifulSoup
- HTML
- CSS
- unittest

## Project Structure

```text
Website-Accessibility-Checker/
├── tests/
│   └── test_accessibility.py
├── accessibility_checker.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

1. Clone this repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

2. Navigate to the project directory:

```bash
cd Website-Accessibility-Checker
```

3. Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

Enter a website URL when prompted.

The program displays accessibility findings in the terminal and generates an HTML report inside the `reports` folder.

## Running Tests

Run the automated test suite:

```bash
python -m unittest discover -s tests -v
```

## Limitations

This tool performs preliminary automated checks on downloaded HTML. It does not provide a complete WCAG compliance assessment.

Some accessibility issues require browser-based testing, assistive technology, and human evaluation.

## Author

Unika Timalsina | Computer Science  Student | Python | Web Accessibility
