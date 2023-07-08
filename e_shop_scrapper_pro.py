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
base_url = "https://rhapsodybikeparts.com/shop/page/"  # Base URL for the product pages


# Send a request to the first page to get the total number of products
response = requests.get(base_url + "1", headers=headers)

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

print(total_products)

# Calculate the total number of pages

total_pages = (total_products - 1) // 16 + 1

# Loop through each page
for page in tqdm(range(1, total_pages + 1), desc='Scraping Pages'):
    url = base_url + str(page)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all product titles on the current page
    product_list = soup.find_all("h2", {"class": "woocommerce-loop-product__title"})

    # Extract the product links from the product titles
    for product in product_list:
        link = product.find("a", {"class": "woocommerce-LoopProduct-link-title"}).get('href')
        productlinks.append(link)

# Initialize a list to store product names
product_names = []

# Iterate through each product link
for link in tqdm(productlinks, desc='Scraping Products'):
    # Send a GET request to the product page
    f = requests.get(link, headers=headers).text
    hun = BeautifulSoup(f, 'html.parser')

    try:
        # Find the <img> tag with class "wp-post-image" within the BeautifulSoup object
        img_tag = hun.find('img', class_='wp-post-image')

        # Check if the <img> tag is found
        if img_tag:
            # Extract the image URL from the 'src' attribute of the <img> tag
            image_url = img_tag['src']

            # Concatenate the updated image details using the "!" symbol
            updated_image_details = f"{image_url}"
            
            # Print each set of details on a new line
            image = updated_image_details
    except:
        image = None

    try:
        # Extract the category from the product details
        category_span = soup.find('span', class_='posted_in')
        find_category = hun.find("div", {"class": "single-product-category"}).text.replace('\n', "")

        # If the category span exists, extract each category name
        if category_span:
            for category_link in category_span.find_all('a'):
                category_name = category_link.text
                categories.append(category_name)

        # Join the categories into a string
        category_result = ', '.join(categories)

        # Use the category from product details if available, otherwise use the categories extracted
        category = find_category if find_category is not None else category_result
    except:
        category = None

    try:
        # Extract the price from the product details
        price_element = hun.find('span', class_='woocommerce-Price-amount')
        price = price_element.text.strip()
    except:
        price = None

    try:
        # Extract the product description from the product details
        descriptions = hun.find_all('div', attrs={"aria-labelledby": "tab-title-description"})[0]
        unwrapped_elements = descriptions.find_all(["h2", "p", "ul"])
        unwrapped_contents = [str(element) for element in unwrapped_elements]
        result = ' '.join(unwrapped_contents)
        about = result
    except:
        about = None

    try:
        # Extract the product name from the product details
        name = hun.find("h1", {"class": "product_title"}).text.replace('\n', "")
        product_names.append(name)
    except:
        name = None

    try:
        # Generate the slug from the name
        slug = re.sub(r'\s+', '_', name).lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
    except:
        slug = None

    try:
        # Assign the formatted date and time to the 'post_date' key in the dictionary
        date = formatted_date
    except:
        date = None

    try:
        # Join the product names using ', ' and assign to the 'tags' variable
        tags = ', '.join(product_names)
    except:
        tags = None

    # Create a dictionary to store the product data
    product_data = {
        "post_title": name,
        "post_name": slug,
        "post_parent": "",
        "ID": "",
        "post_content": about,
        "post_excerpt": "",
        "post_status": "publish",
        "post_password": "",
        "menu_order": "",
        "post_date": date,
        "post_author": "",
        "comment_status": "open",
        "sku": "",
        "parent_sku": "",
        "children": "",
        "downloadable": "no",
        "virtual": "no",
        "stock": "",
        "regular_price": price,
        "sale_price": "",
        "weight": "",
        "length": "",
        "width": "",
        "height": "",
        "tax_class": "",
        "visibility": "",
        "stock_status": "instock",
        "backorders": "no",
        "sold_individually": "no",
        "low_stock_amount": "",
        "manage_stock": "no",
        "tax_status": "taxable",
        "upsell_ids": "",
        "crosssell_ids": "",
        "purchase_note": "",
        "sale_price_dates_from": "",
        "sale_price_dates_to": "",
        "download_limit": "0",
        "download_expiry": "0",
        "product_url": "",
        "button_text": "",
        "images": image,
        "downloadable_files": "",
        "product_page_url": "",
        "meta:total_sales": "",
        "tax:pwb-brand": "",
        "tax:product_type": "",
        "tax:product_visibility": "",
        "tax:product_cat": category,
        "tax:product_tag": tags,
        "tax:product_shipping_class": ""
    }

    # Append the product data to the list
    data.append(product_data)

# Specify the file name for the CSV file
csv_file_name = 'rhapsodybikeparts.csv'

# Get the absolute path of the current working directory
current_dir = os.getcwd()

# Get the absolute path of the CSV file based on the current working directory
csv_file_path = os.path.join(current_dir, csv_file_name)

# Write the product data to a CSV file
with open(csv_file_path, 'w', encoding='utf8', newline='') as f:
    fc = csv.DictWriter(f, fieldnames=data[0].keys())
    fc.writeheader()

    # Use tqdm to track the progress of writing
    progress_bar = tqdm(total=len(data), desc='Writing CSV')

    for row in data:
        fc.writerow(row)
        progress_bar.update(1)

    # Close the tqdm progress bar
    progress_bar.close()

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