import requests

def get_html(url):

    try:
        r = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})

        if r.status_code >= 400:
            raise Exception(f"Status_code: {r.status_code}")

        if "text/html" not in r.headers['content-type']:
            raise Exception(f"Content-type header is not text/html")
              
        return r.text

    
    except Exception as e:
        f"Something went wrong! {e}"
        return None