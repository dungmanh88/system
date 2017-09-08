https://www.opensips.org/Documentation/Tutorials-OpenSIPSFreeSwitchIntegration#toc1
#http://yum.opensips.org/howto.php

#yum -y install http://yum.opensips.org/2.3/releases/el/7/x86_64/opensips-yum-releases-2.3-3.el7.noarch.rpm
#yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
#yum -y install opensips
#systemctl start opensips
#systemctl enable opensips
#Bản opensips này không hỗ trợ db

Disable selinux

wget http://opensips.org/pub/opensips/latest/opensips-2.3.2.tar.gz
cd opensips-2.3.2
https://github.com/OpenSIPS/opensips/blob/master/INSTALL
https://www.opensips.org/Documentation/Install-CompileAndInstall-2-3
yum -y install gcc gcc-c++ make bison flex openssl-devel libxml2-devel ncurses-devel mysql-devel unixODBC-devel nginx
yum -y install php php-fpm php-mysql php-cli php-gd php-pear php-xmlrpc

make clean
make all
make menuconfig > configure compile options
-> customize install path > configure install prefix, default /usr/local/opensips
-> customize module > configure excluded module ->
Select the db_mysql, db_unixodbc, dialplan, mi_xmlrpc, presence*, pua*, regex modules with the spacebar key, then hit the 'q' key
q > save > re-compile and re-install opensips make all && make install

make install

yum -y install mariadb-server
systemctl start mariadb-server
systemctl enable mariadb-server

```
MariaDB [(none)]> grant all privileges on `opensips`.* to 'opensips'@'localhost' identified by 'opensipsrw';
Query OK, 0 rows affected (0.00 sec)
```

```
/usr/local/opensips/sbin/opensipsdbctl create
MySQL password for root:
INFO: test server charset
INFO: creating database opensips ...
INFO: Using table engine InnoDB.
INFO: Core OpenSIPS tables successfully created.
Install presence related tables? (y/n): y
INFO: creating presence tables into opensips ...
INFO: Presence tables successfully created.
Install tables for imc cpl siptrace domainpolicy carrierroute userblacklist b2b cachedb_sql registrant call_center fraud_detection emergency? (y/n): y
INFO: creating extra tables into opensips ...
INFO: Extra tables successfully created.
```

```
/usr/local/opensips/sbin/osipsconfig > Generate opensips script > Residential Script > Configure residential script
>  Add ENABLE_TCP, USE_ALIASES, USE_AUTH, USE_DBACC, USE_DBUSRLOC, USE_DIALOG, USE_DIALPLAN, VM_DIVERSION > q > Generate residential script
```
script gen to /usr/local/opensips/etc/opensips
```
mv opensips_residential_2017-9-7_6\:47\:35.cfg opensips_residential_01.cfg
mv opensips.cfg opensips.cfg.orig
mv opensips_residential_01.cfg opensips.cfg
```

vi opensips_residential_01.cfg - load module

cd /root/opensips-2.3.2/packaging/redhat_fedora/
cp -r opensips.init  /etc/init.d/opensips
chmod u+x /etc/init.d/opensips
/etc/init.d/opensips
```
base=/usr/local/opensips
prog=opensips
opensips=$base/sbin/$prog
cfgdir="$base/etc/$prog"
pidfile="/var/run/$prog.pid"
lockfile="/var/lock/subsys/$prog"
configfile="$cfgdir/$prog.cfg"
m4configfile="$cfgdir/$prog.m4"
m4archivedir="$cfgdir/archive"
```

Create user opensips:
```
opensips:x:997:994:OpenSIPS SIP Server:/var/run/opensips:/sbin/nologin
```
/etc/init.d/opensips start
chkconfig opensips on

insert into load_balancer(group_id, dst_uri, resources) values(1, "sip:<fs-ip>", "ch=fs://:ClueCon@<fs-ip>");

