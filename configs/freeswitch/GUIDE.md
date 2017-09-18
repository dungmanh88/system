On test4
https://freeswitch.org/confluence/display/FREESWITCH/CentOS+7+and+RHEL+7
https://astppdoc.atlassian.net/wiki/spaces/ASTPP/pages/11108393/CentOS+7+Installation
https://jamesnbr.wordpress.com/2016/04/12/freeswitch-1-6-installation-configuration-on-centos-7/

[root@template-centos7 default]# sestatus
SELinux status:                 disabled
systemctl stop firewalld
iptables -F
iptables -t nat -F

yum update
yum groupinstall "Development tools" -y
yum install epel-release

rpm -Uvh http://files.freeswitch.org/freeswitch-release-1-6.noarch.rpm
yum install -y freeswitch-config-vanilla freeswitch-lang-* freeswitch-sounds-*
systemctl enable freeswitch
systemctl start freeswitch
fs_cli -rRS

Some config you should know
Default passwd of freeswitch

vi /etc/freeswitch/vars.xml
```
<X-PRE-PROCESS cmd="set" data="default_password=1234"/>
```

pre extension of freeswitch 1000-1019
/etc/freeswitch/directory/default
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1000.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1001.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1002.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1003.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1004.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1005.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1006.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1007.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1008.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1009.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1010.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1011.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1012.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1013.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1014.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1015.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1016.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1017.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1018.xml
-rw-r----- 1 freeswitch daemon  751 Jul 13 19:46 1019.xml

https://freeswitch.org/confluence/display/FREESWITCH/XML+Dialplan
add 5000 and 5001 as my extensions
cp 1000.xml 5000.xml
cp 1000.xml 5001.xml

5000.xml
```
<include>
  <user id="5000">
    <params>
      <param name="password" value="5000"/>
      <param name="vm-password" value="5000"/>
    </params>
    <variables>
      <variable name="toll_allow" value="domestic,international,local"/>
      <variable name="accountcode" value="5000"/>
      <variable name="user_context" value="default"/>
      <variable name="effective_caller_id_name" value="dungnm"/>
      <variable name="effective_caller_id_number" value="5000"/>
      <variable name="outbound_caller_id_name" value="$${outbound_caller_name}"/>
      <variable name="outbound_caller_id_number" value="$${outbound_caller_id}"/>
      <variable name="callgroup" value="techsupport"/>
    </variables>
  </user>
</include>
```

5001.xml
```
<include>
  <user id="5001">
    <params>
      <param name="password" value="5001"/>
      <param name="vm-password" value="5001"/>
    </params>
    <variables>
      <variable name="toll_allow" value="domestic,international,local"/>
      <variable name="accountcode" value="5001"/>
      <variable name="user_context" value="default"/>
      <variable name="effective_caller_id_name" value="dungnm1"/>
      <variable name="effective_caller_id_number" value="5001"/>
      <variable name="outbound_caller_id_name" value="$${outbound_caller_name}"/>
      <variable name="outbound_caller_id_number" value="$${outbound_caller_id}"/>
      <variable name="callgroup" value="techsupport"/>
    </variables>
  </user>
</include>
```

[root@template-centos7 default]# chown -R freeswitch:daemon 5000.xml
[root@template-centos7 default]# chown -R freeswitch:daemon 5001.xml

setting extension, edit something
/etc/freeswitch/dialplan/default.xml

<extension name="Local_Extension">
<condition field="destination_number" expression=”^(10[01][0-9]|50[01][0-9])$”>

Configure log file
/etc/freeswitch/autoload_configs/logfile.conf.xml
```
        <!-- File to log to -->
        <param name="logfile" value="/var/log/freeswitch.log"/>
        <!-- At this length in bytes rotate the log file (0 for never) -->
```


Make sure:
/etc/freeswitch/vars.xml
```
<!-- Internal SIP Profile -->
<X-PRE-PROCESS cmd="set" data="internal_auth_calls=true"/>
<X-PRE-PROCESS cmd="set" data="internal_sip_port=5060"/>
<X-PRE-PROCESS cmd="set" data="internal_tls_port=5061"/>
<X-PRE-PROCESS cmd="set" data="internal_ssl_enable=false"/>

<!-- External SIP Profile -->
<X-PRE-PROCESS cmd="set" data="external_auth_calls=false"/>
<X-PRE-PROCESS cmd="set" data="external_sip_port=5080"/>
<X-PRE-PROCESS cmd="set" data="external_tls_port=5081"/>
<X-PRE-PROCESS cmd="set" data="external_ssl_enable=false"/>
```

fs_cli
freeswitch@template-centos7> reloadxml
or
fs_cli -x "reloadxml"

Test
https://wiki.freeswitch.org/wiki/Getting_Started_Guide
Install linphone on mobile.
Config sip account

username: 5000
passwd: 5000
domain: test4
transport: tcp

Call 3000 to hear music
Call 9196 to hear echo
Call 9198 to hear Tetris extension
The sound is generated solely using tone generation.
Call 9664 to hear music on hold
Call 3000 to join conference. All parties will be able to hear each other.
Call 9192 to see channel variables
