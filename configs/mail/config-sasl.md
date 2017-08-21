https://serverfault.com/questions/691795/how-to-force-postfix-smtp-to-use-auth-sasl-and-reject-anonymous-connections

/etc/dovecot/conf.d/10-auth.conf
```
...
disable_plaintext_auth = no
auth_mechanisms = plain login
#!include auth-system.conf.ext
!include auth-sql.conf.ext
...
```

/etc/dovecot/conf.d/auth-sql.conf.ext
```
passdb {
  driver = sql
  args = /etc/dovecot/dovecot-sql.conf.ext
}
userdb {
  driver = sql
  args = /etc/dovecot/dovecot-sql.conf.ext
}
```

/etc/dovecot/dovecot-sql.conf.ext
```
connect = host=localhost dbname=mail user=postfix password=postfix
# Use either
driver = mysql
# Or
# driver = pgsql

# Default password scheme - change to match your Postfixadmin setting.
# depends on your $CONF['encrypt'] setting:
# md5crypt  -> MD5-CRYPT
# md5       -> PLAIN-MD5
# cleartext -> PLAIN
default_pass_scheme = MD5-CRYPT

# Query to retrieve password. user can be used to retrieve username in other
# formats also.

password_query = SELECT username AS user,password FROM mailbox WHERE username = '%u' AND active='1'

# Query to retrieve user information, note uid matches dovecot.conf AND Postfix virtual_uid_maps parameter.
user_query = SELECT maildir, 9999 AS uid, 9999 AS gid FROM mailbox WHERE username = '%u' AND active='1'


# MYSQL :
user_query = SELECT CONCAT('/var/vmail/mail/', maildir) AS home, 9999 AS uid, 9999 AS gid, CONCAT('*:bytes=', quota) AS quota_rule FROM mailbox WHERE username = '%u' AND active='1'
# PostgreSQL : (no Quota though) :
# user_query = SELECT '/var/vmail/mail/' || maildir AS home, 9999 as uid, 9999 as gid FROM mailbox WHERE username = '%u' AND active = '1'
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
smtpd_client_restrictions = permit_sasl_authenticated, reject
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_auth_enable = yes
```

systemctl restart dovecot
systemctl restart postfix


```
[root@mail private]# telnet localhost 25
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
220 mail.lab.local ESMTP Postfix
helo 1
250 mail.lab.local
mail from: test@abc.com
250 2.1.0 Ok
rcpt to: adam@lab.local
554 5.7.1 <localhost[127.0.0.1]>: Client host rejected: Access denied
^]
```

```
hello:> telnet remote_IP 25
Escape character is '^]'.
220 mail.lab.local ESMTP Postfix
helo 1
250 mail.lab.local
mail from: test@abc.com
250 2.1.0 Ok
rcpt to: adam@lab.local
554 5.7.1 <unknown[hidden_ip]>: Client host rejected: Access denied
^]
```

```
echo -ne "\000adam\000abc@123" | openssl base64
AGFkYW0AYWJjQDEyMw==

hello:> telnet remote_IP 25
Escape character is '^]'.
220 mail.lab.local ESMTP Postfix
ehlo
501 Syntax: EHLO hostname
ehlo 1
250-mail.lab.local
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-AUTH PLAIN LOGIN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250 DSN
auth plain AGFkYW0AYWJjQDEyMw==
235 2.7.0 Authentication successful
mail from: test@abc.com
250 2.1.0 Ok
rcpt to: adam@lab.local
250 2.1.5 Ok
data
354 End data with <CR><LF>.<CR><LF>
subject: sasl successfully
yeah!!!
.

250 2.0.0 Ok: queued as A2CE3100DABA5
```

```
[adam@mail ~]$ mailx
Heirloom Mail version 12.5 7/5/10.  Type ? for help.
"/home/adam/Maildir/": 2 messages 1 new 2 unread
 U  1 abc@lab.local           Mon Aug 14 22:41  13/400   "this is demo mail"
>N  2 test@abc.com          Tue Aug 15 11:54  10/278   "sasl successfully"
```
