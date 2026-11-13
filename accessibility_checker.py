
import requests
from bs4 import BeautifulSoup


def fetch_webpage(url):
    """
    Downloads a webpage and returns its HTML content.
    """

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "WebsiteAccessibilityChecker/1.0"}
        )

        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException as error:
        print(f"Error accessing website: {error}")
        return None



def check_image_alt_text(soup):
    """
    Checks whether images have missing or potentially unhelpful alt text.
    """

    issues = []

    images = soup.find_all("img")

    generic_descriptions = [
        "image",
        "photo",
        "picture",
        "graphic",
        "image of",
        "photo of"
    ]

    for index, image in enumerate(images, start=1):
        alt_text = image.get("alt")

        # Check whether the alt attribute is missing.
        if alt_text is None:
            issues.append(
                f"Image {index} is missing an alt attribute."
            )

        # Check for potentially generic descriptions.
        elif alt_text.strip().lower() in generic_descriptions:
            issues.append(
                f"Image {index} has generic alt text: '{alt_text}'."
            )

    return issues



def check_page_title(soup):
    """
    Checks whether the webpage has a title.
    """

    issues = []

    title = soup.find("title")

    if title is None or not title.get_text(strip=True):
        issues.append("Webpage is missing a meaningful title.")

    return issues


def check_heading_structure(soup):
    """
    Checks whether the webpage has a main heading.
    """

    issues = []

    if not soup.find("h1"):
        issues.append("Webpage is missing an H1 heading.")

    return issues


def check_links(soup):
    """
    Checks whether links have accessible text.
    """

    issues = []

    links = soup.find_all("a")

    for link in links:
        link_text = link.get_text(strip=True)

        if not link_text and not link.find("img", alt=True):
            issues.append("Link is missing accessible text.")

    return issues


def check_html_language(soup):
    """
    Checks whether the HTML element declares the page language.
    """

    issues = []

    html_tag = soup.find("html")

    if html_tag is None or not html_tag.get("lang", "").strip():
        issues.append(
            "HTML element is missing a language declaration."
        )

    return issues


def check_form_labels(soup):
    """
    Checks whether form fields have accessible labels.
    """

    issues = []

    fields = soup.find_all(["input", "textarea", "select"])

    for field in fields:
        field_type = field.get("type", "").lower()

        # Skip input types that do not require labels.
        if field.name == "input" and field_type in [
            "hidden", "submit", "button", "reset", "image"
        ]:
            continue

        field_id = field.get("id")
        field_name = field.get("name")

        # Check for a label surrounding the field.
        has_wrapping_label = field.find_parent("label") is not None

        # Check for a label connected using the field's ID.
        has_matching_label = (
            field_id is not None
            and soup.find("label", attrs={"for": field_id}) is not None
        )

        # Check for an ARIA label.
        has_aria_label = bool(field.get("aria-label", "").strip())

        # Check whether aria-labelledby references existing elements.
        labelledby_ids = field.get("aria-labelledby", "").split()

        has_aria_labelledby = (
            bool(labelledby_ids)
            and all(soup.find(id=element_id) for element_id in labelledby_ids)
        )

        has_label = (
            has_wrapping_label
            or has_matching_label
            or has_aria_label
            or has_aria_labelledby
        )

        if not has_label:
            field_description = field_id or field_name or field.name

            issues.append(
                f"Form control '{field_description}' "
                "may be missing an accessible name."
            )

    return issues


def analyze_accessibility(html):
    """
    Runs all accessibility checks on webpage HTML.
    """

    soup = BeautifulSoup(html, "html.parser")

    results = {
        "Images": check_image_alt_text(soup),
        "Page Title": check_page_title(soup),
        "Headings": check_heading_structure(soup),
        "Links": check_links(soup),
        "HTML Language": check_html_language(soup),
        "Form Labels": check_form_labels(soup)
    }

    return results
