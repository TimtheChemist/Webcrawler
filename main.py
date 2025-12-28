import sys
from asynccrawler import crawl_site_async
import asyncio




async def main():
    print("Hello from webcrawler!")
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    entered_url = sys.argv[1]
    print(f"starting crawl of: {entered_url}")

    page_data = await crawl_site_async(entered_url)
    print(page_data)




if __name__ == "__main__":
    asyncio.run(main())
