yum -y install dovecot
systemctl enable dovecot

passwd adam
passwd brian

# check locally
```
telnet localhost pop3
Trying ::1...
Connected to localhost.
Escape character is '^]'.
+OK Dovecot ready.
user adam
+OK
pass 12345678
+OK Logged in.
list
+OK 4 messages:
1 852
2 989
3 1124
4 736
.
```

```
telnet localhost imap
Trying ::1...
Connected to localhost.
Escape character is '^]'.
* OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE STARTTLS AUTH=PLAIN AUTH=LOGIN] Dovecot ready.
a login adam 12345678
a OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE SORT SORT=DISPLAY THREAD=REFERENCES THREAD=REFS THREAD=ORDEREDSUBJECT MULTIAPPEND URL-PARTIAL CATENATE UNSELECT CHILDREN NAMESPACE UIDPLUS LIST-EXTENDED I18NLEVEL=1 CONDSTORE QRESYNC ESEARCH ESORT SEARCHRES WITHIN CONTEXT=SEARCH LIST-STATUS SPECIAL-USE BINARY MOVE] Logged in
b select inbox
* FLAGS (\Answered \Flagged \Deleted \Seen \Draft)
* OK [PERMANENTFLAGS (\Answered \Flagged \Deleted \Seen \Draft \*)] Flags permitted.
* 4 EXISTS
* 0 RECENT
* OK [UNSEEN 4] First unseen.
* OK [UIDVALIDITY 1501386677] UIDs valid
* OK [UIDNEXT 5] Predicted next UID
b OK [READ-WRITE] Select completed (0.000 secs).
c logout
* BYE Logging out
```

# check external
*Impossible to connect via POP3, IMAP. You must use secure version POP3S, IMAPS*
```
telnet mail.lab.local 110
Trying 192.168.88.105...
Connected to mail.lab.local.
Escape character is '^]'.
+OK Dovecot ready.
user adam
-ERR [AUTH] Plaintext authentication disallowed on non-secure (SSL/TLS) connections.
```
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
