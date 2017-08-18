# Config postfix MSA (listen on 587)
/etc/postfix/master.cf
```
...
submission inet n       -       n       -       -       smtpd
  -o syslog_name=postfix/submission
  -o smtpd_tls_security_level=encrypt
  -o smtpd_sasl_auth_enable=yes
  -o smtpd_reject_unlisted_recipient=no
#  -o smtpd_client_restrictions=$mua_client_restrictions
#  -o smtpd_helo_restrictions=$mua_helo_restrictions
#  -o smtpd_sender_restrictions=$mua_sender_restrictions
  -o smtpd_recipient_restrictions=permit_sasl_authenticated,reject
  -o milter_macro_daemon_name=ORIGINATING
...
```
systemctl restart postfix

# Config SMTPS (listen on 465)
/etc/postfix/master.cf
```
smtps     inet  n       -       n       -       -       smtpd
  -o syslog_name=postfix/smtps
  -o smtpd_tls_wrappermode=yes
  -o smtpd_sasl_auth_enable=yes
```

# Config postfix TLS

## Gencert
```
openssl req -new -x509 -days 3650 -nodes -out /etc/pki/tls/certs/postfix.pem -keyout /etc/pki/tls/private/postfix.key

openssl dhparam -out /etc/pki/tls/private/postfix.dh.param.tmp 1024
mv /etc/pki/tls/private/postfix.dh.param.tmp  /etc/pki/tls/private/postfix.dh.param
```

## Config postfix support TLS
/etc/postfix/main.cf
```
...
smtp_use_tls = yes
smtpd_use_tls = yes
smtpd_tls_security_level = encrypt
smtpd_tls_auth_only = yes
smtp_tls_note_starttls_offer = yes
smtpd_tls_key_file = /etc/pki/tls/private/postfix.key
smtpd_tls_cert_file = /etc/pki/tls/certs/postfix.pem
smtpd_tls_dh1024_param_file = /etc/pki/tls/private/postfix.dh.param
smtp_tls_CAfile = /etc/pki/tls/certs/ca-bundle.crt
smtpd_tls_loglevel = 1
smtpd_tls_session_cache_timeout = 3600s
smtpd_tls_session_cache_database = btree:/var/lib/postfix/smtpd_tls_cache
tls_random_source = dev:/dev/urandom

smtpd_tls_mandatory_protocols = !SSLv2, !SSLv3
smtpd_tls_protocols = !SSLv2, !SSLv3
smtp_tls_mandatory_protocols = !SSLv2, !SSLv3
smtp_tls_protocols = !SSLv2, !SSLv3

smtp_tls_exclude_ciphers = EXP, MEDIUM, LOW, DES, 3DES, SSLv2
smtpd_tls_exclude_ciphers = EXP, MEDIUM, LOW, DES, 3DES, SSLv2

tls_high_cipherlist = kEECDH:+kEECDH+SHA:kEDH:+kEDH+SHA:+kEDH+CAMELLIA:kECDH:+kECDH+SHA:kRSA:+kRSA+SHA:+kRSA+CAMELLIA:!aNULL:!eNULL:!SSLv2:!RC4:!MD5:!DES:!EXP:!SEED:!IDEA:!3DES
tls_medium_cipherlist = kEECDH:+kEECDH+SHA:kEDH:+kEDH+SHA:+kEDH+CAMELLIA:kECDH:+kECDH+SHA:kRSA:+kRSA+SHA:+kRSA+CAMELLIA:!aNULL:!eNULL:!SSLv2:!MD5:!DES:!EXP:!SEED:!IDEA:!3DES

smtp_tls_ciphers = high
smtpd_tls_ciphers = high
```
systemctl restart postfix

# Config dovecot TLS

/etc/dovecot/conf.d/10-ssl.conf
```
ssl = required
ssl_cert = </etc/pki/dovecot/certs/dovecot.pem
ssl_key = </etc/pki/dovecot/private/dovecot.pem
```


openssl s_client -connect localhost:smtp -starttls smtp
or
openssl s_client -connect mail.lab.local:smtp -starttls smtp

```
openssl s_client -connect mail.lab.local:995
...
---
+OK Dovecot ready.
user adam
+OK
pass 12345678
+OK Logged in.
```

Or use STARTTLS on POP3/IMAP
```
openssl s_client  -connect mail.lab.local:110 -starttls pop3
openssl s_client  -connect mail.lab.local:143 -starttls imap
```
