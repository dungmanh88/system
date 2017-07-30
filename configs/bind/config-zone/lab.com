/var/named/lab.com
```
$TTL 2d
$ORIGIN lab.com.
@       IN      SOA     ns1.lab.com. admin.lab.com. (
                              2017022702         ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL

@ IN NS ns1.lab.com.
@ IN MX 0 mail.lab.com.

ns1 IN A xx.xx.xx.xx
mail IN A yy.yy.yy.yy
```
