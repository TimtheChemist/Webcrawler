from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from get_html import get_html
from crawler_analytics import crawler_analytics


def normalize_url(input_url):
    url_object = urlparse(input_url)
    if input_url == "":
        return ""
    combined_url = url_object.netloc + url_object.path
    combined_url = combined_url.rstrip("/")

    return combined_url.lower()



def get_h1_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1_variable = soup.find("h1")
    if h1_variable == None:
        return ""
    return h1_variable.get_text(strip=True)


def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    main_section = soup.find("main")
    if main_section:
        first_p = main_section.find("p")
        if first_p:
            return first_p.get_text(strip=True)
    first_p = soup.find("p")   
    if first_p:
        return first_p.get_text(strip=True)

    return ""


def get_urls_from_html(html, base_url):
    url_list = []
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('a'):
        href_variable = link.get('href')
        if href_variable:
            try:
                url_list.append(urljoin(base_url, href_variable)) 

            except Exception as e:
                print(f"{str(e)}: {href_variable}")


    return url_list

def get_images_from_html(html, base_url):
    url_list = []
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all('img'):
        img_variable = link.get('src')

        if img_variable:
            try:
                url_list.append(urljoin(base_url, img_variable)) 

            except Exception as e:
                print(f"{str(e)}: {img_variable}")

    return url_list


def extract_page_data(html, page_url):
    page_dict = {}
    page_dict["url"] = page_url
    page_dict["h1"] =  get_h1_from_html(html)
    page_dict["first_paragraph"] = get_first_paragraph_from_html(html)
    page_dict["outgoing_links"] = get_urls_from_html(html, page_url)
    page_dict["image_urls"] = get_images_from_html(html, page_url)

    return page_dict


def crawl_page(base_url, current_url=None, page_data=None):
    if current_url == None:
        current_url = base_url

    if page_data == None:
        page_data = {}

    normalised_current_url = normalize_url(current_url)

    current_url_object = urlparse(current_url)
    base_url_object = urlparse(base_url)

    if current_url_object.netloc != base_url_object.netloc:
        return page_data

    if normalised_current_url in page_data:
        return page_data
    
    html = get_html(current_url)
    if html is None:
        return page_data

    page_data[normalised_current_url] = extract_page_data(html, current_url)
    
    print(f"Getting page data from {current_url}")

    url_list = get_urls_from_html(html, current_url)



    for url in url_list:
        page_data = crawl_page(base_url, url, page_data)

    crawler_analytics(url_list, page_data)
    return page_data



