import socket
import time
import requests
from auth_encrypt import *


url = 'https://a950f6a0.ngrok.io'
payload = {'key1': 'value1', 'key2': 'value2'}

# GET with params in URL
r = requests.get(url, params=payload)

# iv_bytes_len = 16
# sign_len = 32

SHARED_KEY = "ajdurhfvbycuie8734f.,kixhbdjxv98"
HMAC_KEY = "8s9bdhcuxk.,1230"


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('', 6000))

quit = False

print("Connected. Type 'q' to quit")

while not quit:
    msg = raw_input("Enter your message: ")
    if msg == "q" or msg == "Q" or msg =="quit":
        quit = True
        clientsocket.send(msg)
        clientsocket.close()
    else:
        actual_time = time.time()
        print(actual_time)
        (encrypted_data, iv_bytes, signature) = encrypt(msg, SHARED_KEY, HMAC_KEY)
        msg = iv_bytes + signature + encrypted_data
        print(len(iv_bytes))
        print(len(signature))
        print(len(encrypted_data))
        print(len(msg))
        clientsocket.send(msg)