############################## Delete
wget https://github.com/OpenSIPS/opensips-cp/archive/7.2.3.zip
cd opensips-cp-7.2.3
systemctl enable httpd
systemctl start httpd
pear install mdb2
pear install mdb2#mysql
vi config/db.inc.php - donothing
vi config/boxes.global.inc.php
```
...
// options: fifo:/path/to/fifo_file | xmlrpc:host:port | udp:host:port | json:json_url
// $boxes[$box_id]['mi']['conn']="xmlrpc:192.168.0.2:8080";
$boxes[$box_id]['mi']['conn']="/tmp/opensips_fifo";


// monit host:port
//$boxes[$box_id]['monit']['conn']="192.168.0.2:2812";
//$boxes[$box_id]['monit']['user']="admin";
//$boxes[$box_id]['monit']['pass']="pass";
//$boxes[$box_id]['monit']['has_ssl']=1;
...
```
vi config/tools/system/dialog/local.inc.php
```
$box[1]['mi']['conn']="/tmp/opensips_fifo";
```

vi config/tools/system/dispatcher/local.inc.php
```
$box[1]['mi']['conn']="/tmp/opensips_fifo";
```

/etc/httpd/conf/httpd.conf
```
Alias /cp /var/www/opensips-cp/web
```
mkdir -p /var/www/opensips-cp
cp -r web/ /var/www/opensips-cp
cd /var/www/opensips-cp/web
pear install log


mysql -u opensips -p opensips < config/tools/admin/add_admin/ocp_admin_privileges.mysql
mysql -u opensips -p -e "use opensips;INSERT INTO ocp_admin_privileges (username,password,ha1,available_tools,permissions) values
       ('admin','admin',md5('admin:admin'),'all','all');"
mysql -u opensips -p opensips < config/tools/system/smonitor/tables.mysql

crontab -e
```
* * * * *   root   php /var/www/opensips-cp/cron_job/get_opensips_stats.php > /dev/null
```

systemctl restart httpd
systemctl restart crond
/etc/init.d/opensips restart
##############################

cp /usr/local/opensips/etc/opensips/opensipsctlrc /usr/local/opensips/etc/opensips/opensipsctlrc.orig
vi /usr/local/opensips/etc/opensips/opensipsctlrc
```
DBENGINE=MYSQL
DBPORT=3306
DBHOST=localhost
DBNAME=opensips
DBRWUSER=opensips
DBRWPW="opensipsrw"
DBROOTUSER="root"
```

cp /usr/local/opensips/etc/opensips/opensips_residential_01.cfg /usr/local/opensips/etc/opensips/opensips_residential_01.cfg.orig
http://www.opensips.org/html/docs/modules/2.3.x/load_balancer.html
https://www.youtube.com/watch?v=gDpe1fyRaZw
```
listen=udp:<opensips-ip>:5060
listen=tcp:<opensips-ip>:5060

loadmodule "load_balancer.so"
modparam("load_balancer", "db_url","mysql://opensips:opensipsrw@localhost/opensips")
modparam("load_balancer", "initial_freeswitch_load", 15)
modparam("load_balancer", "fetch_freeswitch_stats", 1)

loadmodule "freeswitch.so"

if ($rU==NULL) {
        # request with no Username in RURI
        sl_send_reply("484","Address Incomplete");
        exit;
}

# count as load also the calls orgininated by lb destinations
if (lb_is_destination("$si","$sp") ) {
	# inbound call from destination
	lb_count_call("$si","$sp","-1","conference");
} else {
	# outbound call to destinations
	if ( !load_balance("1","conference") ) {
		send_reply("503","unavailable");
		exit();
	}
	# dst URI points to the new destination
	xlog("sending call to $du\n");
	t_relay();
	exit;
}

# apply DB based aliases
alias_db_lookup("dbaliases");

```

/etc/freeswitch/autoload_config/switch.conf.xml
```
<param name="event-heartbeat-interval" value="20"/>
<param name="max-sessions" value="1000"/>
```

/etc/freeswitch/autoload_config/event_socket.conf.xml
```
<configuration name="event_socket.conf" description="Socket Client">
  <settings>
    <param name="nat-map" value="false"/>
    <param name="listen-ip" value="::"/>
    <param name="listen-port" value="8021"/>
    <param name="password" value="ClueCon"/>
    <!--<param name="apply-inbound-acl" value="loopback.auto"/>-->
    <!--<param name="stop-on-bind-error" value="true"/>-->
  </settings>
</configuration>
```
