# !/usr/bin/python3
# filename：SOCAT.py

import socket
import sys

SOCAT_PORT = 64335
BUFFERSIZE = 409600

# KALOS_HOST = '101.42.95.33'
KALOS_HOST = "www.kricto.cn"
# KALOS_HOST = '192.168.123.227'

# KALOS_HOST = '127.0.0.1'
KALOS_PORT = 64335


# get a socket
def get_asocket():

    # create socat object
    socat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socat.connect((KALOS_HOST, KALOS_PORT))

    return socat


def send(commandID, commandBody):
    socatclient = get_asocket()

    command = (commandID + "#" + commandBody).encode("utf-8")

    socatclient.send(command)

    rep = socatclient.recv(BUFFERSIZE)

    return str(rep, "utf-8")
