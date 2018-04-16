import socket
import select
import thread
import time
from auth_encrypt import *

SHARED_KEY = "ajdurhfvbycuie8734f.,kixhbdjxv98"
HMAC_KEY = "8s9bdhcuxk.,1230"

IV_LEN = 16
SIGN_LEN = 32
MSG_SIZE = 64


def on_new_client(clientsocket,addr):
    while True:
        msg = clientsocket.recv(1024)
        if msg.strip() == "q" or msg == "":
            conn.close()
            print("Received disconnect message.  Shutting down " + str(addr[1]))
            break

        #do some checks and if msg == someWeirdSignal: break:

        # parsed = msg.split("@")
        # content = parsed[0]
        # time_from_client = parsed[1]
        # print addr[1], ' >> ', content
        # print addr[1], ' time taken: ', time.time() - float(time_from_client)

        iv_bytes = msg[0:IV_LEN]
        signature = msg[IV_LEN:IV_LEN+SIGN_LEN]
        encrypted_data = msg[IV_LEN+SIGN_LEN:MSG_SIZE]
        start_time = 
        try:
        	start_time = ...
        	content = decrypt(encrypted_data, iv_bytes, signature, SHARED_KEY, HMAC_KEY)
        	end_time = ...
        except AuthenticationError as e:
        	print("There's an attack.")
        else:
        	print addr[1], ' >> ', content

        #msg = raw_input('SERVER >> ')
        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
        #clientsocket.send(msg)
    clientsocket.close()


port = 6000
#create an INET, STREAMing socket
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host,
# and a well-known port
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('', port))
#become a server socket
serversocket.listen(5)
print("\nconnected to port " + str(port))
conn = None

#pick a large output buffer size because i dont necessarily know how big the incoming packet is
while True:
    try:
        conn, address = serversocket.accept()     # Establish connection with client.
        thread.start_new_thread(on_new_client,(conn,address))
        print ("Connected to client at " + str(address))
        # output = conn.recv(2048);
        # if output.strip() == "q":
        #     conn.close()
        #     print("Received disconnect message.  Shutting down.")
        #     break
        # elif output:
        #     print ("Message received from client " + " : " + output)
        #     print (address[0])

    except Exception as e:
        if conn != None:
            print ("closing socket: " + str(conn))
            conn.close()

        print(e)
        break

