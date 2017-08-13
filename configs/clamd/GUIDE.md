Find out which OS you are using
cat /etc/issue
Debian GNU/Linux 6.0 \n \l

Debian 6 code is squeeze

Resolve source list based on OS
/etc/apt/sources.list
```
deb http://archive.debian.org/debian/ squeeze main non-free contrib
deb-src http://archive.debian.org/debian/ squeeze main non-free contrib
deb http://archive.debian.org/debian-security/ squeeze/updates main non-free contrib
deb-src http://archive.debian.org/debian-security/ squeeze/updates main non-free contrib
```

apt-get update
apt-get install clamav clamav-daemon

/etc/resolv.conf
```
nameserver 8.8.8.8
```

Sample:
/usr/local/etc/freshclam.conf.sample
/usr/local/etc/clamd.conf.sample

/etc/init.d/clamav-daemon restart

/etc/clamav/freshclam.conf
/etc/clamav/clamd.conf
/var/log/clamav/clamav.log
/var/log/clamav/freshclam.log
/var/lib/clamav

Clamav is runing on unix domain socket by default, change it
/etc/clamav/clamd.conf
```
#LocalSocket /var/run/clamav/clamd.ctl
#FixStaleSocket true
#LocalSocketGroup clamav
#LocalSocketMode 666
TCPSocket 3310
TCPAddr localhost
```

# Update
## Config freshclam
```
dpkg-reconfigure clamav-freshclam
File config will be placed in /etc/clamav/freshclam.conf
```
```
ln -s /etc/clamav/freshclam.conf /usr/local/etc/freshclam.conf
freshclam
```
or
```
/etc/init.d/clamav-freshclam restart
```
