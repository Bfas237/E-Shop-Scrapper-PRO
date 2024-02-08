# config.py

import base64
import binascii
import re, os, subprocess
import typing
from colorist import BgColor, Color, Effect
from cryptography.fernet import Fernet, InvalidToken
import base64
import binascii
import typing

class CustomFernet(Fernet):
    def __init__(self, key: typing.Union[bytes, str], backend: typing.Any = None):
        try:
            key = base64.urlsafe_b64decode(key)
        except binascii.Error as exc:
            raise ValueError(f"{BgColor.RED}{Effect.UNDERLINE} Corrupt Config Key: {Effect.OFF}{BgColor.OFF} Your Fernet key is not valid. Run {Color.BLUE}{Effect.BOLD}python -m EscrapperPRO -h{Effect.OFF}{Color.OFF} for Help") from exc
        if len(key) != 32:
            raise ValueError(f"{BgColor.RED}{Effect.UNDERLINE} Invalid Config Key: {Effect.OFF}{BgColor.OFF} Your Fernet key has been tempered with. Run {Color.BLUE}{Effect.BOLD}python -m EscrapperPRO -h{Effect.OFF}{Color.OFF} for Help")

        self._signing_key = key[:16]
        self._encryption_key = key[16:]
        
        
# Regex pattern for valid product slugs (alphanumeric with hyphens)
valid_slug_pattern = r'[a-zA-Z0-9-]+'
GITHUB_REPO = r"https://github.com/Bfas237/E-Shop-Scrapper-PRO.git"
def save_encrypted_code_to_file(encrypted_code: bytes, code_file_path: str):
    """Save the encrypted code to a file."""
    with open(code_file_path, 'wb') as file:
        file.write(encrypted_code)

def save_key_to_file(key: bytes, key_file_path: str):
    """Save the key to a file."""
    with open(key_file_path, 'wb') as file:
        file.write(key)

def load_key_from_file(utils_folder: str, config: str):
    """Load the encryption key from a file."""
    key_file_path = os.path.join(utils_folder, config)
    with open(key_file_path, 'rb') as file:
        key_loaded = file.read()
    return key_loaded

def load_encrypted_code_from_file(utils_folder: str, config: str):
    """Load the encrypted code from a file."""
    code_file_path = os.path.join(utils_folder, config)
    with open(code_file_path, 'rb') as file:
        encrypted_code_loaded = file.read()
    return encrypted_code_loaded

required_modules = [
    'aiohttp',
    'aiofiles',
    'csv',
    'pandas',
    'tqdm',
    'validators',
    'bs4',
    'geocoder',
    'colorist'
]

# Decrypt the code
def decrypt_code(encrypted_code, key):
    """Decrypt the encrypted code."""
    try:
        cipher_suite = CustomFernet(key)
        decrypted_code = cipher_suite.decrypt(encrypted_code).decode()
        return decrypted_code
    except (TypeError, binascii.Error):
        raise ValueError(f"{BgColor.RED}{Effect.UNDERLINE} Unknown Error: {Effect.OFF}{BgColor.OFF} Please check your decryption key and try again.")
    
    except InvalidToken:
        if len(encrypted_code) % 16 != 0:
            raise ValueError(f"{BgColor.RED}{Effect.UNDERLINE} Invalid Token: {Effect.OFF}{BgColor.OFF} The encrypted code may be corrupted or incomplete.")
        else:
            raise ValueError(f"{BgColor.RED}{Effect.UNDERLINE} Invalid Config File: {Effect.OFF}{BgColor.OFF} The decryption key may be incorrect or the config files might be corrupted.")


# Generate a secret key
def generate_key():
    return Fernet.generate_key()

# Encrypt the code
def encrypt_code(code, key):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(code.encode())


def install_missing_modules(required_modules):
    # Iterate over required modules and install if missing
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            print(f"Installing {module}...")
            subprocess.run(['pip', 'install', module])

def update_requirements(required_modules):
    # Write the required modules to the requirements.txt file
    with open('requirements.txt', 'w') as file:
        for module in required_modules:
            file.write(f"{module}\n")


product_list_paths = [
    '/shop',
    '/shop-2',
    '/product-category/(?P<category_slug>{})'.format(valid_slug_pattern),
    '/featured-products',
    '/sale-products',
    '/best-selling-products',
    '/new-arrivals',
    '/products',
    '/all'
]
