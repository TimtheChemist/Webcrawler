

def crawler_analytics(url_list, page_data_dict):
    print(f"{len(url_list)} URLs were examined.")

    for key, value in page_data_dict.items():
        
        if "url" in page_data_dict:
            print(f"{page_data_dict["url"]}: {page_data_dict["h1"]}")