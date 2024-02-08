import sys
from cryptography.fernet import Fernet
import base64
import urllib3, warnings

warnings.filterwarnings("ignore", category=UserWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

pastel_green = "\033[38;5;120m"
pastel_blue = "\033[38;5;81m"
pastel_purple = "\033[38;5;99m"
bold = "\033[1m"
end = "\033[0m"


print(pastel_blue + """
                
                                    ___________________________________
                                    |#######====================#######|
                                    |#       E-SCRAPPER PRO V2.0.0    #|
                                    |#** *****     /===\   ******   **#|
                                    |*#           | (") |            #*|
                                    |#*           | /v\ |            *#|
                                    |#             \===/              #|
                                    |##======== @VISION4GEEKS =======##|
                                    ------------------------------------       
                                     
                                        
	""" + end)

# Decrypt the code
def decrypt_code(encrypted_code, key):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_code).decode()

# Load the key from the file
with open('secure.config', 'rb') as file:
    key_loaded = file.read()

# Load the encrypted code from the file
with open('EScraperPRO.config', 'rb') as file:
    encrypted_code_loaded = file.read()

# Decrypt the code and execute it (passing arguments from the console)
try:
    decrypted_code = decrypt_code(encrypted_code_loaded, key_loaded)
    exec(decrypted_code)
except Exception as e:
    print(f"Decryption failed: {e}")
