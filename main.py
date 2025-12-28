import sys
from asynccrawler import crawl_site_async
import asyncio




async def main():
    print("Hello from webcrawler!")
    if len(sys.argv) < 4:
        print("too few arguments provided")
        sys.exit(1)

    if len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    entered_url = sys.argv[1]
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])
    print(f"starting crawl of: {entered_url}")

    page_data = await crawl_site_async(entered_url, max_concurrency, max_pages)

    for url, info in page_data.items():
        print(f"Report: {info['url']}")
    
    print(page_data)




if __name__ == "__main__":
    asyncio.run(main())
