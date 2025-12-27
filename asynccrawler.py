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
                self.page_data[normalized_url] = {}
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
        if current_url == None:
            current_url = self.base_url


        normalised_current_url = normalize_url(current_url)

        current_url_object = urlparse(current_url)
        base_url_object = urlparse(self.base_url)


        if current_url_object.netloc != base_url_object.netloc:
            return self.page_data

        if await self.add_page_visit(normalised_current_url) == False:
            return self.page_data

        async with self.semaphore:
            html = await self.get_html(current_url)
        
        if html is None:
            return self.page_data
        
        async with self.lock:
            self.page_data[normalised_current_url] = extract_page_data(html, current_url)
        
        print(f"Getting page data from {current_url}")

        url_list = get_urls_from_html(html, current_url)



        tasks = []
        for url in url_list:   
            task = asyncio.create_task(self.crawl_page(url))
            tasks.append(task)

        await asyncio.gather(*tasks)


        return self.page_data