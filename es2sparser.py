# escrapper > main_scrapper.py

"""
This file contains the parsers that will check the different pages and then
grab the equivalent data
"""

from typing import Any, Dict, List, Tuple
from bs4 import BeautifulSoup


class ParsePage():
    def __init__(self, html_soup: BeautifulSoup, config, index=None) -> None:
        self.soup =BeautifulSoup(html_soup, 'html.parser')
        self.config = config
        self.index = index
        self.total = 0

    def find_tags(self, cls, elm):
        return self.soup.find(cls, class_= elm)
    
    def get_all_pages(self):
        """Get Total Number Of Pages"""

        pagination_tag = self.soup.find( 
            self.config["pn_mark"]["type"]["html"], 
            class_ = self.config["pn_mark"]["type"]["class"]
        )

        if pagination_tag:
            page_numbers = pagination_tag.find_all(
                self.config["pn_num"]["type"]["html"], 
                class_ = self.config["pn_num"]["type"]["class"]
            )

            last_page = int(page_numbers[-1].text) if page_numbers[-1].text.isdigit() else int(page_numbers[-2].text)
            print(f"Found {last_page} pages")
            return last_page
        return 0
    
    def get_all_items(self):
        product_tag = self.soup.find(
            self.config["ey_point"]["type"]["html"], 
            class_ = self.config["ey_point"]["type"]["class"]
        )

        products = product_tag.find_all(
            self.config["pt_item"]["type"]["html"]
        )

        self.total = len(products)

        print(f"found {self.total} products in page {self.index}")

        return product_tag

    


