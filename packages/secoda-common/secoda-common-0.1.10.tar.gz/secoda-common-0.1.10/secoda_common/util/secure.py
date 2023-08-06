from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
import os
import base64


def check_key_path(key_path: str):
    if not os.path.exists(key_path) or not os.path.isfile(key_path):
        raise Exception(f'Key does not exist at {key_path}')


def encrypt(key_path: str, content: str):
    check_key_path(key_path)
    key = RSA.import_key(open(key_path, 'r').read())
    return base64.b64encode(PKCS1_OAEP.new(key).encrypt(content.encode('utf-8'))).decode('utf-8')


def decrypt(key_path: str, content: str):
    check_key_path(key_path)
    pkey = RSA.import_key(open(key_path, 'r').read())
    return PKCS1_OAEP.new(pkey).decrypt(base64.b64decode(content.encode('utf-8'))).decode('utf-8')


def big_encrypt(key_path: str, content: str) -> (str, str):
    check_key_path(key_path)
    aes_key = get_random_bytes(16)
    rsa_key = RSA.import_key(open(key_path, 'r').read())

    # Encrypt the data
    cipher = AES.new(aes_key, AES.MODE_EAX)
    ciphertext = base64.b64encode(cipher.encrypt(content.encode('utf-8'))).decode('utf-8')

    # Encrypt the AES key
    enc_key = base64.b64encode(PKCS1_OAEP.new(rsa_key).encrypt(aes_key)).decode('utf-8')

    # Return both
    # Note that a comma ',' is NOT a valid base64 character, so it is a safe deliminator
    return ciphertext, f'{enc_key},{base64.b64encode(cipher.nonce).decode("utf-8")}'


def big_decrypt(key_path: str, aes_string: str, content: str):
    check_key_path(key_path)
    rsa_key = RSA.import_key(open(key_path, 'r').read())
    enc_key, nonce = aes_string.split(',')

    # Decrypt the aes key
    aes_key = PKCS1_OAEP.new(rsa_key).decrypt(base64.b64decode(enc_key.encode('utf-8')))

    # Decrypt the data
    cipher = AES.new(aes_key, AES.MODE_EAX, base64.b64decode(nonce.encode('utf-8')))
    ciphertext = cipher\
        .decrypt(base64.b64decode(content.encode('utf-8')))\
        .decode('utf-8')

    # return both
    return ciphertext
