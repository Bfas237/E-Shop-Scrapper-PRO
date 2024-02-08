from setuptools import find_packages
from distutils.core import setup
import os

# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = 'E-Shop Scrapper PRO is a Python script that scrapes product data from an e-commerce website and exports it to a CSV file. It utilizes web scraping techniques to extract information such as product names, categories, prices, descriptions, and images. '

setup(
    # Name of the package
    name='EScraperPRO',
    # Packages to include into the distribution
    packages=find_packages('.'),
    # Start with a small number and increase it with
    # every change you make https://semver.org
    version='1.0.5',
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository. For example: MIT
    license='MIT',
    # Short description of your library
    description='A Python script for scraping product data from e-commerce sites',
    # Long description of your library
    long_description=long_description,
    long_description_content_type='text/markdown',
    # Your name
    author='vision4geeks Solutions',
    # Your email
    author_email='vision4geeks@gmail.com',
    # Link from which the project can be downloaded
    url='https://github.com/vision4geeks/EScraperPRO',
    # Link from which the project can be downloaded
    download_url='https://github.com/vision4geeks/EScraperPRO/archive/v1.0.5.tar.gz',
    # List of keywords
    keywords=['web scraping', 'e-commerce', 'product data', 'asyncio'],
    # List of packages to install with this one
    install_requires=[
        'aiohttp',
        'aiofiles',
        'pandas',
        'tqdm',
        'validators',
        'beautifulsoup4',
        'geocoder',
        'colorist'
    ],
    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    # Entry points
    entry_points={
        'console_scripts': [
            'EscrapperPRO = EscrapperPRO.__main__:main'
        ]
    }
)
