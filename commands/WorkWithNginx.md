## htaccess
Follow https://www.digitalocean.com/community/tutorials/how-to-set-up-password-authentication-with-nginx-on-ubuntu-14-04
```
sudo sh -c "echo -n 'sammy:' >> /etc/nginx/.htpasswd"
sudo sh -c "openssl passwd -apr1 >> /etc/nginx/.htpasswd"
cat /etc/nginx/.htpasswd
sammy:$apr1$wI1/T0nB$jEKuTJHkTOOWkopnXqC1d1
```

## Basic permision
```
find /path/to/vhost/document/root -type f -exec chmod 644 {} \;
find /path/to/vhost/document/root -type d -exec chmod 755 {} \;
```

## Create user
```
useradd -d /dev/null -c "nginx user" -s /sbin/nologin nginx
```
