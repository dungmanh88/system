# Install jdk 8 oracle
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

# Install solr
wget http://mirrors.viethosting.com/apache/lucene/solr/6.6.0/solr-6.6.0.tgz
tar xvzf solr-6.6.0.tgz
mv solr-6.6.0.tgz solr
cd solr

# Start/stop solr
*Don't run as root*
bin/solr start -p 8984
bin/solr stop -p 8984

# Add new core
bin/solr create -c <core_name> -p 8984
Restart service

# Add existing core
mkdir -p server/solr/<core_name>
copy data: [conf  core.properties  data] into server/solr/<core_name>
Restart service

# Access
http://<IP-SERVER>:8984

# Config secure
Force solr bind on localhost
```
location /solr/<core_name>/select{
  proxy_pass http://127.0.0.1:8984;
}
```
