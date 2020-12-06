#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("ip")
args = parser.parse_args()
print('connecting to', args.ip)

sock = socket.socket()
sock.connect((args.ip, 9090))

data = sock.recv(1024)
sock.close()

print(data)