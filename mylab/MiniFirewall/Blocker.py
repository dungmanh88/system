import sys
import time
import iptc
import os
import socket

IN_INF = "wlp3s0"

if len(sys.argv) != 2:
    print "Usage %s unique_ip_by_filter_str_file" % sys.argv[0]
    sys.exit(1)

input_file = sys.argv[1]
if str(type(input_file)) != "<type 'str'>":
    print "Casting error"
    sys.exit(1)

input_file = input_file.strip()
if len(input_file) == 0:
    print "Usage %s unique_ip_by_filter_str_file" % sys.argv[0]
    sys.exit(1)

if os.getuid() != 0:
    print "You need sudo permission"
    sys.exit(1)

block_list = {}

def block_ip_by_iptables(ip):
    rule = iptc.Rule()
    rule.in_interface = IN_INF
    rule.src = str(ip).strip()
    rule.target = iptc.Target(rule, "DROP")
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    chain.insert_rule(rule)
    print "Blocked ip: %s" % ip

while True:
    with open(input_file, "r") as f:
        for ip in f:
            print "ip = %s" % ip
            try:
                if not block_list.__contains__(ip):
                    # block ip
                    block_list[ip] = True
                    block_ip_by_iptables(ip)
            except ValueError, error:
                print "Invalid ip %s" % error
                continue
    f.close()
    print "Total blocked ip: %d" % len(block_list)
    time.sleep(10)
