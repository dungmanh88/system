#!/usr/bin/python

import socket
host = "0.0.0.0"
port = 60000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

print "Server listening..."

while True:
    conn, addr = s.accept()
    print "Got connection from ", addr
    data = conn.recv(1024)

    filename = "test.txt"
    f = open(filename, "rb")
    d = f.read(1024)
    while d:
        conn.send(d)
        d = f.read(1024)
    f.close()
    print "Done sending"
    conn.send("Thank you")
    conn.close()
