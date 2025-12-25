from urllib.parse import urlparse
from bs4 import BeautifulSoup


def normalize_url(input_url):
    url_object = urlparse(input_url)
    if url_object.path[-1] == "/":
        url_path_processed = url_object.path[:-1]
        return url_object.hostname + url_path_processed
    return url_object.hostname + url_object.path


def get_h1_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.h1 == None:
        return ""
    return soup.h1.get_text()

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.p == None:
        return ""
    if soup.main == None:
        return ""

    return soup.main.p.get_text()