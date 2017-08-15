http://www.iredmail.org/docs/allow.insecure.pop3.imap.smtp.connections.html
/etc/dovecot/conf.d/10-auth.conf
```
disable_plaintext_auth = no
```
/etc/dovecot/conf.d/10-ssl.conf
```
ssl = yes
```

```
hello:> telnet remote_IP 110
Escape character is '^]'.
+OK Dovecot ready.
user adam
+OK
pass abc@123
+OK Logged in.
list
+OK 1 messages:
1 411
.
quit
+OK Logging out.
Connection closed by foreign host.
```
