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
  -o smtpd_reject_unlisted_recipient=no
#  -o smtpd_client_restrictions=$mua_client_restrictions
#  -o smtpd_helo_restrictions=$mua_helo_restrictions
#  -o smtpd_sender_restrictions=$mua_sender_restrictions
  -o smtpd_recipient_restrictions=permit_sasl_authenticated,reject
  -o milter_macro_daemon_name=ORIGINATING
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
- Setup more MTA
- Setup vmail account
- Setup more dovecot
- Metadata db is shared
- Data mailbox is shared
- Cert is re-use

# Deploy greylisting
```
yum -y install postgrey
systemctl enable postgrey
systemctl start postgrey
```
/etc/postfix/main.cf
```
smtpd_recipient_restrictions =
#        permit_mynetworks,
        reject_unauth_destination,
        check_policy_service unix:postgrey/socket,
        permit
```
/etc/sysconfig/postgrey
```
POSTGREY_OPTS="--delay=60"
```
systemctl restart postfix

# Deploy spamassasin + clamav + amavisd-new
```
yum -y install spamassassin spamass-milter spamass-milter-postfix && \
yum -y install clamav clamav-milter clamav-lib clamav-scanner clamav-scanner-systemd clamav-server clamav-server-systemd clamav-filesystem clamav-update clamav-milter-systemd clamav-data && \
yum -y install amavisd-new
```
https://www.ijs.si/software/amavisd/README.postfix.html
/etc/postfix/master.cf
```
...
amavisfeed unix    -       -       n        -      2     lmtp
    -o lmtp_data_done_timeout=1200
    -o lmtp_send_xforward_command=yes
    -o disable_dns_lookups=yes
    -o max_use=20

127.0.0.1:10025 inet n    -       n       -       -     smtpd
    -o content_filter=
    -o smtpd_delay_reject=no
    -o smtpd_client_restrictions=permit_mynetworks,reject
    -o smtpd_helo_restrictions=
    -o smtpd_sender_restrictions=
    -o smtpd_recipient_restrictions=permit_mynetworks,reject
    -o smtpd_data_restrictions=reject_unauth_pipelining
    -o smtpd_end_of_data_restrictions=
    -o smtpd_restriction_classes=
    -o mynetworks=127.0.0.0/8
    -o smtpd_error_sleep_time=0
    -o smtpd_soft_error_limit=1001
    -o smtpd_hard_error_limit=1000
    -o smtpd_client_connection_count_limit=0
    -o smtpd_client_connection_rate_limit=0
    -o receive_override_options=no_header_body_checks,no_unknown_recipient_checks,no_milters
    -o local_header_rewrite_clients=
    -o smtpd_tls_security_level=none
```

/etc/freshclam.conf
Comment Example line

/etc/sysconfig/fresclam
```
## When changing the periodicity of freshclam runs in the crontab,
## this value must be adjusted also. Its value is the timespan between
## two subsequent freshclam runs in minutes. E.g. for the default
##
## | 0 */3 * * *  ...
##
## crontab line, the value is 180 (minutes).
# FRESHCLAM_MOD=

## A predefined value for the delay in seconds. By default, the value is
## calculated by the 'hostid' program. This predefined value guarantees
## constant timespans of 3 hours between two subsequent freshclam runs.
##
## This option accepts two special values:
## 'disabled-warn'  ...  disables the automatic freshclam update and
##                         gives out a warning
## 'disabled'       ...  disables the automatic freshclam silently
# FRESHCLAM_DELAY=
```

freshclam
sa-update -D

/etc/postfix/main.cf
```
...
content_filter=amavisfeed:[127.0.0.1]:10024
```

systemctl enable amavisd && \
systemctl restart amavisd && \
systemctl enable spamassassin && \
systemctl restart spamassassin && \
systemctl restart postfix

Test amavisd
```
telnet localhost 10024
Trying ::1...
Connected to localhost.
Escape character is '^]'.
220 [::1] ESMTP amavisd-new service ready
EHLO localhost
250-[::1]
250-VRFY
250-PIPELINING
250-SIZE
250-ENHANCEDSTATUSCODES
250-8BITMIME
250-SMTPUTF8
250-DSN
250 XFORWARD NAME ADDR PORT PROTO HELO IDENT SOURCE
quit
221 2.0.0 [::1] amavisd-new closing transmission channel
Connection closed by foreign host.
```

Test the dedicated Postfix smtpd-daemon
```
telnet 127.0.0.1 10025
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
220 mail.lab.local ESMTP Postfix
EHLO localhost
250-mail.lab.local
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-STARTTLS
250-ENHANCEDSTATUSCODES
250-8BITMIME
250 DSN
quit
221 2.0.0 Bye
Connection closed by foreign host.
```

Test the new transport chain
```
telnet localhost 10024
Trying ::1...
Connected to localhost.
Escape character is '^]'.
220 [::1] ESMTP amavisd-new service ready
HELO localhost
250 [::1]
MAIL FROM: <>
250 2.1.0 Sender <> OK
RCPT TO: <postmaster>
250 2.1.5 Recipient <postmaster> OK
DATA
354 End data with <CR><LF>.<CR><LF>
this is a simple message
.
250 2.7.0 Ok, discarded, id=20465-02 - spam
```
Aug 22 02:40:07 mail amavis[20465]: (20465-02) Blocked SPAM {DiscardedOpenRelay,Quarantined}, [::1] <> -> <postmaster>, mail_id: Ng_ZTwmXVXKx, Hits: 7.853, size: 28, 38657 ms

