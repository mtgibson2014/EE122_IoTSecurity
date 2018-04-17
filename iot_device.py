import socket
import time
import requests
import thread
import threading
import sched, time
from auth_encrypt import *

# Getting Message from Box
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('', 5000))
serversocket.listen(1)

# Sending Message to Box
#create an INET, STREAMing socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host,
# and a well-known port


while True:
    try:
        time.sleep(5)
        clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        clientsocket.connect(('', 9000))

        def send_to_box():
            def printit():
              threading.Timer(10.0, printit).start()
              clientsocket.send("Sent from iot")
              print (" >>> Sending to Box")

            printit()


        try:
            thread.start_new_thread(send_to_box, ())
            conn, address = serversocket.accept()     # Establish connection with client.
            print ("Connected to client at " + str(address))
            while True:
                msg = conn.recv(1024)
                print address[1], ' >> ', msg


        except Exception as e:
            print("Should not come here")
            serversocket.close()
            clientsocket.close()
            if conn != None:
                print ("closing socket: " + str(conn))
                conn.close()

            print(e)
            break
    except Exception as e:
        serversocket.close()
        clientsocket.close()
        print("Error " + str(e))
        break






