```
myhostname = mail.lab.com
mydomain = lab.com
myorigin = $mydomain
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
# trust subnet
mynetworks_style = subnet
# not relay for any domain
relay_domains =
# by default:
# smtpd_relay_restrictions = permit_mynetworks,permit_sasl_authenticated,defer_unauth_destination
smtpd_relay_restrictions = permit_sasl_authenticated,defer_unauth_destination
```

```
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
220 mail.lab.com ESMTP Postfix
helo case2.lab.com
250 mail.lab.com
mail from: abc@lab.com
250 2.1.0 Ok
rcpt to: hidden@gmail.com
454 4.7.1 <hidden@gmail.com>: Relay access denied
```

```
[root@test3 ~]# telnet localhost 25
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
220 mail.lab.com ESMTP Postfix
helo case2.lab.com
250 mail.lab.com
mail from: abc@lab.com
250 2.1.0 Ok
rcpt to: joe@lab.com
550 5.1.1 <joe@lab.com>: Recipient address rejected: User unknown in local recipient table
```

```
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
220 mail.lab.com ESMTP Postfix
helo case2.lab.com
250 mail.lab.com
mail from: abc@lab.com
250 2.1.0 Ok
rcpt to: adam@lab.com
250 2.1.5 Ok
data
354 End data with <CR><LF>.<CR><LF>
subject: this is demo mail
demo
.
250 2.0.0 Ok: queued as A0D70100DABA5
```

```
[adam@mail ~]$ mailx
Heirloom Mail version 12.5 7/5/10.  Type ? for help.
"/home/adam/Maildir/": 1 message 1 new
>N  1 abc@lab.com           Mon Aug 14 22:41  13/400   "this is demo mail"
& 1
Message  1:
From abc@lab.com Mon Aug 14 22:41:46 2017
Return-Path: <abc@lab.com>
X-Original-To: adam@lab.com
Delivered-To: adam@lab.com
subject: this is demo mail
Date: Mon, 14 Aug 2017 22:41:46 +0700 (+07)
From: abc@lab.com
Status: R

demo

&
```
