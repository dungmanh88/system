http://saevolgo.blogspot.com/2012/03/making-rtpproxy-work.html
http://saevolgo.blogspot.com/2013/08/rtpproxy-revisited-kamailio-40.html
http://saevolgo.blogspot.com/2012/06/opensips-as-load-balancer-for.html
http://kb.asipto.com/freeswitch:kamailio-3.0.x-freeswitch-1.0.6d-ms
http://kb.asipto.com/freeswitch:kamailio-3.1.x-freeswitch-1.0.6d-sbc
http://lists.sip-router.org/pipermail/sr-users/2011-September/070196.html
https://lists.kamailio.org//pipermail/sr-users/2011-September/thread.html#70205
https://www.kamailio.org/wiki/cookbooks/4.2.x/pseudovariables
https://www.kamailio.org/wiki/cookbooks/4.4.x/core#mhomed --- If you use private IP for FS you will consider this options
https://www.kamailio.org/docs/modules/5.0.x/modules/rtpproxy.html
https://lists.kamailio.org/pipermail/sr-users/2014-March/082250.html
http://lists.freeswitch.org/pipermail/freeswitch-users/2010-March/055234.html
http://lists.freeswitch.org/pipermail/freeswitch-users/2015-August/115098.html

Mastering FS ebook
Openser ebook
Opensips ebook
FreeSWITCH 1.2 ebook

Comment:
```
http://saevolgo.blogspot.com/2012/07/freeswitch-with-sip-users-in-mysql-mod.html
Here is my idea:

1- Put in a Kamailio or OpenSIPS infront of your FreeSWITCH Servers, Let the SIP proxy handle the registrations.

2- For any incoming call send call to Load-Balanced array of FreeSWITCH servers who will just do some call routing logic, and if the dialed number matches the extension sequence number route call back to the SIP Proxy.

3- In SIP Proxy detect the call is coming in from the FreeSWITCH servers, try finding the active registered extension in SIP Proxy and connect the call to that user.

4- If in SIP proxy the number is offline, send call to some outbound gateway/trunk.
```

Kamailio:
- load balancer for media servers FS
- SIP registra
- SIP proxy
- SIP auth
- SIP location
- Support RTPProxy module to relay media service
- Two interfaces: WAN and LAN

Media server:
- FS process media service from RTP Proxy
- Only have LAN IP

Architecture

SIP phone A ---> Kamailio(SIP) + rtpproxy(RTP) ---> (FS1,2,3,..,n) ---> Kamailio(SIP) + RTPProxy(RTP) ---> SIP phone B

hostnamectl set-hostname kamailio

Off firewall and selinux

[home_kamailio_v4.3.x-rpms]
name=RPM Packages for Kamailio v4.3.x (RHEL_7)
type=rpm-md
baseurl=http://download.opensuse.org/repositories/home:/kamailio:/v4.3.x-rpms/RHEL_7/
gpgcheck=1
gpgkey=http://download.opensuse.org/repositories/home:/kamailio:/v4.3.x-rpms/RHEL_7//repodata/repomd.xml.key
enabled=1

mkdir -p /var/run/kamailio
chown -R kamailio:kamailio /var/run/kamailio
to save kamailio_fifo and kamailio_ctl...

yum -y install kamailio wget tmux gdb kamailio-mysql kamailio-tls mysql mariadb-server

yum install epel-release
or
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
rpm -ivh epel-release-latest-7.noarch.rpm

yum install rtpproxy

/etc/kamailio/kamctlrc
```
SIP_DOMAIN=lb-ip
DBENGINE=MYSQL
DBHOST=localhost
DBNAME=kamailio
DBRWUSER="kamailio"
DBRWPW="kamailiorw"
DBACCESSHOST=localhost
DBROOTUSER="root"
```

systemctl restart mariadb && systemctl enable mariadb
systemctl restart kamailio && systemctl enable kamailio

Gen DB
kamdbctl create ### will create db kamailio by default
grant all privileges on `kamailio`.* to 'kamailio'@'localhost' identified by 'kamailiorw';

Start rtpproxy on bridge mode
//rtpproxy -F -l public-lb-ip/private-lb-ip -s udp:127.0.0.1:7722 -d DBUG:LOG_LOCAL0
//rtpproxy -F -l localip -A publicip  -s udp:127.0.0.1:7722 -d DBUG:LOG_LOCAL0
rtpproxy -F -l 172.31.21.142/54.202.25.215 -s udp:127.0.0.1:7722 -d DBUG:LOG_LOCAL0

