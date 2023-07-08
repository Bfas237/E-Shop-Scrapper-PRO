# E-Shop Scrapper PRO

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Requirements](#requirements)
- [Files](#files)
- [Usage](#usage)
- [Contributing](#contributing)
- [Issues](#issues)
- [License](#license)
- [Contact](#contact)

![image](https://github.com/Bfas237/E-Shop-Scrapper-PRO/assets/24810035/b94a3736-3237-4fd7-b04a-aa6457956961)



## Description

**E-Shop Scrapper PRO** is a Python script that scrapes product data from an e-commerce website and exports it to a CSV file. It utilizes web scraping techniques to extract information such as product names, categories, prices, descriptions, and images. The script is designed to be highly customizable and can be adapted to scrape data from different e-commerce websites.

## Features

- Scrapes product data from an e-commerce website
- Extracts product names, categories, prices, descriptions, and images
- Generates a random date and time for each scraped product
- Supports customization for different e-commerce websites
- Writes the scraped data to a CSV file
- Displays a progress bar during the scraping process


## Prerequisites

Before using **E-Shop Scrapper PRO**, make sure you have the following knowledge and tools:

- Basic understanding of Python programming language
- Familiarity with PHP, HTML and CSS
- Familiar with how Woocommerce, and Wordpress works
- Python 3 installed on your system ([Download Python](https://www.python.org/downloads/))


### Python Installation

1. Install Python: If Python is not already installed on your system, follow these steps:

   - Visit the official Python website at https://www.python.org.
   - Go to the Downloads section and select the appropriate Python version for your operating system (Windows, macOS, or Linux).
   - Download the installer and run it.
   - Follow the installation wizard instructions and make sure to check the box that says "Add Python to PATH" during the installation process.
   - Once the installation is complete, open a command prompt (Windows) or terminal (macOS/Linux) and type `python --version` to verify that Python is installed correctly. You should see the version number of Python printed in the console.

2. Verify Python installation: Open a command prompt or terminal and run `python --version` to ensure that Python is installed and accessible from the command line. You should see the version number of Python displayed.

Now that Python is installed, you can proceed with setting up the project and installing the dependencies as outlined in the rest of the README file.

## Installation

There are two ways to install E-Shop Scrapper PRO: using a release package or by forking and cloning the repository.

### Installation via Release

1. Go to the [Releases](https://github.com/bfas237/e-shop-scrapper-pro/releases) page of the GitHub repository.
2. Download the latest release package (`e-shop-scrapper-pro.zip`).
3. Extract the contents of the ZIP file to your desired location.
4. Open a command prompt or terminal and navigate to the extracted directory.
5. Run the following command to install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

### Installation by Forking and Cloning

1. Fork the [E-Shop Scrapper PRO](https://github.com/bfas237/e-shop-scrapper-pro) repository to your GitHub account.
2. Clone the forked repository to your local machine using the following command:

   ```shell
   git clone https://github.com/bfas237/e-shop-scrapper-pro.git
   ```

3. Navigate to the cloned directory:

   ```shell
   cd e-shop-scrapper-pro
   ```

4. Run the following command to install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

## Requirements

- Python (3.x)
- Pip (3.x)
- requests (2.26.0)
- BeautifulSoup (4.9.3)
- pandas (1.3.3)
- tqdm (4.62.3)
- tabulate (0.8.9)

## Files

The repository contains the following files:

- `e_shop_scrapper_pro.py`: The main Python script for scraping the e-commerce website.
- `requirements.txt`: A file specifying the required Python packages.
- `rhapsodybikeparts.csv`: The CSV file where the scraped data is stored.
- `LICENSE`: The license file for the project.

## Usage

1. Modify the `base_url` variable in the script to match the target e-commerce website.

2. Run the script:

```bash
python e_shop_scrapper_pro.py
```

3. Wait for the scraping process to complete. The progress bar will indicate the progress.

4. After completion, the CSV file `rhapsodybikeparts.csv` will be generated in the same directory.

5. Open the CSV file to view the scraped data.

## Contributing

Contributions are welcome! Here's how you can contribute to the E-Shop Scrapper PRO project:

1. Fork the repository.

2. Create a new branch:

```bash
git checkout -b feature/your-feature
```

3. Make your changes and commit them:

```bash
git commit -m 'Add your feature'
```

4. Push the changes to your forked repository:

```bash
git push origin feature/your-feature
```

5. Open a pull request on the main repository.

Please make sure to follow the code style and provide clear commit messages.

## Issues

If you encounter any issues or have suggestions for improvements, please create a new issue on the GitHub repository.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contact

For more information or questions, you can reach us on:

- Website: [about.me/bfaschat](https://about.me/bfaschat)
- Twitter: [@bfaschat](https://twitter.com/bfaschat)

---

Thank you for using E-Shop Scrapper PRO. Happy scraping!
