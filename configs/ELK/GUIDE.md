https://www.digitalocean.com/community/tutorials/how-to-install-elasticsearch-logstash-and-kibana-elk-stack-on-centos-7
http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
jdk-8u144-linux-x64.rpm
rpm -iv jdk-8u144-linux-x64.rpm

jre:
/usr/java/jdk1.8.0_144/jre/bin/
jdk:
/usr/java/jdk1.8.0_144/bin

/etc/profile.d/java.sh
```
export JAVA_HOME=/usr/java/jdk1.8.0_144
```
source /etc/profile.d/java.sh

cd /tmp
curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.5.1.tar.gz
mv elasticsearch-5.5.1 elasticsearch
mv elasticsearch /usr/local/bin
useradd -d /usr/local/bin/elasticsearch -c "elasticsearch user" -s /sbin/nologin elasticsearch
chown -R elasticsearch:elasticsearch /usr/local/bin/elasticsearch/

usermod -s /bin/bash elasticsearch
su - elasticsearch (RUN BY NORMAL USER)
bin/elasticsearch (NEVER RUN BY ROOT)

/etc/yum.repos.d/kibana.repo
[kibana-5.x]
name=Kibana repository for 5.x packages
baseurl=https://artifacts.elastic.co/packages/5.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md

yum -y install kibana
/etc/kibana/kibana.yml
```
server.port: 5601
server.host: "localhost"
```
systemctl restart kibana
systemctl enable kibana


yum -y install epel-release
yum -y install nginx httpd-tools
htpasswd -c /etc/nginx/htpasswd.users kibanaadmin
abc@123

/etc/nginx/nginx.conf
```
include /etc/nginx/conf.d/*.conf;
}
```

/etc/nginx/conf.d/kibana.conf
```
server {
    listen 80;

    server_name kibana.lab.com;

    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/htpasswd.users;

    location / {
        proxy_pass http://localhost:5601;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;        
    }
}
```
systemctl restart nginx
systemctl enable nginx


/etc/yum.repos.d/logstash.repos
```
[logstash-5.x]
name=Elastic repository for 5.x packages
baseurl=https://artifacts.elastic.co/packages/5.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
```
yum install -y logstash

Gen cert
```
cd /etc/pki/tls
openssl req -subj '/CN=elk.lab.com/' -x509 -days 3650 -batch -nodes -newkey rsa:2048 -keyout private/logstash-forwarder.key -out certs/logstash-forwarder.crt
```
