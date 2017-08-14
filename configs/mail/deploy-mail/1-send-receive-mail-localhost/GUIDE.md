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
yum install net-tools telnet mailx -y
```

systemctl restart postfix

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
