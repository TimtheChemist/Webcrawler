import unittest
from crawl import normalize_url
from crawl import get_h1_from_html
from crawl import get_first_paragraph_from_html
from crawl import get_urls_from_html
from crawl import get_images_from_html


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_2(self):
        input_url = "https://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_3(self):
        input_url = "http://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)


    def test_get_h1_from_html(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_blank(self):
        input_body = '<html><body><h1></h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_no_h1(self):
        input_body = '<html><body></body></html>'
        actual = get_h1_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_h1_from_html_blank(self):
        input_body = '<html><body><h1></h1></body></html>'
        actual = get_h1_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)


    def test_get_first_paragraph_from_html_basic(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_main2(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)


    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute2(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html>
        <body>
            <a href="https://blog.boot.dev">Abs</a>
            <a href="/about">Rel</a>
            <a>No href</a>
            <a href="">Empty</a>
        </body>
        </html>'''
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev","https://blog.boot.dev/about"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute3(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html>
        <body>
            <a href="/about">About Us</a>
        </body>
        </html>'''
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/about"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute4(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html>
        <body>
            <a href="">About Us</a>
        </body>
        </html>'''
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)


    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative2(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="https://blog.boot.dev/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative3(self):
        input_url = "https://blog.boot.dev"
        input_body = """
        <html>
        <body>
            <img src="/logo.png" alt="Logo">
            <img alt="No source here">
            <img src="" alt="Empty source">
        </body>
        </html>
        """
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)




if __name__ == "__main__":
    unittest.main()

