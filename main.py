import sys
from get_html import get_html
from crawl import crawl_page




def main():
    print("Hello from webcrawler!")
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    entered_url = sys.argv[1]
    print(f"starting crawl of: {entered_url}")

    print(crawl_page(entered_url))




if __name__ == "__main__":
    main()
