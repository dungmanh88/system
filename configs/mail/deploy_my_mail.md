# Requirement
- Use virtual account - done
- Prevent send mail outside my domain - done
- Don't relay anything - done
- Support multiple virtual domain
- Support postfixadmin - done
- Stack: dovecot + postfix + postfixadmin - done
- Support SASL to auth sending mail - done
- Support TLS/SSL for dovecot + postfix - done
- Support MSA (465+587) to get mail from client - done

# Prepare
```
Centos 7
systemctl stop firewalld
systemctl disable firewalld
disable selinux
```

# Install
```
yum -y install ntp
systemctl enable ntpd && \
systemctl restart ntpd
yum --enablerepo=centosplus install postfix -y
systemctl enable postfix && \
systemctl restart postfix
yum install net-tools telnet wget mailx -y
yum -y install dovecot dovecot-mysql
systemctl enable dovecot && \
systemctl restart dovecot
```

```
yum -y install epel-release

yum -y install mysql mariadb-server nginx php php-fpm php-mysql php-mbstring php-imap

systemctl start mariadb && \
systemctl enable mariadb && \
systemctl start nginx && \
systemctl enable nginx && \
systemctl start php-fpm && \
systemctl enable php-fpm

cd /tmp
wget https://downloads.sourceforge.net/project/postfixadmin/postfixadmin/postfixadmin-3.1/postfixadmin-3.1.tar.gz
tar xvzf postfixadmin-3.1.tar.gz
mv postfixadmin-3.1 postfixadmin
```

# Config hostname
```
hostnamectl set-hostname mail.lab.local
```

# Config virtual user
```
groupadd -g 9999 vmail
mkdir -p /var/vmail/mail
useradd -u 9999 -g vmail -d /var/vmail -s /sbin/nologin -c "Virtual Mail User" vmail
chown -R vmail:vmail /var/vmail
```

# Config database
```
CREATE DATABASE mail;
CREATE USER 'postfix'@'localhost' IDENTIFIED BY 'postfix';
GRANT ALL PRIVILEGES ON `mail` . * TO 'postfix'@'localhost';
CREATE USER 'postfixadmin'@'localhost' IDENTIFIED BY 'postfixadmin';
GRANT ALL PRIVILEGES ON `mail` . * TO 'postfixadmin'@'localhost';
```

# Config postfixadmin

postfixadmin/config.local.php
```
<?php
$CONF['database_type'] = 'mysqli';
$CONF['database_user'] = 'postfixadmin';
$CONF['database_password'] = 'postfixadmin';
$CONF['database_name'] = 'mail';

$CONF['configured'] = true;

$CONF['domain_path'] = 'YES';
$CONF['domain_in_mailbox'] = 'NO';

$CONF['used_quotas'] = 'YES';
$CONF['quota'] = 'YES';
?>
```

# Create templates_c in postfixadmin
```
cd postfixadmin
mkdir -p templates_c
chmod o+rwx templates_c/
```

# Config web
/etc/nginx/conf.d/postfixadmin.conf
```
server {

  index index.php index.html;
  server_name postfixadmin.lab.local www.postfixadmin.lab.local;
  error_log /var/log/nginx/postfixadmin.lab.local/error.log;
  client_max_body_size 20M;
  access_log /var/log/nginx/postfixadmin.lab.local/access.log;
  root /data/www/html/postfixadmin;
  listen 80;

  location / {
  }

  location ~ \.php$ {
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include /etc/nginx/fastcgi_params;
    fastcgi_index index.php;
    fastcgi_pass 127.0.0.1:9000;
  }
}
```

```
mkdir -p /var/log/nginx/postfixadmin.lab.local && \
mkdir -p /data/www/html/
mv /tmp/postfixadmin /data/www/html/
chown vmail:vmail -R /data/www/html/postfixadmin


systemctl restart nginx && \
systemctl restart php-fpm
```

# Create admin user
```
http://postfixadmin.lab.local/setup.php
Create setup password
```
NOTICE:
```
If you want to use the password you entered as setup password, edit config.inc.php or config.local.php and set
$CONF['setup_password'] = 'xyz...';
```
Add
```
$CONF['setup_password'] = 'xyz...';
```
into postfixadmin/config.local.php

email admin must be a email in domain lab.local
admin (such as admin@lab.local) - this account is a isolated account for postfixadmin management (not email account)

After creating one admin account, you should remove file setup.php or rename to setup.php.orig

