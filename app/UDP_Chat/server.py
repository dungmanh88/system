#!/usr/bin/python

import socket
SERVER="0.0.0.0"
PORT=321
if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((SERVER, PORT))
    while True:
        data, addr = s.recvfrom(1024)
        print "Server received %s from %s" % (data, addr)
        s.sendto("Echo " + data, addr)