cd /usr/share/doc/amavisd-new-2.11.0/test-messages/
perl -pe 's/./chr(ord($&)^255)/sge' <sample.tar.gz.compl | zcat | tar xvf -
$ sendmail -i your-address@example.com <sample-virus-simple.txt
$ sendmail -i your-address@example.com <sample-executable.txt (PASS)
$ sendmail -i your-address@example.com <sample-virus-nested.txt (PASS)
$ sendmail -i your-address@example.com <sample-nonspam.txt (PASS)
$ sendmail -i your-address@example.com <sample-spam-GTUBE-junk.txt
$ sendmail -i your-address@example.com <sample-spam-GTUBE-nojunk.txt
$ sendmail -i your-address@example.com <sample-spam.txt   # old sample (PASS)
$ sendmail -i your-address@example.com <sample-42-mail-bomb.txt
$ sendmail -i your-address@example.com <sample-badh.txt

https://easyengine.io/tutorials/mail/server/testing/antivirus/
wget https://secure.eicar.org/eicar.com.txt
sendmail -i dungnm@lab.local < eicar.com.txt

# Deploy SPF
https://www.linode.com/docs/email/postfix/configure-spf-and-dkim-in-postfix-on-debian-8
Config named lab.local-zone
yum -y install pypolicyd-spf
useradd -d /dev/null -s /sbin/nologin -c "policyd spf" policyd-spf
/etc/python-policyd-spf/policyd-spf.conf
```
#  For a fully commented sample config file see policyd-spf.conf.commented

debugLevel = 1
defaultSeedOnly = 1

Mail_From_reject = Fail
HELO_reject = SPF_Not_Pass

PermError_reject = True
TempError_Defer = True

skip_addresses = 127.0.0.0/8,::ffff:127.0.0.0/104,::1
```
/etc/postfix/master.cf
```
policyd-spf  unix  -       n       n       -       0       spawn
    user=policyd-spf argv=/usr/libexec/postfix/policyd-spf
```

/etc/postfix/main.cf
```
smtpd_recipient_restrictions =
        reject_unauth_destination,
        check_policy_service unix:postgrey/socket,
        check_policy_service unix:private/policyd-spf,  ### add new
        permit

policyd-spf_time_limit = 3600
```
systemctl restart postfix
# Deploy DKIM
https://www.rosehosting.com/blog/how-to-install-and-integrate-opendkim-with-postfix-on-a-centos-6-vps/
```
yum -y install opendkim
```

mv /etc/opendkim.conf /etc/opendkim.conf.orig
/etc/opendkim.conf
```
LogWhy                  Yes
Syslog                  Yes
SyslogSuccess           Yes
Mode                    sv
Domain                  lab.local
Canonicalization        relaxed/simple
ExternalIgnoreList      refile:/etc/opendkim/trusted.hosts
InternalHosts           refile:/etc/opendkim/trusted.hosts
KeyTable                refile:/etc/opendkim/key.table
SigningTable            refile:/etc/opendkim/signing.table
SignatureAlgorithm      rsa-sha256
Socket                  inet:8891@localhost
PidFile                 /var/run/opendkim/opendkim.pid
UMask                   022
UserID                  opendkim:opendkim
TemporaryDirectory      /var/tmp
On-BadSignature         reject
On-SignatureError       reject
RequiredHeaders         Yes
On-KeyNotFound          reject
```

mkdir -p /etc/opendkim/keys/lab.local
opendkim-genkey -D /etc/opendkim/keys/lab.local/ -d lab.local -s default
chown -R opendkim: /etc/opendkim/keys/lab.local/
mv /etc/opendkim/keys/lab.local/default.private /etc/opendkim/keys/lab.local/default

/etc/opendkim/signing.table
```
*@lab.local default._domainkey.lab.local
```
/etc/opendkim/key.table
```
default._domainkey.lab.local lab.local:default:/etc/opendkim/keys/lab.local/default
```
/etc/opendkim/trusted.hosts
```
127.0.0.1
```

/etc/postfix/main.cf - before content_filter
after the smtpd_recipient_restrictions entry
```
smtpd_milters           = inet:127.0.0.1:8891
non_smtpd_milters       = $smtpd_milters
milter_default_action   = accept
#milter_protocol         = 2
milter_protocol         = 6
```

systemctl restart opendkim && \
systemctl enable opendkim && \
systemctl restart postfix

configure dns
```
default._domainkey      IN      TXT     ( "v=DKIM1; k=rsa; "
          "p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDV5EbzBMBmHrgj48xrczO+qsad/NYOgUH9cCiBvEAhaha1trqf/cPkgEWmpq/94WOnPmE+utWr/VCB8+KXi5fZ05qDWO8ESRDUqa8rE7z8vwOTmk9S/OjtVQY3g5JTfWRlrAxv/BzbPHQ+G2qbPi3lPHxVMPPxZvKKiAQhFyhvQIDAQAB" )  ; ----- DKIM key default for lab.local
```
systemctl restart named
