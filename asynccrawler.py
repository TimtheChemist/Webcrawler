import asyncio
import aiohttp
from crawl import urlparse, normalize_url, extract_page_data, get_urls_from_html


class AsyncCrawler():
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):


        async with self.lock:
            if self.should_stop is True:
                return False

            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")

                for task in self.all_tasks:
                    task.cancel()

                return False

            if normalized_url in self.page_data:
                return False
            else: 
                return True


    async def get_html(self, url):
        try:
            async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as resp:

                
                if resp.status >= 400:
                    raise Exception(f"Status_code: {resp.status}")

                if "text/html" not in resp.headers.get("content-type", ""):
                    raise Exception(f"Content-type header is not text/html")
                
                return await resp.text()


        
        except Exception as e:
            print(f"Something went wrong! {e}")
            return None




    async def crawl_page(self, current_url=None):
        if self.should_stop is True:
            return 

        if current_url == None:
            current_url = self.base_url


        normalised_current_url = normalize_url(current_url)

        current_url_object = urlparse(current_url)
        base_url_object = urlparse(self.base_url)


        if current_url_object.netloc != base_url_object.netloc:
            return 

        if await self.add_page_visit(normalised_current_url) == False:
            return 

        async with self.semaphore:
            html = await self.get_html(current_url)
        
        if html is None:
            return 
        
        async with self.lock:
            self.page_data[normalised_current_url] = extract_page_data(html, current_url)
        
        print(f"Crawling {current_url}")

        url_list = get_urls_from_html(html, current_url)



        tasks = []
        for url in url_list:   
            task = asyncio.create_task(self.crawl_page(url))
            tasks.append(task)
            self.all_tasks.add(task)

        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)

            finally:
                for task in tasks:
                    self.all_tasks.discard(task)


        return 


    async def crawl(self):
        await self.crawl_page(self.base_url)

        return self.page_data

async def crawl_site_async(base_url, max_concurrency, max_pages):
    crawler = AsyncCrawler(base_url, max_concurrency, max_pages)
    async with crawler:
        page_data = await crawler.crawl()

    return page_data