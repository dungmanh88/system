#!/usr/bin/python

import socket, select, string, sys, traceback

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print "Usage telnet.py hostname port"
        sys.exit()
    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((host, port))
    except:
        print "Unable to connect"
#        traceback.print_exc()
        sys.exit()
    print "Connected to the host"

