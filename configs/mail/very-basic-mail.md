# Requirement
```
Centos 7
systemctl stop firewalld
systemctl disable firewalld
disable selinux
```

# Install
```
yum --enablerepo=centosplus install postfix -y
systemctl enable postfix
systemctl restart postfix
yum install net-tools telnet mailx -y
```

# Config hostname
```
hostnamectl set-hostname mail.lab.local
```

# Config postfix
/etc/postfix/main.cf
```
...
#home_mailbox = Mailbox
home_mailbox = Maildir/
...
```

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
From adam@mail.lab.local Sun Jul 30 08:48:16 2017
Return-Path: <adam@mail.lab.local>
X-Original-To: brian
Delivered-To: brian@mail.lab.local
Date: Sun, 30 Jul 2017 08:48:16 +0000
To: brian@mail.lab.local
Subject: test again
User-Agent: Heirloom mailx 12.5 7/5/10
Content-Type: text/plain; charset=us-ascii
From: adam@mail.lab.local
Status: R

hello i am testing mail local again

& r
To: adam@mail.lab.local brian@mail.lab.local
Subject: Re: test again

adam@mail.lab.local wrote:

> hello i am testing mail local again
done
.
EOT
```

You can send mail to google mail if you want.
But your mail will go into spam.
```
telnet localhost 25
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
220 test3.localdomain ESMTP Postfix
helo case1.lab.local
250 test3.localdomain
mail from: test@lab.local
250 2.1.0 Ok
rcpt to: hidden@gmail.com
250 2.1.5 Ok
data
354 End data with <CR><LF>.<CR><LF>
subject: this is a mail demo
this is just a demo
.
250 2.0.0 Ok: queued as D2453100DABA5
```
