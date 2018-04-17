import socket
import select
import thread
import time
from auth_encrypt import *
from OpenSSL import SSL
import ssl

HOST = "https://c31d6f06.ngrok.io"
NGROK_PORT = 443
HOST = socket.getaddrinfo(HOST, NGROK_PORT)[0][4][0]


SHARED_KEY = "ajdurhfvbycuie8734f.,kixhbdjxv98"
HMAC_KEY = "8s9bdhcuxk.,1230"

IV_LEN = 16
SIGN_LEN = 32



#socket to send data over to iot device
to_iot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
to_iot.connect(('', 5000))

#socket to receive from iot
from_iot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
from_iot.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
from_iot.bind(('', 9000))
from_iot.listen(5)

#create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host,
# and a well-known port
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('', 3000))
#become a server socket
serversocket.listen(1)
conn = None

exiting = False

@profile
def listen_to_iot():
    print("Waiting from IoT")
    conn, addr = from_iot.accept()
    print("Connected to IoT")
    while True:
        msg = conn.recv(1024)
        print 'IoT device: ', addr[1], ' >> ', msg
        context = SSL.Context(SSL.SSLv23_METHOD)
        sock = socket.socket()
        sock = SSL.Connection(context, sock)
        sock.connect(('www.google.com', 443))
        start_time = time.time()
        sock.do_handshake()
        end_time = time.time()
        actual_time = end_time - start_time
        print("Time for Handshake: " + str(actual_time))
        print 'IoT device: ', addr[1], ' >> Done Handshake'
        return

@profile
def on_new_client(conn,addr):

    while True:
        msg = conn.recv(1024)
        if msg.strip() == "q":
            conn.close()
            print("Received disconnect message.  Shutting down " + str(addr[1]))
            break

        iv_bytes = msg[0:IV_LEN]
        signature = msg[IV_LEN:IV_LEN+SIGN_LEN]
        encrypted_data = msg[IV_LEN+SIGN_LEN:]
        try:
            start_time = time.time()
            content = decrypt(encrypted_data, iv_bytes, signature, SHARED_KEY, HMAC_KEY)
            end_time = time.time()
            actual_time = end_time - start_time
            print("Time for decrypt: " + str(actual_time))

        except AuthenticationError as e:
            serversocket.close()
            to_iot.close()
            from_iot.close()
            print("There's an attack.")

        else:
            to_iot.send(content)
            print addr[1], ' >> ', content
            # exiting = True
            return

@profile
def verify_cb(conn, x509, errno, errdepth, retcode):
  """
  callback for certificate validation
  should return true if verification passes and false otherwise
  """
  if errno == 0:
    if errdepth != 0:
      # don't validate names of root certificates
      return True
    else:
      if x509.get_subject().commonName != HOST:
        return False
  else:
    return False


while not exiting:
    try:
        # Establish connection with client.
        thread.start_new_thread(listen_to_iot, ())
        conn, addr = serversocket.accept()
        thread.start_new_thread(on_new_client, (conn,addr))
        print ("Connected to client at " + str(addr))
        # if(exiting):
        #     break


    except Exception as e:
        serversocket.close()
        to_iot.close()
        from_iot.close()
        if conn != None:
            print ("closing socket: " + str(conn))
            conn.close()

        print(e)
        break