# Config postfix
/etc/postfix/main.cf
```
queue_directory = /var/spool/postfix
command_directory = /usr/sbin
daemon_directory = /usr/libexec/postfix
data_directory = /var/lib/postfix

mail_owner = postfix
myhostname = mail.lab.local
mydomain = lab.local
myorigin = $mydomain
inet_interfaces = all
inet_protocols = ipv4
### remove $mydomain from mydestination
mydestination = $myhostname, localhost.$mydomain, localhost

unknown_local_recipient_reject_code = 550

mynetworks_style = subnet
relay_domains = <domain list separate by comma>

alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases

home_mailbox = Maildir/

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

virtual_mailbox_base = /var/vmail/mail
virtual_uid_maps = static:9999
virtual_gid_maps = static:9999

virtual_mailbox_domains = proxy:mysql:/etc/postfix/sql/mysql_virtual_domains_maps.cf

virtual_mailbox_maps =
   proxy:mysql:/etc/postfix/sql/mysql_virtual_mailbox_maps.cf,
   proxy:mysql:/etc/postfix/sql/mysql_virtual_alias_domain_mailbox_maps.cf

virtual_alias_maps =
   proxy:mysql:/etc/postfix/sql/mysql_virtual_alias_maps.cf,
   proxy:mysql:/etc/postfix/sql/mysql_virtual_alias_domain_maps.cf,
   proxy:mysql:/etc/postfix/sql/mysql_virtual_alias_domain_catchall_maps.cf

smtpd_relay_restrictions = permit_auth_destination, defer_unauth_destination

smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_auth_enable = yes
```

mkdir -p /etc/postfix/sql

/etc/postfix/sql/mysql_virtual_alias_maps.cf
```
user = postfix
password = postfix
hosts = localhost
dbname = mail
query = SELECT goto FROM alias WHERE address='%s' AND active = '1'
#expansion_limit = 100
```

/etc/postfix/sql/mysql_virtual_alias_domain_maps.cf
```
user = postfix
password = postfix
hosts = localhost
dbname = mail
query = SELECT goto FROM alias,alias_domain WHERE alias_domain.alias_domain = '%d' and alias.address = CONCAT('%u', '@', alias_domain.target_domain) AND alias.active = 1 AND alias_domain.active='1'
```

/etc/postfix/sql/mysql_virtual_alias_domain_catchall_maps.cf
```
# handles catch-all settings of target-domain
user = postfix
password = postfix
hosts = localhost
dbname = mail
query  = SELECT goto FROM alias,alias_domain WHERE alias_domain.alias_domain = '%d' and alias.address = CONCAT('@', alias_domain.target_domain) AND alias.active = 1 AND alias_domain.active='1'
```

/etc/postfix/sql/mysql_virtual_domains_maps.cf
```
user = postfix
password = postfix
hosts = localhost
dbname = mail
query          = SELECT domain FROM domain WHERE domain='%s' AND active = '1'
#query          = SELECT domain FROM domain WHERE domain='%s'
#optional query to use when relaying for backup MX
#query           = SELECT domain FROM domain WHERE domain='%s' AND backupmx = '0' AND active = '1'
#expansion_limit = 100
```

/etc/postfix/sql/mysql_virtual_mailbox_maps.cf
```
user = postfix
password = postfix
hosts = localhost
dbname = mail
query           = SELECT maildir FROM mailbox WHERE username='%s' AND active = '1'
#expansion_limit = 100
```

/etc/postfix/sql/mysql_virtual_alias_domain_mailbox_maps.cf
```
user = postfix
password = postfix
hosts = localhost
dbname = mail
query = SELECT maildir FROM mailbox,alias_domain WHERE alias_domain.alias_domain = '%d' and mailbox.username = CONCAT('%u', '@', alias_domain.target_domain) AND mailbox.active = 1 AND alias_domain.active='1'
```

/etc/postfix/master.cf
```
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

smtps     inet  n       -       n       -       -       smtpd
  -o syslog_name=postfix/smtps
  -o smtpd_tls_wrappermode=yes
  -o smtpd_sasl_auth_enable=yes
#  -o smtpd_reject_unlisted_recipient=no
#  -o smtpd_client_restrictions=$mua_client_restrictions
#  -o smtpd_helo_restrictions=$mua_helo_restrictions
#  -o smtpd_sender_restrictions=$mua_sender_restrictions
  -o smtpd_recipient_restrictions=permit_sasl_authenticated,reject
#  -o milter_macro_daemon_name=ORIGINATING
```

```
openssl req -new -x509 -days 3650 -nodes -out /etc/pki/tls/certs/postfix.pem -keyout /etc/pki/tls/private/postfix.key
openssl dhparam -out /etc/pki/tls/private/postfix.dh.param.tmp 1024
mv /etc/pki/tls/private/postfix.dh.param.tmp  /etc/pki/tls/private/postfix.dh.param
```

# Config dovecot

/etc/dovecot/dovecot.conf
```
protocols = imap pop3
!include conf.d/*.conf
```

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

/etc/dovecot/conf.d/10-master.conf
```
...
service auth {
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
  user = dovecot
}

service auth-worker {
  user = vmail
}
...
```

/etc/dovecot/conf.d/10-ssl.conf
```
ssl = required
ssl_cert = </etc/pki/dovecot/certs/dovecot.pem
ssl_key = </etc/pki/dovecot/private/dovecot.pem
```

