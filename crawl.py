from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup


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



