import csv

def write_csv_report(page_data, filename="report.csv"):

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["page_url", "h1", "first_paragraph", "outgoing_link_urls", "image_urls"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader() # Writes column names

        for page in page_data.values():
            writer.writerow(";".join(page["outgoing_links"]))