/etc/dovecot/conf.d/10-logging.conf
```
auth_debug = yes
auth_debug_passwords = yes
```

/etc/dovecot/conf.d/10-mail.conf
```
mail_location = maildir:/var/vmail/mail/%d/%n
namespace inbox {
  inbox = yes
}
mail_uid = 9999
mail_gid = 9999
mail_privileged_group = vmail
first_valid_uid = 9999
last_valid_uid = 9999
first_valid_gid = 9999
last_valid_gid = 9999
mbox_write_locks = fcntl
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

```
chown -R vmail:dovecot /etc/dovecot
chmod -R o-rwx /etc/dovecot
```

```
dovecot -n
auth_debug = yes
auth_debug_passwords = yes
auth_mechanisms = plain login
disable_plaintext_auth = no
first_valid_gid = 9999
first_valid_uid = 9999
last_valid_gid = 9999
last_valid_uid = 9999
mail_gid = 9999
mail_location = maildir:/var/vmail/mail/%d/%n
mail_privileged_group = vmail
mail_uid = 9999
mbox_write_locks = fcntl
namespace inbox {
  inbox = yes
  location =
  mailbox Drafts {
    special_use = \Drafts
  }
  mailbox Junk {
    special_use = \Junk
  }
  mailbox Sent {
    special_use = \Sent
  }
  mailbox "Sent Messages" {
    special_use = \Sent
  }
  mailbox Trash {
    special_use = \Trash
  }
  prefix =
}
passdb {
  args = /etc/dovecot/dovecot-sql.conf.ext
  driver = sql
}
protocols = imap pop3
service auth-worker {
  user = vmail
}
service auth {
  unix_listener /var/spool/postfix/private/auth {
    group = postfix
    mode = 0660
    user = postfix
  }
  user = dovecot
}
ssl = required
ssl_cert = </etc/pki/dovecot/certs/dovecot.pem
ssl_key = </etc/pki/dovecot/private/dovecot.pem
userdb {
  args = /etc/dovecot/dovecot-sql.conf.ext
  driver = sql
}
```

systemctl restart dovecot && \
systemctl restart postfix

# Test
Add lab.local domain into postfixadmin.lab.local
Add some virtual mailbox via postfixadmin.lab.local such as dungnm, bot (passwd abc@123)

```
echo -ne "\000dungnm@lab.local\000abc@123" | openssl base64
<something>
echo -ne "\000bot@lab.local\000abc@123" | openssl base64
<something1>
```

openssl s_client -connect localhost:smtp -starttls smtp
or
openssl s_client -connect mail.lab.local:smtp -starttls smtp
```
ehlo lab.local
auth plain <something>
235 2.7.0 Authentication successful
mail from: dungnm@lab.local
250 2.1.0 Ok
rcpt to: <hidden>@gmail.com
454 4.7.1 <<hidden>@gmail.com>: Relay access denied
rcpt to: bot@lab.local
250 2.1.5 Ok
data
354 End data with <CR><LF>.<CR><LF>
subject: hello bot
hello bot, this is mail demo
.
250 2.0.0 Ok: queued as 541476E52E
```
**Send between accounts in same mail server, you don't need DNS**

telnet localhost 25 (if you don't use TLS/SSL)
```
ehlo lab.local
AUTH PLAIN <something>
...
```
openssl s_client  -connect localhost:110 -starttls pop3
or
openssl s_client  -connect mail.lab.local:110 -starttls pop3
```
+OK Dovecot ready.
auth plain <something1>
+OK Logged in.
list
+OK 1 messages:
1 423
.
retr 1
+OK 423 octets
...
Date: Fri, 18 Aug 2017 09:35:46 +0700 (ICT)
From: dungnm@lab.local

hello bot, this is mail demo
```
telnet localhost 110 (if you don't use TLS/SSL)
```
user bot@lab.local
pass abc@123
...
```

openssl s_client  -connect localhost:143 -starttls imap
```
a login bot@lab.local abc@123
b select inbox
* FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
* OK [PERMANENTFLAGS (\Answered \Flagged \Deleted \Seen \Draft \*)] Flags permitted.
* 1 EXISTS
* 0 RECENT
* OK [UIDVALIDITY 1503024394] UIDs valid
* OK [UIDNEXT 2] Predicted next UID
b OK [READ-WRITE] Select completed (0.000 secs).

```
or
openssl s_client  -connect mail.lab.local:143 -starttls imap
telnet localhost 143 (if you don't use TLS/SSL)
```
a login bot@lab.local abc@123
b select inbox
c logout
```

Add more virtual domain lab.vip
Try to send/receive between account belong different domain - done
**Send between accounts in same mail server belong different domain that mail service manage, you don't need DNS**

Config my mail server using my dns via /etc/resolv.conf

# High availibility
- You just install more MTA
- Setup vmail account
- Setup SASL implementation + mail_location
- Metadata db is shared
- Data mailbox is shared
- Cert is re-use
