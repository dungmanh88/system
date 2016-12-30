#!/usr/bin/python

import socket, sys
MESSAGE = "ping"
msg=MESSAGE

if __name__ == "__main__":
    if(len(sys.argv) < 3 ):
        print "Use client.py host port"
        sys.exit()
    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while msg != "BYE":
        msg = raw_input()
        s.sendto(msg, (host, port))
        data, addr = s.recvfrom(1024)
        print "Client received: %s from %s" % (data, addr)
    print "Bye bye"


