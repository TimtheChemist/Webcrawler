from crawl import crawl_page


class AsyncCrawler():
    def __init__(self, base_url):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = 4
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None

	async def __aenter__(self):
		self.session = aiohttp.ClientSession()
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.page_data:
                return False
            else: 
                self.page_data[normalized_url] = True
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