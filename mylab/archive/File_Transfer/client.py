#!/usr/bin/python

import socket, sys

if (len(sys.argv) < 3):
    print "Use client.py host port"
    sys.exit()
host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send("Hello server!!!")

with open("received_file", "wb") as f:
    while True:
        print "Receiving data"
        data = s.recv(1024)
        if not data:
            break
        f.write(data)
f.close()
print "Get the file successfully"
s.close()
print "Close connection"

