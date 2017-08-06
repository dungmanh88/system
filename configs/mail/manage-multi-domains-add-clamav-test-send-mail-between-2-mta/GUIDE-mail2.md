https://www.server-world.info/en/note?os=CentOS_7&p=mail&f=1

yum --enablerepo=centosplus install postfix -y

/etc/postfix/main.cf
```
queue_directory = /var/spool/postfix
command_directory = /usr/sbin
daemon_directory = /usr/libexec/postfix
data_directory = /var/lib/postfix
mail_owner = postfix
*myhostname = mail2.data.net
*mydomain = data.net
*myorigin = $mydomain
*inet_interfaces = all
inet_protocols = all
*mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
*mynetworks_style = subnet
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
*home_mailbox = Maildir/
*smtpd_banner = $myhostname ESMTP
sample_directory = /usr/share/doc/postfix-2.10.1/samples
readme_directory = /usr/share/doc/postfix-2.10.1/README_FILES
*message_size_limit = 10485760
*mailbox_size_limit = 1073741824
*smtpd_sasl_type = dovecot
*smtpd_sasl_path = private/auth
*smtpd_sasl_auth_enable = yes
*smtpd_sasl_security_options = noanonymous
*smtpd_sasl_local_domain = $myhostname
*smtpd_recipient_restrictions = permit_mynetworks,permit_auth_destination,permit_sasl_authenticated,reject
```

[root@mail2 ~]# systemctl restart postfix
[root@mail2 ~]# systemctl enable postfix

yum -y install dovecot

/etc/dovecot/dovecot.conf
```
protocols = imap pop3 lmtp
listen = *
```

/etc/dovecot/conf.d/10-auth.conf
```
disable_plaintext_auth = no
auth_mechanisms = plain login
```

/etc/dovecot/conf.d/10-mail.conf
```
mail_location = maildir:~/Maildir
```

/etc/dovecot/conf.d/10-master.conf
```
# Postfix smtp-auth
unix_listener /var/spool/postfix/private/auth {
  mode = 0666
  user = postfix
  group = postfix
}
```

/etc/dovecot/conf.d/10-ssl.conf
```
ssl = no
```

[root@mail2 ~]# systemctl restart dovecot
[root@mail2 ~]# systemctl enable dovecot

yum -y install mailx
echo 'export MAIL=$HOME/Maildir' >> /etc/profile

Test send/receive using postfix (I have stopped dovecot for the testcase)
similar to GUIDE-mail1.md

Configure domain name for data.net

Use email client like thunderbird

Use IMAP no SSL, normal passwd

By the way, for [Username] field, if you use OS user accounts, specify username,
but if you use virtual mailbox accounts, specify email-address for it.

Use SSL for Postfix and Dovecot

If you use SSL for Postfix, you must enable MSA function for Postfix (This is standard)
or use SMTPS (deprecated)

```
openssl req -new -x509 -days 3650 -nodes -out /etc/pki/tls/certs/postfix.pem -keyout /etc/pki/tls/private/postfix.key
```

Add to the end
/etc/postfix/main.cf
```
smtpd_use_tls = yes
smtpd_tls_cert_file = /etc/pki/tls/certs/postfix.pem
smtpd_tls_key_file = /etc/pki/tls/private/postfix.key
smtpd_tls_session_cache_database = btree:/var/lib/postfix/smtpd_tls_cache
```
/etc/postfix/master.cf
```
smtps     inet  n       -       n       -       -       smtpd
  -o syslog_name=postfix/smtps
  -o smtpd_tls_wrappermode=yes
```

/etc/dovecot/conf.d/10-ssl.conf
```
ssl = required
ssl_cert = </etc/pki/dovecot/certs/dovecot.pem
ssl_key = </etc/pki/dovecot/private/dovecot.pem
```

[root@mail1 postfix]# systemctl restart dovecot
[root@mail1 postfix]# systemctl restart postfix

Edit mail client thunderbird

Use IMAPs 993, SSL/TLS, Normal Password (before: 143, No encrypt, Normal Password)
or IMAPs 143, STARTTLS, Normal Password
Use SMTPs 465, SSL/TLS, Normal Password (before: 25, No encrypt, Normal Password)
If you want SMTPs 587, STARTTLS, you must reconfig in /etc/postfix/master.cf
Confirm for self-sign for postfix and dovecot
