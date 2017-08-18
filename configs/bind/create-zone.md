# Requirement
```
Centos 7
systemctl stop firewalld
systemctl disable firewalld
disable selinux
```

# Install
```
yum -y install bind bind-utils
systemctl enable named
```

# Config named.conf
/etc/named.conf
```
options {
        listen-on port 53 { 127.0.0.1; any; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        allow-query     { localhost; any; };

        /*
         - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.
         - If you are building a RECURSIVE (caching) DNS server, you need to enable
           recursion.
         - If your recursive DNS server has a public IP address, you MUST enable access
           control to limit queries to your legitimate users. Failing to do so will
           cause your server to become part of large scale DNS amplification
           attacks. Implementing BCP38 within your network would greatly
           reduce such attack surface
        */
        recursion yes;

        dnssec-enable no;
        dnssec-validation no;

        /* Path to ISC DLV key */
        bindkeys-file "/etc/named.iscdlv.key";

        managed-keys-directory "/var/named/dynamic";

        pid-file "/run/named/named.pid";
        session-keyfile "/run/named/session.key";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "." IN {
        type hint;
        file "named.ca";
};

zone "lab.local" IN {
        type master;
        file "lab.local";
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```

systemctl restart named

# Config zone
/var/named/lab.local
```
$TTL 2d
$ORIGIN lab.local.
@       IN      SOA     ns1.lab.local. admin.lab.local. (
                              2017022702         ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL

@ IN NS ns1.lab.local.
@ IN MX 0 mail.lab.local.

ns1 IN A xx.xx.xx.xx
mail IN A yy.yy.yy.yy
```

systemctl restart named
