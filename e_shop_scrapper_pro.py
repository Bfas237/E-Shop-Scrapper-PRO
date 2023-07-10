import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from tqdm import tqdm
import subprocess
from tabulate import tabulate
import re, os
import random
from datetime import datetime, timedelta
 
# Generate a random date and time
start_date = datetime(2022, 1, 1)
end_date = datetime.now()
random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

# Format the random date and time
formatted_date = random_date.strftime("%Y-%m-%d %H:%M:%S")

# Set the headers for the HTTP requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

# Initialize variables
productlinks = []  # List to store product links
data = []  # List to store product data
categories = []  # List to store categories
base_url = "https://rcfminibikes.com/product-category/all/page/"  # Base URL for the product pages

# Send a request to the first page to get the total number of products
response = requests.get(base_url + "1", headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
# Define the number of products displayed per page
products_per_page = 16 

# Find the pagination element in the HTML
pagination_info = soup.find('nav', class_='woocommerce-pagination')

if pagination_info:
    # Extract the page numbers from the pagination element
    page_numbers = pagination_info.find_all('a', class_='page-numbers')
    
    # Check if there are page numbers available
    if page_numbers:
        # Get the second-to-last page number (last page often represented by "next" link)
        last_page = int(page_numbers[-2].text)
    else:
        last_page = 0
        
    # Calculate the total number of products based on the last page number and products per page
    total_products = last_page * products_per_page
else:
    # If no pagination information is found, set total_products to 0
    total_products = 0

# Calculate the total number of pages

total_pages = (total_products - 1) // products_per_page + 1
# Loop through each page
for page in tqdm(range(1, total_pages + 1), desc='Scraping Pages'):
    url = base_url + str(page)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all product summaries on the current page
    product_list = soup.find_all('div', class_='wpbf-woo-loop-summary')

    # Extract the product links from the product summaries
    for product_summary in product_list:
        # Extract the post title from the <h3> tag
        post_title = product_summary.find('h3', class_='woocommerce-loop-product__title').text
       
        # Extract the href link from the <a> tag
        link = product_summary.find('a', class_='woocommerce-LoopProduct-link')['href']
        productlinks.append(link)

# Initialize a list to store product names
product_names = []
import csv

# Initialize the list to store product data
data = []

# Iterate through each product link
for link in tqdm(productlinks, desc='Scraping Products'):
    # Send a GET request to the product page
    f = requests.get(link, headers=headers).text
    hun = BeautifulSoup(f, 'html.parser')

    try:
        # Extract the price from the product details
        price_element = hun.find('p', class_='price')

        # Check if the price element exists and contains a valid price
        if price_element and price_element.text.strip() != '':
            price = price_element.find('bdi').text.strip()
        else:
            price = None

    except Exception as e:
        print(f"Error: {e}")
        price = None

    try:
        # Extract the product name from the product details
        name = hun.find('h1', class_='product_title').text.strip()
        product_names.append(name)

    except Exception as e:
        print(f"Error: {e}")
        name = None

    try:
        # Generate the slug from the name
        slug = re.sub(r'\s+', '_', name).lower()
        slug = re.sub(r'[^\w\s-]', '', slug)

    except Exception as e:
        print(f"Error: {e}")
        slug = None

    try:
        # Find the summary section
        summary_element = hun.find('div', class_='woocommerce-product-details__short-description')

        # Extract the contents under the summary section
        summary = summary_element.decode_contents().strip() if summary_element else None

    except Exception as e:
        print(f"Error: {e}")
        summary = None

    try:
        # Extract the SKU from the product details
        sku = hun.find('span', class_='sku').text.strip()

    except Exception as e:
        print(f"Error: {e}")
        sku = None

    try:
        # Join the product names using ', ' and assign to the 'tags' variable
        categories_element = hun.find('span', class_='posted_in')
        tags = [a.text for a in categories_element.find_all('a')]
        print("Featured Tags:", ", ".join(tags))

    except Exception as e:
        print(f"Error: {e}")
        tags = None


    description_html = None  # Initialize the variable outside the try-except block

    try:
        # Find the description tab
        description_tab = hun.find('li', class_='description_tab')
        
        if description_tab:
            description_content = description_tab.find_next('div', class_='woocommerce-Tabs-panel')
            
            if description_content:
                description_html = description_content.decode_contents()
            else:
                description_html = None
        else:
            description_html = None

    except Exception as e:
        print(f"Error: {e}")
        description_html = None

    try:
        # Find the additional information tab
        additional_info_tab = hun.find('li', class_='additional_information_tab')
        
        if additional_info_tab:
            additional_info_content = additional_info_tab.find_next('div', class_='woocommerce-Tabs-panel').decode_contents()

            # Extract the attribute details from additional_info_content
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
            additional_info_content = None
            attribute = ""
            attribute_data = ""
            attribute_default = ""

    except Exception as e:
        print(f"Error: {e}")
        additional_info_content = None
        attribute = ""
        attribute_data = ""
        attribute_default = ""


    try:
       
        image_div = hun.find('div', class_='woocommerce-product-gallery')
        image_tags = image_div.find_all('img')

        featured_image = image_tags[0]['src'] if image_tags else None
        gallery_images = [img['src'] for img in image_tags[1:]] if len(image_tags) > 1 else None

        featured_images = f"{featured_image} ! alt : {name} ! title : {name}.jpg ! desc : {name} ! caption : {' | '.join(gallery_images) if gallery_images is not None else ''}"
        
        


    except Exception as e:
        print(f"Error: {e}")
        featured_images = None
        gallery_images = None

    try:
        # Find the last <a> tag in the breadcrumb navigation
        breadcrumb_nav = hun.find('nav', class_='woocommerce-breadcrumb')
        last_a_tag = breadcrumb_nav.find_all('a')[-1]

        # Get the text of the last <a> tag, which is the category
        category = last_a_tag.text.strip()

    except Exception as e:
        print(f"Error: {e}")
        category = None

    # Create a dictionary to store the product data
    product_data = {
    "post_title": name,
    "post_name": slug,
    "post_parent": "",
    "ID": "",
    "post_content": description_html,
    "post_excerpt": summary,
    "post_status": "publish",
    "post_password": "",
    "menu_order": "",
    "post_date": "",
    "post_author": "",
    "comment_status": "open",
    "_sku": sku,
    "parent_sku": "",
    "parent": "",
    "_children": "",
    "_downloadable": "no",
    "_virtual": "no",
    "_stock": "",
    "_regular_price": price,
    "_sale_price": "",
    "_weight": "",
    "_length": "",
    "_width": "",
    "_height": "",
    "_tax_class": "",
    "_visibility": "",
    "_stock_status": "instock",
    "_backorders": "no",
    "_manage_stock": "no",
    "_tax_status": "taxable",
    "_upsell_ids": "",
    "_crosssell_ids": "",
    "_featured": "",
    "_sale_price_dates_from": "",
    "_sale_price_dates_to": "",
    "_download_limit": "0",
    "_download_expiry": "0",
    "_product_url": "",
    "_button_text": "",
    "meta:_yoast_wpseo_focuskw": "",
    "meta:_yoast_wpseo_title": "",
    "meta:_yoast_wpseo_metadesc": "",
    "meta:_yoast_wpseo_metakeywords": "",
    "images": featured_images,
    "downloadable_files": "",
    "product_page_url": "",
    "tax:product_type": "simple",
    "tax:product_visibility": "",
    "tax:product_cat": category,
    "tax:product_tag": ', '.join(tags) if tags else None,
    "tax:product_shipping_class": "",
    "meta:partdo_post_views_count": "",
    "meta:total_sales": "",
    "attribute": attribute,
    "attribute_data": attribute_data,
    "attribute_default": attribute_default
}

    # Append the product data to the list
    data.append(product_data)

# Specify the file name for the CSV file
csv_file_name = 'rcfminibikes.csv'

# Get the absolute path of the current working directory
current_dir = os.getcwd()

# Get the absolute path of the CSV file based on the current working directory
csv_file_path = os.path.join(current_dir, csv_file_name)

# Write the product data to a CSV file
with open(csv_file_path, 'w', encoding='utf8', newline='') as f:
    # Check if the data list is not empty
    if data:
        fc = csv.DictWriter(f, fieldnames=data[0].keys())
        fc.writeheader()
        
        print('Now writing data to CVS file...')

        # Use tqdm to track the progress of writing
        progress_bar = tqdm(total=len(data), desc='Writing CSV')

        for row in data:
            fc.writerow(row)
            progress_bar.update(1)

        # Close the tqdm progress bar
        progress_bar.close()
    else:
        print('No data available. CSV file not created.')

# Open the CSV file after writing is done
try:
    if os.name == 'nt':  # Check if the system is Windows
        os.startfile(csv_file_path)
    elif os.name == 'posix':  # Check if the system is macOS or Linux
        subprocess.call(['xdg-open', csv_file_path])
    else:
        print('Unable to open the CSV file. Please open it manually.')
except:
    print('Unable to open the CSV file. Please open it manually.')

# Create a DataFrame from the product data
df = pd.DataFrame(data)

# Print the DataFrame
print(df)