rtpproxy -F -A 34.213.179.216 172.31.30.47 -l 172.31.30.47 127.0.0.1 -m 10000 -M 65000 -s udp:127.0.0.1:7722 -d DBUG:LOG_LOCAL3

-m 10000 -M 65000

Config kamailio

cd /etc/kamailio
mv kamailio.cfg  kamailio.cfg.orig
cp kamailio-basic.cfg kamailio.cfg

Base on kamailio-basic.cfg
```
# *** To enable mysql:
#     - define WITH_MYSQL
#!define WITH_MYSQL

# *** To enable authentication execute:
#     - enable mysql
#     - define WITH_AUTH
#!define WITH_AUTH

# *** To enable persistent user location execute:
#     - enable mysql
#     - define WITH_USRLOCDB
#!define WITH_USRLOCDB

# *** To enable nat traversal execute:
#     - define WITH_NAT
#!define WITH_NAT
```

- Config log
```
log_facility=LOG_LOCAL2
```
- Config alias
```
auto_aliases=no
alias="lb-ip"
```
- Config listen
```
listen=udp:lb-ip:5060
or comment to listen all interface
```
mhomed=1
fork=yes
//children=<core number of cpu, output nproc>

- Use avpops.so
- Use dispatcher.so
```
loadmodule "acc.so"
loadmodule "avpops.so"
loadmodule "dispatcher.so"

#!ifdef WITH_AUTH
...
```
- Config param module avpops.so
```
# ----- tm params -----
...
# ------- AVP-OPS params ---------
modparam("avpops","db_url", DBURL)
modparam("avpops","avp_table","dispatcher")

# ----- dispatcher params -----
...
```
- Config param module dispatcher.so
```
# ------- AVP-OPS params ---------
...
# ----- dispatcher params -----
modparam("dispatcher", "db_url", DBURL)
modparam("dispatcher", "table_name", "dispatcher")
modparam("dispatcher", "flags", 2)
modparam("dispatcher", "dst_avp", "$avp(AVP_DST)")
modparam("dispatcher", "grp_avp", "$avp(AVP_GRP)")
modparam("dispatcher", "cnt_avp", "$avp(AVP_CNT)")
modparam("dispatcher", "sock_avp", "$avp(AVP_SOCK)")

# ----- rr params -----
...
```
- Block scanner
```
if($ua =~ "friendly-scanner") {
        sl_send_reply("404", "NOt here");
        exit;
}
```
- Rewrite auth in registra and invite process
```
# Handle SIP registrations
route[REGISTRAR] {
        if (!is_method("REGISTER")) return;
        if(isflagset(FLT_NATS)) {
                setbflag(FLB_NATB);
#!ifdef WITH_NATSIPPING
                # do SIP NAT pinging
                setbflag(FLB_NATSIPPING);
#!endif
        }
        #xlog("test");
        if (!www_authorize("kamailio test", "subscriber")) {
                www_challenge("kamailio test", "0");
                exit;
        }

        if (!save("location"))
                sl_reply_error();

        exit;
}

# IP authorization and user uthentication
route[AUTH] {
#!ifdef WITH_AUTH

#!ifdef WITH_IPAUTH
        if((!is_method("REGISTER")) && allow_source_address()) {
                # source IP allowed
                return;
        }
#!endif

        if(ds_is_from_list("1")) {
                return;
        }

        if (!is_method("REGISTER")) {
                # authenticate requests
                if (!proxy_authorize("kamailio test","subscriber")) {
                        proxy_challenge("kamailio test","0");
                        exit;
                }

                consume_credentials();

        }
        # if caller is not local subscriber, then check if it calls
        # a local destination, otherwise deny, not an open relay here
        if (from_uri!=myself && uri!=myself) {
                sl_send_reply("403","Not relaying");
                exit;
        }

#!endif
        return;
}
```
- Request route
```
if ($rU==$null) {
        # request with no Username in RURI
        sl_send_reply("484","Address Incomplete");
        exit;
}

route(DISPATCH);

# user location service
route(LOCATION);
```
- route[DISPATCH]
```
route[DISPATCH] {

        if(!is_method("INVITE")){
                return;
        }

        if(ds_is_from_list("1")) {
                return;
        }

        prefix("kb-");
        # round robin dispatching on gateways group '1'
        if(!ds_select_dst("1", "4"))
        {
                send_reply("404", "No destination");
                exit;
        }
        xlog("L_DBG", "--- SCRIPT: going to <$ru> via <$du>\n");
        t_on_failure("RTF_DISPATCH");
        route(RELAY);
        exit;
}
```
- failure_route[RTF_DISPATCH]
```
# Sample failure route
failure_route[RTF_DISPATCH] {
        if (t_is_canceled()) {
                exit;
        }
        # next DST - only for 500 or local timeout
        if (t_check_status("500")
                        or (t_branch_timeout() and !t_branch_replied()))
        {
                if(ds_next_dst())
                {
                        t_on_failure("RTF_DISPATCH");
                        route(RELAY);
                        exit;
                }
        }
}
```
- Rewrite route[NATMANAGE]
```
if (!(isflagset(FLT_NATS) || isbflagset(FLB_NATB)))
        return;

if (is_method("BYE")) {
        xlog("L_NOTICE","$rm from $fu (IP:$si:$sp) in Route[RTPPROXY] unforced RTP Proxy STATS='$rtpstat'\n");
        rtpproxy_destroy();
} else if (is_method("INVITE")) {
        if(avp_db_query("select destination from dispatcher where destination like '%$dd%'")){
                xlog("L_NOTICE","$rm from $fu (IP:$si:$sp) in route[RTPPROXY] RTPproxy with IE Flags\n");
                rtpproxy_manage("rwei");

        }
        else if(avp_db_query("select destination from dispatcher where destination='sip:$si:$sp'")){
                 xlog("L_NOTICE","$rm from $fu (IP:$si:$sp) in route[RTPPROXY] RTPproxy with EI Flags\n");
                rtpproxy_manage("rwie");

        }
        else {
                xlog("L_NOTICE","$rm from $fu (IP:$si:$sp) in Route[RTPPROXY] Forcing RTPproxy\n");
          #      rtpproxy_manage("r");
        }
}

#rtpproxy_manage("co");
```

