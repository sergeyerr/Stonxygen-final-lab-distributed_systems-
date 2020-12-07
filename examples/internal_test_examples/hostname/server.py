#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()
sock.bind(('', 9090))
while True:
    sock.listen(1)
    conn, addr = sock.accept()
    print(f'lol {addr}')
    conn.send(str.encode(f'connected: {addr}'))
conn.close()