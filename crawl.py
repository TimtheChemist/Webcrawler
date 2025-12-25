from urllib.parse import urlparse


def normalize_url(input_url):
    url_object = urlparse(input_url)
    if url_object.path[-1] == "/":
        url_path_processed = url_object.path[:-1]
        return url_object.hostname + url_path_processed
    return url_object.hostname + url_object.path