################################################################################
# Import statements
################################################################################

import logging
import binascii

from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto import Random

################################################################################
# Basic functions
################################################################################

########################################
# Define core functions
########################################

def get_random_byte_string(byte_length):
    return Random.get_random_bytes(byte_length)

def byte_string_to_hex_string(byte_string):
    return binascii.hexlify(byte_string)

def hex_string_to_byte_string(hex_string):
    return binascii.unhexlify(hex_string)

def make_keys(cipher_type, key_size, iv_size):
    """ Generate keys that are is dumpable to JSON
    """
    cipher_key = get_random_byte_string(key_size)    # 256 bits (32 bytes)
    cipher_iv  = get_random_byte_string(iv_size)    # 16 bytes (same as block size)
    
    return {
        "cipher":   cipher_type,
        "key":      binascii.hexlify(cipher_key).decode("utf-8"),
        "iv":       binascii.hexlify(cipher_iv).decode("utf-8")
    }
    # import json
    # with open("cryptography-keys.json", "w+b") as f:
    #     f.write(json.dumps(cryptography))


########################################
# AES Encrypt/Decrypt functions
########################################

def aes_encrypt(cipher_key, cipher_iv, plain_text):
    cipher = AES.new(cipher_key, AES.MODE_CFB, cipher_iv)
    cipher_text = cipher.encrypt(plain_text)
    return cipher_text

def aes_decrypt(cipher_key, cipher_iv, cipher_text):
    cipher = AES.new(cipher_key, AES.MODE_CFB, cipher_iv)
    plain_text = cipher.decrypt(cipher_text)
    return plain_text

def aes_encrypt_as_hex(crypto_struct, plain_text):
    cipher_key = hex_string_to_byte_string(crypto_struct['key'])
    cipher_iv  = hex_string_to_byte_string(crypto_struct['iv'])
    cipher = AES.new(cipher_key, AES.MODE_CFB, cipher_iv)
    cipher_text = cipher.encrypt(plain_text.encode("utf-8"))
    return binascii.hexlify(cipher_text).decode("utf-8")


def aes_decrypt_from_hex(crypto_struct, hex_text):
    cipher_key = hex_string_to_byte_string(crypto_struct['key'])
    cipher_iv  = hex_string_to_byte_string(crypto_struct['iv'])
    cipher = AES.new(cipher_key, AES.MODE_CFB, cipher_iv)
    cipher_text = binascii.unhexlify(hex_text)
    plain_text = cipher.decrypt(cipher_text).decode("utf-8")
    return plain_text


def aes_sample_usage():
    aes_key = get_random_byte_string(32)    # 256 bits (32 bytes)
    aes_iv  = get_random_byte_string(16)    # 16 bytes (same as block size)

    # Hardcode for re-testability
    aes_key_hex_string = "480b41eec90e92aabe6ec159768d7d88fa64eb35a91c7e5c39b89be53eab0d06"
    aes_iv_hex_string = "ed0306cc63b48a3ab0405608aa4ea334"

    aes_key = hex_string_to_byte_string(aes_key_hex_string)
    aes_iv  = hex_string_to_byte_string(aes_iv_hex_string)

    cipher_text = aes_encrypt(aes_key, aes_iv, "Attack at dawn")
    print(cipher_text)

    plain_text = aes_decrypt(aes_key, aes_iv, cipher_text)
    print(plain_text)


########################################
# Hash functions
########################################

def sha256_as_hex(plain_text):
    return SHA256.new(data=plain_text.encode("UTF8")).hexdigest()

def sha256_sample_usage():
    return sha256_as_hex("Hello world")


def hmacsha256_as_hex(key, plain_text):
    h = HMAC.new(key.encode("UTF8"), digestmod = SHA256)
    h.update(plain_text.encode("UTF8"))
    return h.hexdigest()


def verify_hmacsha256_from_hex(key, plain_text, hex_mac):
    h = HMAC.new(key.encode("UTF8"), digestmod = SHA256)
    h.update(plain_text.encode("UTF8"))
    try:
        h.hexverify(hex_mac)
        return True
    except ValueError:
        return True

def hmacsha256_sample_usage():
    secret_key = "globalpass"
    message = "Hello world"
    hex_mac = hmacsha256_as_hex(secret_key, message)
    is_valid = verify_hmacsha256_from_hex(secret_key, message, hex_mac)


########################################
# PBKDF functions
########################################

def derive_32bytes_as_hex(password, salt_hex_string, count=1000000):
    salt_bytes = hex_string_to_byte_string(salt_hex_string)
    encoded_password = password.encode("UTF8")
    return PBKDF2(encoded_password, salt_bytes, 32, count = count, hmac_hash_module = SHA256)


def derive_32bytes_sample():
    salt_hex_string = "480b41eec90e92aabe6ec159768d7d88fa64eb35a91c7e5c39b89be53eab0d06"
    count = 2000000
    key = derive_32bytes_as_hex("hello world", salt_hex_string, count)
    hex_key = byte_string_to_hex_string(key)
    print("hex_key {0}".format(hex_key))


################################################################################
# Variables dependent on Application basic functions
################################################################################

# N/A

################################################################################
# Main function
################################################################################

if __name__ == '__main__':
    pass