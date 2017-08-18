# Config dovecot SASL
/etc/dovecot/conf.d/10-auth.conf
```
...
auth_mechanisms = plain login
...
```

/etc/dovecot/conf.d/10-master.conf
```
...
#unix_listener auth-userdb {
  #mode = 0666
  #user =
  #group =
#}

# Postfix smtp-auth - dovecot will auth for smtp
unix_listener /var/spool/postfix/private/auth {
  mode = 0660
  user = postfix
  group = postfix
}
...
```

/etc/postfix/main.cf
```
...
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_auth_enable = yes
```

systemctl restart dovecot
systemctl restart postfix


passwd 12345678 is not compatible
change passwd to abc@1234
echo -ne "\000adam\000abc@1234" | openssl base64
AGFkYW0AYWJjQDEyMzQ=

openssl s_client -connect mail.lab.local:smtp -starttls smtp
```
...
250 DSN
ehlo lab.local
250-mail.lab.local
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-AUTH PLAIN LOGIN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250 DSN
AUTH PLAIN AGFkYW0AYWJjQDEyMzQ=
235 2.7.0 Authentication successful
...
```
