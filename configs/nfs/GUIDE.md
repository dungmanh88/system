# Server
yum -y install nfs-utils nfs-utils-lib

/etc/exports
```
/var/vmail/mail/    *(rw,sync)
```

service rpcbind start
chkconfig rpcbind on
service nfs start
chkconfig nfs on

exportfs -v
/var/vmail/mail


# Client
yum -y install nfs-utils nfs-utils-lib
showmount -e xx.xx.xx.xx
Export list for xx.xx.xx.xx:
/var/vmail/mail *

mkdir -p /mailbox
mount xx.xx.xx.xx:/var/vmail/mail /mailbox
ln -s /mailbox /var/vmail/mail

By default, you can not use root to write to nfs mountpoint from client.

You should add remote mountpoint into /etc/fstab
