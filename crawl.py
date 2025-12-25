from urllib.parse import urlparse
from urllib.parse import urljoin
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

def get_urls_from_html(html, base_url):
    url_list = []
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('a'):
        href_variable = link.get('href')
        if href_variable:
            url_list.append(urljoin(base_url, href_variable)) 

    return url_list

def get_images_from_html(html, base_url):
    url_list = []
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('img'):
        img_variable = link.get('src')
        if img_variable:
            url_list.append(urljoin(base_url, img_variable)) 

    return url_list