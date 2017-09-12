On test3
https://www.youtube.com/watch?v=gDpe1fyRaZw
https://www.opensips.org/Documentation/Tutorials-OpenSIPSFreeSwitchIntegration#toc1 (old docs)
https://github.com/OpenSIPS/opensips/blob/master/INSTALL
https://www.opensips.org/Documentation/Install-CompileAndInstall-2-3
https://blog.opensips.org/2017/03/01/freeswitch-driven-routing-in-opensips-2-3/
http://www.opensips.org/html/docs/modules/2.3.x/load_balancer#id293644
https://voipmagazine.wordpress.com/tag/osipsconfig/
http://www.opensips.org/html/docs/modules/2.3.x/load_balancer.html
https://freeswitch.org/confluence/display/FREESWITCH/OpenSIPS+configuration+for+2+or+more+FreeSWITCH+installs
https://www.opensips.org/Documentation/Tutorials-LoadBalancing

Disable selinux

wget http://opensips.org/pub/opensips/latest/opensips-2.3.2.tar.gz
cd opensips-2.3.2
yum -y install gcc gcc-c++ make bison flex openssl-devel libxml2-devel ncurses-devel mysql-devel unixODBC-devel

make clean
make all ### compile core module
make menuconfig > configure compile options > configure install prefix, change to /usr/local/opensips
make menuconfig > configure compile options > configure excluded module ->
Select the db_mysql, db_unixodbc, dialplan, mi_xmlrpc_ng, regex, presence*, pua* modules with the spacebar key, then hit the 'q' key
q > save > q > compile and install opensips (= make all && make install)

You can re-make anytime.

yum -y install mariadb-server
systemctl start mariadb-server
systemctl enable mariadb-server

```
> grant all privileges on `opensips`.* to 'opensips'@'localhost' identified by 'opensipsrw';
Query OK, 0 rows affected (0.00 sec)
```

cp /usr/local/opensips/etc/opensips/opensipsctlrc /usr/local/opensips/etc/opensips/opensipsctlrc.orig
vi /usr/local/opensips/etc/opensips/opensipsctlrc
```
SIP_DOMAIN=lb-ip
DBENGINE=MYSQL
DBPORT=3306
DBHOST=localhost
DBNAME=opensips
DBRWUSER=opensips
DBRWPW="opensipsrw"
DBROOTUSER="root"
```

/usr/local/opensips/sbin/opensipsdbctl create
```
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
56 tables will be created

/usr/local/opensips/sbin/osipsconfig > Generate opensips script
Residential Script > Configure residential script
Trunking script (when you have PBX)
Load balancer script (simple load balancer)
```
>  Add ENABLE_TCP, USE_ALIASES, USE_AUTH, USE_DBACC, USE_DBUSRLOC, USE_DIALOG, USE_DIALPLAN, VM_DIVERSION > q > Generate residential script
```
Try to Generate loadbalancer script with ENABLE_TCP

script gen to /usr/local/opensips/etc/opensips
```
mv opensips_loadbalancer_2017-9-9_23:41:37.cfg opensips_loadbalancer.cfg
mv opensips_residential_2017-9-9_23:41:7.cfg opensips_residential.cfg
```

vi opensips_residential.cfg
```
log_level=3
log_facility=LOG_LOCAL1

listen=udp:<lb-ip>:5060   # CUSTOMIZE ME
listen=tcp:<lb-ip>:5060
mpath="/usr/local//lib64/opensips/modules/" # FOCUS to make sure set correctly


#### LOAD BALANCER module - below DIALOG module
loadmodule "freeswitch.so"

loadmodule "load_balancer.so"
modparam("load_balancer", "db_url",
        "mysql://opensips:opensipsrw@localhost/opensips") # CUSTOMIZE ME
modparam("load_balancer", "probing_method", "OPTIONS")
modparam("load_balancer", "probing_interval", 30)
modparam("load_balancer", "initial_freeswitch_load", 15)
modparam("load_balancer", "fetch_freeswitch_stats", 1)

....

if ($rU==NULL) {
        # request with no Username in RURI
        sl_send_reply("484","Address Incomplete");
        exit;
}

if ($rU=~"^\*") {
        strip(1);
        $du = "sip:fs-ip:5060"; # CUSTOMIZE ME
        route(relay);
}

...


# do lookup with method filtering
if (!lookup("location","m")) {


        t_newtran();
        t_reply("404", "Not Found");
        exit;
}



# when routing via usrloc, log the missed calls also
do_accounting("log","missed");

if ( !load_balance("1","channel")) {

        send_reply("500","No Destination available");
        exit;
}
route(relay);

...

```
Some config is using 127.0.0.1
```
# do lookup with method filtering
if (!lookup("location","m")) {
        if (!db_does_uri_exist()) {
                send_reply("420","Bad Extension");
                exit;
        }

        # redirect to a different VM system
        $du = "sip:127.0.0.2:5060"; # CUSTOMIZE ME
        route(relay);

}


# redirect the failed to a different VM system
if (t_check_status("486|408")) {
        $du = "sip:127.0.0.2:5060"; # CUSTOMIZE ME
        # do not set the missed call flag again
        route(relay);
}
```


vi /etc/rsyslog.conf
```
# Save boot messages also to boot.log
local7.*                                                /var/log/boot.log
local1.*                        - /var/log/opensips.log
```
systemctl restart rsyslog

cd /root/opensips-2.3.2/packaging/redhat_fedora/
cp -r opensips.init  /etc/init.d/opensips
chmod u+x /etc/init.d/opensips
vi /etc/init.d/opensips
```
base=/usr/local/opensips
prog=opensips
opensips=$base/sbin/$prog
cfgdir="$base/etc/$prog"
pidfile="/var/run/$prog.pid"
lockfile="/var/lock/subsys/$prog"
configfile="$cfgdir/opensips_residential.cfg"
m4configfile="$cfgdir/$prog.m4"
m4archivedir="$cfgdir/archive"
```

```
useradd -d /dev/null -c "OpenSIPS SIP Server" -s /sbin/nologin opensips
```

/etc/init.d/opensips start
chkconfig opensips on

insert into load_balancer(group_id, dst_uri, resources) values(1, "sip:<fs-ip>:5060", "ch=fs://:ClueCon@<fs-ip>");

/etc/freeswitch/autoload_configs/switch.conf.xml
```
<param name="event-heartbeat-interval" value="20"/>
<param name="max-sessions" value="1000"/>
```

/etc/freeswitch/autoload_configs/event_socket.conf.xml
```
<configuration name="event_socket.conf" description="Socket Client">
  <settings>
    <param name="nat-map" value="false"/>
    <param name="listen-ip" value="fs-ip"/>
    <param name="listen-port" value="8021"/>
    <param name="password" value="ClueCon"/>
    <param name="apply-inbound-acl" value="lb-net/net-mask"/>
    <!--    <param name="stop-on-bind-error" value="true"/> -->
  </settings>
</configuration>
```
systemctl restart freeswitch

On opensips - this is new register on opensips
opensipsctl add 5000 5000

Database changed: subscriber and location


opensipsctl add 5001 5001

How to forward from 5000 opensips to 5000 freeswitch

That bai roi
