'''
    Title: Military Rocket Control Source Code
    Author: SmithJ_Dev
    Date: 09/01/2022
    Code version: 1.2
    If there is a problem, please contact https://twitter.com/a5coenXWcLBd7W
'''
'''
    Install pybluez using the command:
        pip install pybluez

    Start the program using the command:
        python -i rocket_port10.py or python -i rocket_port3.py
'''

from bluetooth import *
import time
import socket as sock 

from pybluez import bluetooth

host = "00:11:67:E3:B9:09"

# They seem to have hardcoded the RFComm port.
# From our bruteforce, we get that we have to connect to port 10 first, disconnect (sock.close()),
# then the actual interaction will happen on port 3.
# After, most of the time, we can directly connect to port 3.

port = 10
print("---- Connecting to {} port {}.".format(host, port))
try: 
    sock=BluetoothSocket(RFCOMM)
    sock.bind(("", port))
    sock.connect((host, port))

    print("---- Waiting for 5 secs before closing socket.".format(host, port))
    time.sleep(5)
    sock.close()
    
    print("---- Socket Closed!")
except Exception as e:
    print("Error : ", e)