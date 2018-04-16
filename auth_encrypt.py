#!/usr/bin/env python
"""
Roughly based on: http://code.activestate.com/recipes/576980-authenticated-encryption-with-pycrypto/
"""

import hashlib
import hmac

from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto.Util.number import long_to_bytes

__author__ = 'Dirk Moors'
__copyright__ = 'Copyright 2014, Dirk Moors'
__version__ = "1.0.0"
__status__ = "Production"

HASH_ALGO = hashlib.sha256

SIG_SIZE = HASH_ALGO().digest_size

class AuthenticationError(Exception):
    pass

def get_random_bytes(amount):
    return long_to_bytes(random.getrandbits(amount * 8))

def compare_mac(mac, mac_verif):
    if len(mac) != len(mac_verif):
        print "invalid MAC size"
        return False

    result = 0
    for x, y in zip(mac, mac_verif):
        result |= ord(x) ^ ord(y)
    return result == 0

def encrypt(data, shared_key, hmac_key):
    """encrypt data with AES-CBC and sign it with HMAC-SHA256"""
    pad = AES.block_size - len(data) % AES.block_size
    data = data + pad * chr(pad)
    iv_bytes = get_random_bytes(AES.block_size)
    cypher = AES.new(shared_key, AES.MODE_CBC, iv_bytes)
    encrypted_data = cypher.encrypt(data)
    iv_data = iv_bytes + encrypted_data
    sig = hmac.new(hmac_key, iv_data, HASH_ALGO).digest()
    return (encrypted_data, iv_bytes, sig)

def decrypt(encrypted_data, iv_bytes, signature, shared_key, hmac_key):
    """verify HMAC-SHA256 signature and decrypt data with AES-CBC"""
    iv_data = iv_bytes + encrypted_data
    if not compare_mac(hmac.new(hmac_key, iv_data, HASH_ALGO).digest(), signature):
        raise AuthenticationError("message authentication failed")
    cypher = AES.new(shared_key, AES.MODE_CBC, iv_bytes)
    data = cypher.decrypt(encrypted_data)
    return data[:-ord(data[-1])]

if __name__ == "__main__":
    SHARED_KEY = get_random_bytes(AES.block_size)
    HMAC_KEY = get_random_bytes(SIG_SIZE)

    (encrypted_data, iv_bytes, signature) = encrypt("appelflap", SHARED_KEY, HMAC_KEY)
    decrypted_data = decrypt(encrypted_data, iv_bytes, signature, SHARED_KEY, HMAC_KEY)
    print decrypted_data