- Add db of kamailio
insert into dispatcher(setid, destination) values(1,'sip:fs-ip-1|2:5060');
```
mysql> select * from dispatcher\G
*************************** 1. row ***************************
         id: 1
      setid: 1
destination: sip:fs-ip-1:5060
      flags: 0
   priority: 0
      attrs:
description:
*************************** 2. row ***************************
         id: 2
      setid: 1
destination: sip:fs-ip-2:5060
      flags: 0
   priority: 0
      attrs:
description:
2 rows in set (0.00 sec)
```

kamailio -c -f kamailio.cfg
```
oading modules under config path: /usr/lib64/kamailio/modules/
 0(6505) INFO: <core> [sctp_core.c:75]: sctp_core_check_support(): SCTP API not enabled - if you want to use it, load sctp module
Listening on
             udp: 127.0.0.1:5060
             udp: 172.31.21.142:5060
             tcp: 127.0.0.1:5060
             tcp: 172.31.21.142:5060
Aliases:
             *: 54.202.25.215:*

config file ok, exiting...
```

On Freeswitch
- Follow Install_from_pkgs.md to install Freeswitch
- Follow Acl instruction
- Some dialplan
/etc/freeswitch/dialplan/public.xml
```
<include>
  <context name="public">


  <extension name="from_kamailio">
      <condition field="network_addr" expression="^xx\.xx\.xx\.xx$" /> // this is IP of kamailio
      <condition field="destination_number" expression="^(.+)$">
        <action application="transfer" data="$1 XML default"/>
      </condition>
    </extension>

```
/etc/freeswitch/dialplan/default.xml
```
<extension name="extension-intercom">
...
<!--
     dial the extension (1000-1019) for 30 seconds and go to voicemail if the
     call fails (continue_on_fail=true), otherwise hang up after a successful
     bridge (hangup_after_bridge=true)
-->

<extension name="kbridge">
  <condition field="destination_number" expression="^kb-(.+)$">
              <action application="set" data="proxy_media=true"/>
              <action application="set" data="call_timeout=50"/>
              <action application="set" data="continue_on_fail=true"/>
              <action application="set" data="hangup_after_bridge=true"/>
              <action application="set" data="sip_invite_domain=fs-ip"/> // this is ip of fs
              <action application="export" data="sip_contact_user=ufs"/>
              <action application="bridge" data="sofia/$${domain}/$1@lb-ip"/> // this is ip of kamailio
              <action application="answer"/>
            <!--  <action application="voicemail" data="default ${domain_name} $1"/> -->
  </condition>
</extension>
<extension name="Local_Extension">
...
```
config /etc/rsyslog.conf
```
local2.*                        -/var/log/kamailio.log
```

You don't need config user directory on FS, you don't need sync directory data between FS servers

restart kamailio and FS service, rsyslog

TEST
Add some sip on kamailio
kamctl add 8888 8888
kamctl add 9999 9999

register two sip phone with domain lb-ip
