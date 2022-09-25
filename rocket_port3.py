'''
    Title: Military Rocket Control Source Code
    Author: SmithJ_Dev
    Date: 09/01/2022
    Code version: 1.2
    If there is a problem, please contact https://twitter.com/a5coenXWcLBd7W
'''
'''
Procedure of the program

    Install pybluez using the command:
        pip install pybluez

    Start the program using the command:
        python -i rocket_port3.py
'''

# This is code version 1.2, and future versions may be committed to github.
from bluetooth import *
import time
import socket as sock 

from pybluez import bluetooth

global counterDown
counterDown = 0x2D

global counterUp
counterUp = 0x03

# receive data until the packet size matches the header
def rx():
    data = None
    try:
        while data == None:
            data = sock.recv(1024)
        while len(data) < 3:
            data = data + sock.recv(1024)
        while len(data) < ord(chr(data[1])) + 3:
            data = data + sock.recv(1024)
    except IOError as e:
        print("IOError rx(): {}".format(e))

    print("\tReceiving ({}):\t{}".format(len(data), " ".join([hex(i) for i in data])))
    return data

def tx(data):
    sock.send(data)
    print("\tSending ({}):\t{}".format(len(data), " ".join([hex(ord(i)) for i in data])))

def counterUpStr():
    global counterUp
    if(counterUp == 0xFF):
        counterUp = 0x00
    else:
        counterUp = counterUp + 1

    return chr(counterUp)

def counterDownStr():
    global counterDown
    if(counterDown == 0x00):
        counterDown = 0xFF
    else:
        counterDown = counterDown - 1

    return chr(counterDown)

def dc_cmd(cmd):
    if(cmd == 'left'):
        seq = "\x30\x38\x30\x30\x30\x46\x38"
    elif(cmd == 'right'):
        seq = "\x31\x38\x30\x30\x30\x46\x39"
    elif(cmd == 'up'):
        seq = "\x30\x30\x30\x38\x30\x46\x38"
    elif(cmd == 'down'):
        seq = "\x30\x30\x31\x38\x30\x46\x39"
    elif(cmd == 'fire'):
        seq = "\x30\x30\x30\x30\x39\x46\x39"
    elif(cmd == 'stop'):
        seq = "\x30\x30\x30\x30\x30\x46\x30"
    else:
        print('Error: Command not exist.')
        return
    data = "\x55\x0f\x00\x43\x00" + counterUpStr() + "\x00\x01\x0a" + seq  + "\x0d" + counterDownStr()
    tx(data)
    rx()

def left():
    dc_cmd('left')

def right():
    dc_cmd('right')

def up():
    dc_cmd('up')

def down():
    dc_cmd('down')

def fire():
    for i in range (0, 10):
        dc_cmd('fire')
        time.sleep(0.8)

handshakeMaybe = ["\x55\x06\x00\x02\x00\x00\x00\x38\xc0",
                "\x55\x0d\x00\x4c\x00\x01\x00\x00\x00\x00\x06\x3d\xab\xf3\xfe\xc7",
                "\x55\x3e\x00\x3a\x00\x02\x0c\x03\x00\x00\x00\x03\x00\x01\x00\x04\x00\x02\x00\x01\x04\x00\x02\x00\x04\x04\x00\x02\x00\x05\x04\x00\x02\x00\x06\x04\x00\x02\x00\x07\x04\x00\x02\x00\x08\x04\x00\x02\x00\x09\x04\x00\x02\x00\x0c\x04\x00\x04\x00\x01\x03\x00\x05\x00\xfe",
                "\x55\x05\x00\x3c\x00\x03\x00\xbc",
                "\x55\x04\x00\x14\x00\x01\xe7",
                "\x55\x06\x00\x02\x00\x03\x00\x15\xe0",
                "\x55\x06\x00\x02\x00\x03\x00\x15\xe0",
                "\x55\x06\x00\x02\x00\x03\x00\x15\xe0",
                "\x55\x06\x00\x02\x00\x03\x00\x15\xe0",
                "\x55\x06\x00\x02\x00\x03\x00\x15\xe0",
                "\x55\x06\x00\x02\x00\x03\x00\x15\xe0",
                "\x55\x06\x00\x02\x00\x03\x00\x15\xe0",
                "\x55\x05\x00\x16\x00\x03\x00\xe2",
                "\x55\x19\x00\x17\x00\x03\x47\x0a\x0a\x09\x0c\xd3\x12\xcc\x18\x1f\xaf\xa8\xa4\xb1\x1a\xf1\x2f\x8e\x24\xde\x01\xfe",
                "\x55\x05\x00\x19\x00\x03\x00\xdf",
                "\x55\x06\x00\x02\x00\x04\x00\x64\x90",
                "\x55\x07\x00\x3f\x00\x02\x00\x01\x01\xb6"]

# Before you may contact via port 3 for control, you must first contact via port 10.
initialSequnce = [("\x55\x0f\x00\x43\x00\x03\x00\x01\x0a\x30\x30\x30\x30\x30\x46\x30\x0d\x2d","\x55\x06\x00\x02\x00\x05\x00\x42\xb1")]

host = "00:11:67:E3:B9:09"

# They seem to have hardcoded the RFComm port.
# From our bruteforce, we get that we have to connect to port 10 first, disconnect (sock.close()),
# then the actual interaction will happen on port 3.
# After, most of the time, we can directly connect to port 3.
port = 3
print("---- Connecting to {} port {}".format(host, port))

sock = BluetoothSocket( RFCOMM )
sock.connect((host, port))

recv = rx()

print("---- Sending handshakeMaybe")
for i in handshakeMaybe:
    tx(i)
    # For some sequence, the cannon doesn't send back anything. We will just skip rx() for those.
    if(i in ["\x55\x05\x00\x16\x00\x03\x00\xe2", "\x55\x06\x00\x02\x00\x04\x00\x64\x90", "\x55\x05\x00\x3c\x00\x03\x00\xbc"]):
        continue
    recv = rx()

print("---- Sending sequences")
for (i, j) in initialSequnce:
    tx(i)
    recv = rx()
    recv = rx()
    tx(j)
    time.sleep(0.3)

print("---- Now accepting command:")
print("-- left()")
print("-- right()")
print("-- up()")
print("-- down()")
print("-- fire()")