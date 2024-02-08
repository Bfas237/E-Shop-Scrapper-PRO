
import os
import random
import asyncio
import re
import sys
import aiohttp
import aiofiles
import csv
import pandas as pd
from bs4 import BeautifulSoup
import tqdm
from tqdm.asyncio import trange
import urllib3
import validators
import http.client as httplib
from EscrapperPRO.__main__ import Vision4Geeks, getUrl, return_parser, scrape, show_choices_and_handle_input
from utils.config import product_list_paths, update_requirements, install_missing_modules, required_modules

import traceback
import platform
from datetime import datetime
import geocoder
from urllib.parse import urlparse
from colorist import  Color, BgColor, Effect


class Builder:
    def __init__(self, base_url):
        self.base_url = base_url
        self.productlinks = []
        self.data = []
        self.categories = []
        self.mega_links = []

    def have_internet(self, hosts="8.8.8.8") -> bool:
        conn = httplib.HTTPSConnection(hosts, timeout=5)
        try:
            conn.request("HEAD", "/")
            return True
        except Exception:
            return False
        finally:
            conn.close()


    async def get_location():
        # Use geocoder to get the location information
        location = geocoder.ip('me')
        return location.country
    async def send_message_to_dev(self, message):
        # Get additional information
        python_version = platform.python_version()
        computer_name = platform.node()
        country = await Builder.get_location()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        BOT_TOKEN = '6538097396:AAHkTCIuCyAh-hbLFl4JKm5pEH516kbbzYM'
        CHAT_ID = '810231628'
        # Construct the URL for sending a message to the bot
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        # Construct the message text with markdown formatting
        config = f'''
    *Upgrade Required:*

    *Python Version:* `{python_version}`
    *Computer Name:* `{computer_name}`
    *Country:* `{country}`
    *Time:* `{current_time}`

    *Customer Message:* `{message}`
    '''

        # Send the message using the Telegram Bot API
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json={'chat_id': CHAT_ID, 'text': config, 'parse_mode': 'MarkdownV2'}) as response:
                    return True
        except Exception as e:
            return False

    async def report_error(error_message):
        # Get additional information
        python_version = platform.python_version()
        computer_name = platform.node()
        country = await Builder.get_location()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        BOT_TOKEN = '6538097396:AAHkTCIuCyAh-hbLFl4JKm5pEH516kbbzYM'
        CHAT_ID = '810231628'
        # Construct the URL for sending a message to the bot
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        # Construct the message text
        message = f'''
        {BgColor.RED}{Effect.UNDERLINE}Error Report:{Effect.OFF}{BgColor.OFF}
        
        Python Version: {python_version}
        Computer Name: {computer_name}
        Country: {country}
        Time: {current_time}
        
        Error Message: {Color.YELLOW}{error_message}{Color.OFF}
        
        {Color.RED}Traceback:
        {traceback.format_exc()}{Color.OFF}'''

        # Construct the message text using Telegram MarkdownV2 syntax
        errmessage = f'''
        *Error Report:*
        
        *Python Version:* `{python_version}`
        *Computer Name:* `{computer_name}`
        *Country:* `{country}`
        *Time:* `{current_time}`
        
        *Error Message:* `{error_message}`
        
        *Traceback:*
        
        ```
        {traceback.format_exc()}
        ```
        '''

        # Send the message using the Telegram Bot API
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json={'chat_id': CHAT_ID, 'text': errmessage, 'parse_mode': 'MarkdownV2'}) as response:
                    print(f'''
                                {message}                   
                        ''')
        except Exception as e:
            print(f'Failed to send error message: {e}')


    @staticmethod
    def is_valid_woocommerce_shop(base_url):
        for path in product_list_paths:
            if re.search(path, base_url):
                return True
        return False


    def get_link(self, index) -> str:
        return "".join([self.base_url, "page/", str(index)])

    async def get_random_user_agent(self):
        
        project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        ua_file = os.path.join(project_root, "utils", "ua.txt")
        
        try:
            async with aiofiles.open(ua_file, 'r', encoding='utf8') as f:
                agents = await f.readlines()
                return {'User-Agent': random.choice(agents).strip()}
        except FileNotFoundError as e:
            await Builder.report_error(str(e))
            os.system("cls" if os.name == "nt" else "clear")
            endmessage = f"{BgColor.RED}{Effect.UNDERLINE} Scrapping Error: {Effect.OFF}{BgColor.OFF} The scrapping was unsuccessful\n"
                #print(f"{endmessage}")
                
            await show_choices_and_handle_input(endmessage)

    async def check(self, session: aiohttp.ClientSession, url: str) -> str:
        parser = await return_parser()
        
        if not Builder.have_internet(self):
            os.system("cls" if os.name == "nt" else "clear")
            endmessage = f"{BgColor.RED}{Effect.UNDERLINE} Internet Error: {Effect.OFF}{BgColor.OFF} Internet connection is required to scrape\n"
            #print(f"{endmessage}")
            
            await show_choices_and_handle_input(endmessage)

        try:
            async with session.get(url) as response:
                if response.status != 200:
                    
                    os.system("cls" if os.name == "nt" else "clear")
                    endmessage = f"{BgColor.RED}{Effect.UNDERLINE} Status Error: {Effect.OFF}{BgColor.OFF} Invalid status code: {response.status}\n"
                    #print(f"{endmessage}")
                    await show_choices_and_handle_input(endmessage)
                return await response.text()
        except aiohttp.ClientError as e:
            os.system("cls" if os.name == "nt" else "clear")
            endmessage = f"{BgColor.RED}{Effect.UNDERLINE} Dev Error: {Effect.OFF}{BgColor.OFF} {str(e)}\n"
            #print(f"{endmessage}")
            await show_choices_and_handle_input(endmessage)



    async def get_total_products(self, session, max_pages=2):
        html = await self.check(session, self.get_link(1))
        soup = BeautifulSoup(html, "html.parser")
        pagination_tag = soup.find("nav", class_="woocommerce-pagination")
        last_page = 1
        
        if pagination_tag:
            page_numbers = pagination_tag.find_all(
                "a", 
                class_=["page-numbers", "page-number"]
            )

            if page_numbers:
                if len(page_numbers) == 1:
                    last_page = int(page_numbers[0].text)
                else:
                    last_page = int(page_numbers[-1].text) if page_numbers[-1].text.isdigit() else int(page_numbers[-2].text)
                    
                # Check if there's a next page link, indicating more pages
                next_link = pagination_tag.find("a", class_="page-numbers")

                # If there's a next page link, adjust last_page accordingly
                if next_link:
                    last_page += 1

                # Limit the number of pages to scrape if max_pages is specified
                if max_pages is not None:
                    last_page = min(last_page, max_pages)

                return last_page
        else:
            # Limit the number of pages to scrape if max_pages is specified
            last_page = min(1, max_pages) if max_pages is not None else 2
            flist = [self.get_link(i) for i in range(1, last_page + 1)]
            pbar = tqdm.tqdm(total=len(flist), desc='Checking pagination')

            # Iterate over the range of page numbers
            for page_number in range(1, len(flist) + 1):
                async with session.get(self.get_link(page_number)) as response:
                    if response.status != 200: 
                        last_page -= 1 
                        flist = [self.get_link(i) for i in range(1, last_page - 1)]
                        pbar.total = len(flist)
                        pbar.refresh()
                        pbar.update()
                    else:
                        last_page +=1
                        flist = [self.get_link(i) for i in range(1, last_page + 1)]
                        pbar.total = len(flist)
                        pbar.refresh()
                        pbar.update()
                    

            pbar.close()
            #print(f"Found {last_page-1} pages")
            return last_page-1

    async def scrape_product_links(self, session, total_pages):
        
        for page in trange(1, total_pages + 1, desc='Scraping Pages'):
            try:
                url = self.get_link(page)
                html = await self.check(session, url)
                soup = BeautifulSoup(html, 'html.parser')
            
                product_list = soup.find('ul', class_='products')
                if product_list:
                    # If product list is found, try to find products within 'li' elements
                    product_items = product_list.find_all('li', class_=['product', 'type-product'])
                else:
                    # If product list is not found, try to find products within 'div' elements
                    product_items = soup.find_all('div', class_=['product', 'type-product'])

                for product_summary in product_items:
                    link = product_summary.find('a', class_='woocommerce-LoopProduct-link')['href']
                    self.productlinks.append(link)
            except  Exception as e:
                await Builder.report_error(str(e))
                os.system("cls" if os.name == "nt" else "clear")
                endmessage = f"{BgColor.RED}{Effect.UNDERLINE} Scrapping Error: {Effect.OFF}{BgColor.OFF} The scrapping was unsuccessful\n"
                #print(f"{endmessage}")
                
                await show_choices_and_handle_input(endmessage)

    async def scrape_product_data(self, session, max_products=12):
        products_scraped = 0
        
        for link in trange(len(self.productlinks), desc='Scraping Products', total=max_products):
            if products_scraped >= max_products:
                print(f"Maximum number of products ({max_products}) scraped. Stopping...")
                break
            html = await self.check(session, self.productlinks[link])
            hun = BeautifulSoup(html, "html.parser")
            try:
                price_element = hun.find('p', class_='price')
                price = price_element.find('bdi').text.strip() if price_element and price_element.text.strip() != '' else None
                name = None

                h1_title = hun.find('h1', class_='product_title')
                if h1_title:
                    name = h1_title.text.strip()
                else:
                    h2_title = hun.find('h2', class_='product_title')
                    if h2_title:
                        name = h2_title.text.strip()
                    else:
                        h3_title = hun.find('h3', class_='product_title')
                        if h3_title:
                            name = h3_title.text.strip()

                
                slug = re.sub(r'\s+', '_', name).lower() if name else None
                slug = re.sub(r'[^\w\s-]', '', slug) if slug else None
                
                summary_element = hun.find('div', class_='woocommerce-product-details__short-description')
                summary = summary_element.decode_contents().strip() if summary_element else None
                
                sku = hun.find('span', class_='sku').text.strip() if hun.find('span', class_='sku') else None
                
                categories_element = hun.find('span', class_='posted_in')
                tags = [a.text for a in categories_element.find_all('a')] if categories_element else None
                
                
                product_description = hun.find('div', class_=['woocommerce-Tabs-panel', 'woocommerce-Tabs-panel--description', 'panel entry-content'])
                if product_description:
                    # Remove only the first <h2> tag from description
                    first_h2_tag = product_description.find('h2')
                    if first_h2_tag:
                        first_h2_tag.decompose()
                    product_description = product_description.decode_contents()
                else:
                    product_description = None

                    
                additional_info_tab = hun.find('li', class_='additional_information_tab')
                if additional_info_tab:
                    additional_info_content = additional_info_tab.find_next('div', class_='woocommerce-Tabs-panel').decode_contents()
                    additional_info_soup = BeautifulSoup(additional_info_content, 'html.parser')
                    attribute_elements = additional_info_soup.find_all('tr', class_='woocommerce-product-attributes-item')

                    attributes = {}
                    for attribute_element in attribute_elements:
                        attribute_label = attribute_element.find('th', class_='woocommerce-product-attributes-item__label').text.strip()
                        attribute_value = attribute_element.find('td', class_='woocommerce-product-attributes-item__value').text.strip()
                        attributes[attribute_label] = attribute_value

                    attribute = attributes.get("Attribute", "")
                    attribute_data = attributes.get("Attribute Data", "")
                    attribute_default = attributes.get("Attribute Default", "")
                else:
                    attribute = ""
                    attribute_data = ""
                    attribute_default = ""

                image_div = hun.find('div', class_='woocommerce-product-gallery')
                image_tags = image_div.find_all('img') if image_div else None
                
                featured_image = image_tags[0]['src'] if image_tags else None
                gallery_images = [img['src'] for img in image_tags[1:]] if len(image_tags) > 1 else None
                
                featured_images = f"{featured_image} ! alt : {name} ! title : {name}.jpg ! desc : {name} ! caption : {' | '.join(gallery_images) if gallery_images is not None else ''}" if featured_image else None
                
                breadcrumb_nav = hun.find('nav', class_='woocommerce-breadcrumb')
                last_a_tag = breadcrumb_nav.find_all('a')[-1] if breadcrumb_nav else None
                category = last_a_tag.text.strip() if last_a_tag else None
                
                # Store the data
                self.data.append({
                    'price': price,
                    'name': name,
                    'slug': slug,
                    'summary': summary,
                    'sKU': sku,
                    'tags': tags,
                    'description': product_description,
                    'attribute': attribute,
                    'attribute_Data': attribute_data,
                    'attribute_Default': attribute_default,
                    'featured_Images': featured_images,
                    'category': category
                })
                # Increment the counter after successfully scraping a product
                products_scraped += 1
            except Exception as e:
                await Builder.report_error(str(e))
                os.system("cls" if os.name == "nt" else "clear")
                endmessage = f"{BgColor.RED}{Effect.UNDERLINE} Scrapping Error: {Effect.OFF}{BgColor.OFF} The scrapping was unsuccessful\n"
                #print(f"{endmessage}")
                
                await show_choices_and_handle_input(endmessage)
                
    async def save_data_to_csv_and_print(self):
        url = await getUrl()
        parsed_url = urlparse(url)
        parsed_url = parsed_url.netloc
        parser = await return_parser()
        csv_file_name = f'EscraperPRO_{(parsed_url)}.csv'
        script_dir = os.path.dirname(os.path.realpath(__file__))
        csv_file_path = os.path.join(script_dir, csv_file_name)
        endmessage = f"\n{BgColor.RED}{Effect.UNDERLINE} Error Opening File: {Effect.OFF}{BgColor.OFF} Unable to open the CSV file. Please open it manually.\n"
        csvmessage = f"\n{BgColor.BLUE}{Effect.UNDERLINE} CSV Data Preview: {Effect.OFF}{BgColor.OFF} The scraping process has been completed.\n"
        
        async with aiofiles.open(csv_file_path, 'w', encoding='utf8', newline='') as f:
            try:
                if self.data:
                    fc = csv.DictWriter(f, fieldnames=self.data[0].keys())
                    await fc.writeheader()
                    
                    success = f"\n{BgColor.GREEN}{Effect.UNDERLINE} Writing to CSV: {Effect.OFF}{BgColor.OFF} Stay positive and keep moving forward! 😊\n"
                    print(success)

                    progress_bar = trange(len(self.data), desc='Writing CSV')

                    for row in self.data:
                        await fc.writerow(row)
                        progress_bar.update(1)

                    progress_bar.close()
            except Exception as e:
                await Builder.report_error(str(e)) 
                await show_choices_and_handle_input(endmessage)

        try:
           
            while True:
                Vision4Geeks()
                print(csvmessage)
                open_csv = input("Do you want to open the CSV file? (y/n): ").lower()
                if open_csv == 'y':
                    if os.name == 'posix':
                        subprocess.call(['xdg-open', csv_file_path])
                        Vision4Geeks()
                        exit(2)
                    elif os.name == 'nt':
                        os.startfile(csv_file_path)
                        Vision4Geeks()
                        parser.help(parser)
                        exit(2)
                    else:
                        print(f'{endmessage}')
                else:
                    Vision4Geeks()
                    parser.help(parser)
                    exit(2)
        except Exception as e:
            print(f'{endmessage}')
            await show_choices_and_handle_input(endmessage)

            
            
    async def Run(self):
        if not Builder.have_internet(self):
            os.system("cls" if os.name == "nt" else "clear")
            endmessage = f"{BgColor.RED}{Effect.UNDERLINE} Run Error: {Effect.OFF}{BgColor.OFF} Internet connection is required to scrape\n"
            #print(f"{endmessage}")
            await show_choices_and_handle_input(endmessage)
        async with aiohttp.ClientSession(headers=await self.get_random_user_agent()) as session:
            
            total_pages = await self.get_total_products(session)
            await self.scrape_product_links(session, total_pages)
            await self.scrape_product_data(session)
            await self.save_data_to_csv_and_print()
