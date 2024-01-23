import logging
import asyncio
import aiohttp
import os
import json
from es2sparser import ParsePage

class SiteConfig:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename

    def get_config(self, sitename: str) -> dict:
        try:
            with open(self.filename) as file:
                return json.load(file)[sitename]
        except Exception as error:
            raise error

class Es2pro:
    def __init__(self, urls: list, headers: dict):
        self.headers: dict = headers
        self.urls: list = urls
        self.tasks: list = []
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # File handler
        file_handler = logging.FileHandler('scraper.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        # Stream handler (console)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    async def fetch(self, session, url):
        self.logger.info(f'Fetching {url}')
        async with session.get(url) as response:
            return await response.text()

    async def scrape(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            self.tasks = [asyncio.create_task(self.fetch(session, url)) for url in self.urls]
            results = await asyncio.gather(*self.tasks)
            return results

    async def main(self):
        data = await self.scrape()
        config = SiteConfig("siteconfig.json").get_config("WooCommerce")
        parsed_page = ParsePage(data[0], config)
        total_items = parsed_page.get_all_items()
        #self.logger.info(f'Total items: {total_items}')

if __name__ == '__main__':
    urls = [
        "https://rcfminibikes.com/product-category/all"
        #'https://offermanwoodshop.com/store/'
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }

    scraper = Es2pro(urls, headers)
    asyncio.run(scraper.main())
