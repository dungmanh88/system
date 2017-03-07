# Get pic network interface
```
lspci | grep -i Network
lspci | grep -i ethernet
```

# Which physical interface is using
```
lspci | grep -i Network
00:19.0 Ethernet controller: Intel Corporation 82579LM Gigabit Network Connection (rev 05)
02:00.0 Ethernet controller: Intel Corporation 82574L Gigabit Network Connection

cd /sys/bus/pci/devices

NOTE 00:19.0

cd 0000\:00\:19.0/net
ls
eth0
-> 82579LM tương ứng với eth0
```

# Check status network
```
ethtool eth0
```
