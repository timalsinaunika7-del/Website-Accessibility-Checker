
import unittest
from bs4 import BeautifulSoup

from accessibility_checker import (
    check_image_alt_text,
    check_page_title,
    check_heading_structure,
    check_links,
    check_html_language,
    check_form_labels
)


class TestImageAltText(unittest.TestCase):

    def test_missing_alt_attribute(self):
        html = '<img src="cat.jpg">'
        soup = BeautifulSoup(html, "html.parser")

        results = check_image_alt_text(soup)

        self.assertEqual(len(results), 1)

    def test_generic_alt_text(self):
        html = '<img src="dog.jpg" alt="image">'
        soup = BeautifulSoup(html, "html.parser")

        results = check_image_alt_text(soup)

        self.assertEqual(len(results), 1)

    def test_descriptive_alt_text(self):
        html = '<img src="flower.jpg" alt="A red flower">'
        soup = BeautifulSoup(html, "html.parser")

        results = check_image_alt_text(soup)

        self.assertEqual(len(results), 0)

    def test_decorative_image(self):
        html = '<img src="decoration.png" alt="">'
        soup = BeautifulSoup(html, "html.parser")

        results = check_image_alt_text(soup)

        self.assertEqual(len(results), 0)


class TestPageTitle(unittest.TestCase):

    def test_missing_title(self):
        html = '<html><body>Hello</body></html>'
        soup = BeautifulSoup(html, "html.parser")

        results = check_page_title(soup)

        self.assertEqual(len(results), 1)

    def test_existing_title(self):
        html = '<html><head><title>My Website</title></head></html>'
        soup = BeautifulSoup(html, "html.parser")

        results = check_page_title(soup)

        self.assertEqual(len(results), 0)


class TestHeadingStructure(unittest.TestCase):

    def test_missing_h1(self):
        html = '<html><body><h2>Welcome</h2></body></html>'
        soup = BeautifulSoup(html, "html.parser")

        results = check_heading_structure(soup)

        self.assertEqual(len(results), 1)

    def test_existing_h1(self):
        html = '<html><body><h1>Welcome</h1></body></html>'
        soup = BeautifulSoup(html, "html.parser")

        results = check_heading_structure(soup)

        self.assertEqual(len(results), 0)


class TestLinks(unittest.TestCase):

    def test_link_without_accessible_text(self):
        html = '<a href="/home"></a>'
        soup = BeautifulSoup(html, "html.parser")

        results = check_links(soup)

        self.assertEqual(len(results), 1)

    def test_link_with_text(self):
        html = '<a href="/home">Visit Home</a>'
        soup = BeautifulSoup(html, "html.parser")

        results = check_links(soup)

        self.assertEqual(len(results), 0)

    def test_link_with_image_alt_text(self):
        html = '<a href="/home"><img src="logo.png" alt="Home"></a>'
        soup = BeautifulSoup(html, "html.parser")

        results = check_links(soup)

        self.assertEqual(len(results), 0)


class TestHTMLLanguage(unittest.TestCase):

    def test_missing_language(self):
        html = '<html><body>Hello</body></html>'
        soup = BeautifulSoup(html, "html.parser")

        results = check_html_language(soup)

        self.assertEqual(len(results), 1)

    def test_existing_language(self):
        html = '<html lang="en"><body>Hello</body></html>'
        soup = BeautifulSoup(html, "html.parser")

        results = check_html_language(soup)

        self.assertEqual(len(results), 0)


class TestFormLabels(unittest.TestCase):

    def test_missing_form_label(self):
        html = '<input type="text" id="username">'
        soup = BeautifulSoup(html, "html.parser")

        results = check_form_labels(soup)

        self.assertEqual(len(results), 1)

    def test_explicit_label(self):
        html = '''
        <label for="username">Username</label>
        <input type="text" id="username">
        '''
        soup = BeautifulSoup(html, "html.parser")

        results = check_form_labels(soup)

        self.assertEqual(len(results), 0)

    def test_wrapping_label(self):
        html = '''
        <label>
            Email
            <input type="email">
        </label>
        '''
        soup = BeautifulSoup(html, "html.parser")

        results = check_form_labels(soup)

        self.assertEqual(len(results), 0)

    def test_aria_label(self):
        html = '<input type="text" aria-label="Search">'
        soup = BeautifulSoup(html, "html.parser")

        results = check_form_labels(soup)

        self.assertEqual(len(results), 0)

    def test_valid_aria_labelledby(self):
        html = '''
        <span id="search-label">Search</span>
        <input type="text" aria-labelledby="search-label">
        '''
        soup = BeautifulSoup(html, "html.parser")

        results = check_form_labels(soup)

        self.assertEqual(len(results), 0)

    def test_invalid_aria_labelledby(self):
        html = '''
        <input type="text" aria-labelledby="missing-label">
        '''
        soup = BeautifulSoup(html, "html.parser")

        results = check_form_labels(soup)

        self.assertEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
