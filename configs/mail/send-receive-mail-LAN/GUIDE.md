# Requirement
```
Centos 7
systemctl stop firewalld
systemctl disable firewalld
disable selinux
```

# Install
```
yum -y install dovecot
systemctl enable dovecot
yum --enablerepo=centosplus install postfix -y
systemctl enable postfix
yum install net-tools telnet mailx -y
```

# Config hostname
```
hostnamectl set-hostname mail.lab.com
```

# Config postfix
/etc/postfix/main.cf
```
...
#home_mailbox = Mailbox
home_mailbox = Maildir/
...
```

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

systemctl restart postfix

# Config user
/etc/login.defs
```
...
#QMAIL_DIR      Maildir
#MAIL_DIR       /var/spool/mail
#MAIL_FILE      .mail
MAIL_FILE       Maildir/
...
```

/etc/profile.d/mailenv.sh
```
MAIL=$HOME/Maildir/
```

/etc/default/useradd
```
# useradd defaults file
GROUP=100
HOME=/home
INACTIVE=-1
EXPIRE=
SHELL=/bin/bash
SKEL=/etc/skel
CREATE_MAIL_SPOOL=no
```

Create user
```
useradd adam
useradd brian
passwd adam - 12345678
passwd brian - 12345678
```

# Create Maildir (also check send/receive mail internal)
Maildir structure:
```
Maildir structure
cur new tmp

cur: recevied mail
new: sending mail until mail is sent
```
```
su - adam
[adam@mail ~]$ mailx brian
Subject: test again
hello i am testing mail local again
.
EOT

su - brian
mailx
& 8
Message  8:
From adam@mail.lab.com Sun Jul 30 08:48:16 2017
Return-Path: <adam@mail.lab.com>
X-Original-To: brian
Delivered-To: brian@mail.lab.com
Date: Sun, 30 Jul 2017 08:48:16 +0000
To: brian@mail.lab.com
Subject: test again
User-Agent: Heirloom mailx 12.5 7/5/10
Content-Type: text/plain; charset=us-ascii
From: adam@mail.lab.com
Status: R

hello i am testing mail local again

& r
To: adam@mail.lab.com brian@mail.lab.com
Subject: Re: test again

adam@mail.lab.com wrote:

> hello i am testing mail local again
done
.
EOT
```

# Config postfix MSA
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

# Postfix smtp-auth
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

# Config nameserver
Review configs/bind/create-zone

/etc/resolv.conf
```
nameserver xx.xx.xx.xx # because I am config mail mx on this server. All client and mail server must use this nameserver.
```

# Config thunderbird
```
Use thunderbird

Mail account setup
- john
- john@lab.com
- 12345678

Manual config
- Incomming IMAP mail.lab.com 143 STARTTLS Normal Passwd
- Outgoing SMTP mail.lab.com 587 STARTTLS Normal Passwd
Username incomming brian, outgoing brian

Done
```
