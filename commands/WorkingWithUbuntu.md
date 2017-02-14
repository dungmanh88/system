## Package management
### Update package
```
apt-get update
```

### Enable sshd
http://ubuntuhandbook.org/index.php/2016/04/enable-ssh-ubuntu-16-04-lts/
```
apt-get update
apt-get install openssh-server
service ssh start
update-rc.d ssh defaults
```
