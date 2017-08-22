# Get date time
date

# Change timezone in centos 6
cp /etc/localtime /root/old.timezone
rm /etc/localtime
ln -s /usr/share/zoneinfo/Asia/Bangkok /etc/localtime

# Change timezone in centos 7
timedatectl list-timezones
timedatectl set-timezone America/Chicago
timedatectl status

# Synchronize datetime
systemctl start ntpd
