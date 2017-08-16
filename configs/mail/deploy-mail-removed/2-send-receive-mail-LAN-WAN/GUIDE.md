# Config postfix
/etc/postfix/main.cf

```
...
#myhostname = host.domain.tld
#myhostname = virtual.domain.tld
myhostname = mail.lab.com
...
#mydomain = domain.tld
mydomain = lab.com
...
#myorigin = $myhostname
myorigin = $mydomain
...
inet_interfaces = all
#inet_interfaces = $myhostname
#inet_interfaces = $myhostname, localhost
#inet_interfaces = localhost
...
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
...
#mynetworks_style = class
mynetworks_style = subnet
#mynetworks_style = host
...
relay_domains =
```

# Config nameserver
Review configs/bind/create-zone

/etc/resolv.conf
```
nameserver xx.xx.xx.xx # because I am config mail mx on this server. All client and mail server must use this nameserver.
```
