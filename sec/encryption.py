from cryptography.fernet import Fernet
import hashlib
import base64
import hmac
import json
from typing import Union

def get_hashed_password(password:str) -> str:
    password = password.encode()
    h = hmac.new(b'23cj31lnd',b'',hashlib.sha3_512)
    h.update(password)
    return h.hexdigest()

def get_user_key(password:str) -> bytes:
    key = password.encode().ljust(32,b'\0')[:32]
    key = base64.urlsafe_b64encode(key)
    return key

def encrypt_the_content(content:Union[list, dict, str], user_key) -> str:
    cipher_suite = Fernet(user_key)
    encoded_content = json.dumps(content).encode()
    encrypted_content:bytes = cipher_suite.encrypt(encoded_content)
    decoded_content:str = encrypted_content.decode()
    return decoded_content

def decrypt_the_content(content:str, user_key) -> Union[list, dict, str]:
    cipher_suite = Fernet(user_key)
    encoded_content = content.encode()
    decrypted_content:bytes = cipher_suite.decrypt(encoded_content)
    decoded_content: Union[list, dict, str] = json.loads(decrypted_content.decode())
    return decoded_content
